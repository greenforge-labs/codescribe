# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Low-level PLCopen XML helpers shared by every language renderer.

Namespaces are stripped rather than matched. The exact URI varies between
schema revisions - the hand-authored fixture is tc6_0201, real CODESYS output
is tc6_0200 - and CODESYS layers proprietary extensions on top. Matching local
tag names survives all of it.
"""

import io
import warnings

# CODESYS puts its own ScriptLib ahead of the standard library, and its xml
# package imports the deprecated xmllib on the way in. That prints a
# DeprecationWarning plus the offending source line into the message view,
# where CODESYS red-flags both as errors. Nobody can act on it - it is
# CODESYS's own bundled library - so it is silenced at the point it fires.
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    import xmlbackend

from model import Connection

TRUTHY = ("true", "1")

# Body element names, one of which wraps every POU implementation.
BODY_LANGUAGES = ("LD", "FBD", "SFC", "ST", "IL", "CFC")


def tag(elem):
    """Local tag name, with any namespace stripped."""
    return elem.tag.split("}")[-1]


def find_child(elem, name):
    for child in elem:
        if tag(child) == name:
            return child
    return None


def child_text(elem, name):
    child = find_child(elem, name)
    if child is None or child.text is None:
        return None
    return child.text.strip()


def is_true(elem, attr_name):
    return (elem.get(attr_name) or "").lower() in TRUTHY


def attr(elem, name):
    """An attribute, treating CODESYS's literal "none" as absent."""
    value = elem.get(name)
    if value in (None, "", "none"):
        return None
    return value


def direct_connections(elem):
    """Wires arriving at this element's own connectionPointIn children.

    Several <connection> under a single connectionPointIn is how PLCopen
    spells a parallel branch (a wired OR), so order and multiplicity matter.
    This deliberately does not recurse: a block's pins hang off
    <inputVariables> and are collected separately, with their pin names.
    """
    connections = []
    for point in elem:
        if tag(point) != "connectionPointIn":
            continue
        for child in point:
            if tag(child) != "connection":
                continue
            ref = child.get("refLocalId")
            if ref is not None:
                connections.append(Connection(ref, source_pin=attr(child, "formalParameter")))
    return connections


def block_connections(block_elem):
    """Wires arriving at a block, tagged with the pin they land on.

    A pin variable can carry negated="true" - the bubble CODESYS draws on the
    pin itself - and edge="rising"/"falling", the P or N that makes the pin
    see a change rather than a level. Both apply to everything arriving at
    that pin, so they ride on each connection.
    """
    connections = []
    for group_name in ("inputVariables", "inOutVariables"):
        group = find_child(block_elem, group_name)
        if group is None:
            continue
        for var in group:
            if tag(var) != "variable":
                continue
            pin = var.get("formalParameter")
            pin_negated = is_true(var, "negated")
            pin_edge = attr(var, "edge")
            for connection in direct_connections(var):
                connection.target_pin = pin
                connection.negated = pin_negated
                connection.edge = pin_edge
                connections.append(connection)
    return connections


def block_outputs(block_elem):
    """(pin, assigned variable) for each block output.

    CODESYS writes an assignment straight onto the output pin as
    <connectionPointOut><expression>uiCurrSupplyVolt</expression>.
    """
    outputs = []
    group = find_child(block_elem, "outputVariables")
    if group is None:
        return outputs
    for var in group:
        if tag(var) != "variable":
            continue
        assigned = None
        point = find_child(var, "connectionPointOut")
        if point is not None:
            expression = find_child(point, "expression")
            if expression is not None and expression.text:
                assigned = expression.text.strip()
        outputs.append((var.get("formalParameter"), assigned))
    return outputs


def stored_output_pins(block_elem):
    """{pin: "set" | "reset"} for output pins that store rather than assign.

    CODESYS writes storage="set" on the pin carrying an inline assignment,
    exactly as it does on a coil. A stored value is held until something
    resets it, so rendering one as a plain assignment says it clears the
    moment its condition drops - the opposite of what the program does.
    """
    stored = {}
    group = find_child(block_elem, "outputVariables")
    if group is None:
        return stored
    for var in group:
        if tag(var) != "variable":
            continue
        storage = attr(var, "storage")
        if storage:
            stored[var.get("formalParameter")] = storage
    return stored


def negated_output_pins(block_elem):
    """Output pins carrying an in-place negation bubble (negated="true").

    The value leaving such a pin is the inverse of the pin, so an inline
    assignment stores NOT pin and a consumer reads NOT pin. Dropping the flag
    renders the exact opposite of the program.
    """
    pins = set()
    group = find_child(block_elem, "outputVariables")
    if group is None:
        return pins
    for var in group:
        if tag(var) != "variable":
            continue
        if is_true(var, "negated"):
            pins.add(var.get("formalParameter"))
    return pins


def block_st_code(block_elem):
    """Inline ST carried by an EXECUTE box, as a list of lines.

    CODESYS puts the whole body of an EXECUTE box in an addData STCode
    element. It is the only content the box has, so ignoring it draws an empty
    box where a dozen lines of logic should be.
    """
    add_data = find_child(block_elem, "addData")
    if add_data is None:
        return []
    for data in add_data:
        if tag(data) != "data":
            continue
        code = find_child(data, "STCode")
        if code is not None and code.text:
            return code.text.replace("\r\n", "\n").strip("\n").split("\n")
    return []


def comment_text(elem):
    """The text of a <comment>, which nests its content in an xhtml element."""
    content = find_child(elem, "content")
    if content is None:
        return ""
    xhtml = find_child(content, "xhtml")
    if xhtml is None or xhtml.text is None:
        return ""
    return xhtml.text.strip()


# CODESYS stores a network's title as a vendorElement of this element type,
# with the text in alternativeText rather than in a content element.
NETWORK_TITLE = "networktitle"


def network_title(elem):
    """The title text of a network-title vendorElement, else None.

    A vendorElement is CODESYS editor state and most of them hold no logic,
    but this one holds the network's title - which is often the only
    description a network has, and marks where a network begins even when it
    has no comment.
    """
    is_title = False
    for child in elem.iter():
        if tag(child) == "ElementType" and (child.text or "").strip() == NETWORK_TITLE:
            is_title = True
            break
    if not is_title:
        return None
    alternative = find_child(elem, "alternativeText")
    if alternative is None:
        return ""
    xhtml = find_child(alternative, "xhtml")
    if xhtml is None or xhtml.text is None:
        return ""
    return xhtml.text.strip()


# --- interface -------------------------------------------------------------

SCOPE_TAGS = {
    "localVars": "VAR",
    "inputVars": "VAR_INPUT",
    "outputVars": "VAR_OUTPUT",
    "inOutVars": "VAR_IN_OUT",
    "tempVars": "VAR_TEMP",
    "globalVars": "VAR_GLOBAL",
}


def _type_name(var_elem):
    """The declared type, or UNKNOWN where the export does not carry one.

    Not BOOL: a variable whose type is missing is a variable whose type this
    file does not know, and calling it BOOL states a type the program may not
    have. UNKNOWN does not compile, which is the point - the rendered
    declaration is for reading, and it should not read as fact.
    """
    type_elem = find_child(var_elem, "type")
    if type_elem is None:
        return "UNKNOWN"
    for child in type_elem:
        name = tag(child)
        if name == "derived":
            return child.get("name") or "UNKNOWN"
        return name
    return "UNKNOWN"


def _initial_value(var_elem):
    value_elem = find_child(var_elem, "initialValue")
    if value_elem is None:
        return None
    simple = find_child(value_elem, "simpleValue")
    if simple is None:
        return None
    return simple.get("value")


def _add_data_declaration(owner):
    """A declaration blob anywhere in this element's own addData, or None.

    The whole addData subtree is walked rather than its first two levels.
    CODESYS writes the text under a data element named
    ".../plcopenxml/interfaceasplaintext", and how deeply it nests inside that
    is exactly the kind of detail that differs between versions.
    """
    if owner is None:
        return None
    add_data = find_child(owner, "addData")
    if add_data is None:
        return None
    candidates = []
    for element in add_data.iter():
        text = element.text
        if text and "VAR" in text and "END_VAR" in text:
            candidates.append((element, text.replace("\r\n", "\n").strip("\n")))
    if not candidates:
        return None

    named = []
    for element, text in candidates:
        name = (element.get("name") or "").lower()
        if "interfaceasplaintext" in name or "declaration" in name:
            named.append(text)
    if len(named) == 1:
        return named[0]
    if len(candidates) == 1:
        return candidates[0][1]
    return None


def declaration_text(pou_elem):
    """The lossless plaintext declaration, if CODESYS wrote one.

    Requested with export_xml(declarations_as_plaintext=True). The structured
    <interface> has nowhere to put a comment, a pragma or an attribute, so
    rebuilding a declaration from it silently drops all three - and a pragma
    like {attribute 'qualified_only'} changes what the code means.

    Both the interface's addData and the POU's own are searched, because the
    flag demonstrably writes the text - it grows the export by well over a
    kilobyte - but not inside <interface>, which was the only place the first
    attempt looked.

    Neither the element name nor the data name is matched exactly: this is a
    proprietary 3S extension whose naming has moved between CODESYS versions,
    and pinning a name that later changed would drop silently back to the
    lossy path. Requiring both VAR and END_VAR keeps that loose match from
    catching arbitrary prose.
    """
    if pou_elem is None:
        return None
    return _add_data_declaration(find_child(pou_elem, "interface")) or _add_data_declaration(pou_elem)


def parse_interface(interface_elem):
    """Variables from a POU interface, in declaration order."""
    from model import Variable

    variables = []
    if interface_elem is None:
        return variables
    for group in interface_elem:
        scope = SCOPE_TAGS.get(tag(group))
        if scope is None:
            continue
        if is_true(group, "constant"):
            scope += " CONSTANT"
        for var_elem in group:
            if tag(var_elem) != "variable":
                continue
            variables.append(
                Variable(
                    name=var_elem.get("name") or "",
                    type_name=_type_name(var_elem),
                    initial_value=_initial_value(var_elem),
                    scope=scope,
                )
            )
    return variables


def read_document(source):
    """Document bytes, with anything before the first tag removed.

    CODESYS writes a UTF-8 BOM on every export_xml file, and the ElementTree
    that CODESYS ships in ScriptLib rejects it outright:

        Error('Syntax error at line 1: illegal data at start of file',)

    CPython's expat accepts a BOM silently, so this is invisible outside
    CODESYS. Slicing to the first "<" handles the BOM however it is
    represented, plus any stray leading whitespace, in one step - nothing
    before the first tag can be XML anyway.

    ``source`` is a path or a file object. io.open is used rather than the
    builtin so a binary read returns real bytes under IronPython too.
    """
    if hasattr(source, "read"):
        data = source.read()
    else:
        handle = io.open(source, "rb")
        try:
            data = handle.read()
        finally:
            handle.close()

    if not isinstance(data, bytes):
        data = data.encode("utf-8")

    start = data.find(b"<")
    if start > 0:
        data = data[start:]
    return _to_ascii(data)


def _to_ascii(data):
    """Replace non-ASCII characters with XML numeric character references.

    The ElementTree CODESYS ships works byte-wise and rejects UTF-8 multi-byte
    sequences outright:

        Error('Syntax error at line 216: illegal character in content',)

    A numeric reference is plain ASCII, and every parser expands it back to
    the same character, so the parsed result is identical while the bytes
    handed to the parser are safe. One degree sign in a comment is enough to
    lose a whole POU otherwise.

    Safe as a blanket transform because PLCopen exports contain no CDATA
    sections, which are the one place a numeric reference would stay literal
    text instead of being expanded.
    """
    try:
        # Native-speed check, and the overwhelmingly common case. Scanning
        # byte by byte in Python costs real time on a large project.
        data.decode("ascii")
        return data
    except UnicodeDecodeError:
        pass

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        # Not valid UTF-8 despite the declaration. latin-1 cannot fail, and
        # preserves every byte as a character so nothing is lost.
        text = data.decode("latin-1")

    # A character outside the Basic Multilingual Plane is a surrogate pair in
    # a UTF-16 string, which is what IronPython has. Encoding that pair one
    # unit at a time writes two references for one character, and a lone
    # surrogate is not a legal XML character: System.Xml lets it through,
    # expat rejects the document outright. So the same export parses inside
    # CODESYS and fails everywhere else.
    if any(0xD800 <= ord(character) <= 0xDBFF for character in text):
        return _references(text)

    try:
        # This error handler does exactly the job, natively.
        return text.encode("ascii", "xmlcharrefreplace")
    except (LookupError, ValueError):
        return _references(text)


def _references(text):
    """Numeric references, one per character, surrogate pairs recombined."""
    pieces = []
    index = 0
    while index < len(text):
        code = ord(text[index])
        step = 1
        if 0xD800 <= code <= 0xDBFF and index + 1 < len(text):
            low = ord(text[index + 1])
            if 0xDC00 <= low <= 0xDFFF:
                code = 0x10000 + ((code - 0xD800) << 10) + (low - 0xDC00)
                step = 2
        pieces.append(text[index] if code < 128 else "&#%d;" % code)
        index += step
    return "".join(pieces).encode("ascii")


# XML 1.0 forbids these outright - they cannot even be written as a numeric
# reference, so a document containing one is malformed at the source.
_LEGAL_CONTROL = (0x09, 0x0A, 0x0D)


def describe_suspect_characters(source, limit=5):
    """Characters likely to make a parser reject the document.

    Reported on a rendering failure so the next run explains itself, rather
    than needing another round of manual diagnosis.
    """
    try:
        handle = io.open(source, "rb")
        try:
            raw = handle.read()
        finally:
            handle.close()
    except (IOError, OSError) as error:
        return ["could not re-read the file: " + repr(error)]

    notes = []
    for line_number, line in enumerate(raw.split(b"\n"), 1):
        for column, byte in enumerate(bytearray(line), 1):
            if byte < 0x20 and byte not in _LEGAL_CONTROL:
                notes.append(
                    "line %d column %d: control character 0x%02X, illegal in XML 1.0" % (line_number, column, byte)
                )
            elif byte > 0x7F:
                notes.append("line %d column %d: non-ASCII byte 0x%02X" % (line_number, column, byte))
            if len(notes) >= limit:
                return notes
    return notes


def find_pous(root):
    """POU elements, without walking the whole document to find them.

    PLCopen puts them at project/types/pous/pou. Scanning every element
    instead meant touching a few thousand nodes per file to reach one or two,
    which is pure waste under any backend and expensive under one whose
    elements are wrapped in Python objects. The full walk stays as a fallback
    for any layout that does not match.
    """
    types = find_child(root, "types")
    if types is not None:
        pous = find_child(types, "pous")
        if pous is not None:
            found = [child for child in pous if tag(child) == "pou"]
            if found:
                return found
    return [elem for elem in root.iter() if tag(elem) == "pou"]


def _language_body(owner):
    """(language, body_elem) for an element's own <body>, or None."""
    body = find_child(owner, "body")
    if body is None:
        return None
    for child in body:
        if tag(child) in BODY_LANGUAGES:
            return tag(child), child
    return None


def iter_bodies(source):
    """Yield (pou_elem, language, body_elem) for every POU with an implementation."""
    root = xmlbackend.parse(read_document(source))
    for elem in find_pous(root):
        found = _language_body(elem)
        if found is not None:
            yield elem, found[0], found[1]


# Sub-POU elements that carry a name and a body of their own. Matched without
# regard to case: an export writes <Method name="..."> with a capital M where
# it writes <action> in lower case, and matching only one spelling means the
# other kind never renders at all. An SFC body's inline <action> blocks share
# the tag but carry a localId instead of a name, so requiring the name to
# match keeps them out.
MEMBER_TAGS = ("action", "transition", "method")


def iter_member_bodies(source, member_name):
    """Yield (pou_elem, language, body_elem) for a named sub-POU member.

    PLCopen has no top-level element for an action or transition, so CODESYS
    exports the *parent* POU with the member nested inside it - parent body
    included. Rendering the pou's own <body> from such a file draws the
    parent's networks under the member's filename, which is how the HMI
    PLC_PRG.ACT_* dumps came to describe a different POU than the .xml
    beside them.

    The member is found by name: either a pou element named for the member
    itself (how some builds export methods), or an action/transition/method
    element with a matching name attribute anywhere inside a pou. IEC
    identifiers are case-insensitive, so the comparison is too. Yielding
    nothing at all is the honest outcome when the export simply does not
    carry the member's body - the caller then writes no rendering rather
    than a foreign one.
    """
    root = xmlbackend.parse(read_document(source))
    wanted = member_name.lower()
    for pou_elem in find_pous(root):
        pou_name = (pou_elem.get("name") or "").lower()
        if pou_name == wanted or pou_name.endswith("." + wanted):
            found = _language_body(pou_elem)
            if found is not None:
                yield pou_elem, found[0], found[1]
            continue
        for elem in pou_elem.iter():
            if tag(elem).lower() not in MEMBER_TAGS:
                continue
            elem_name = (elem.get("name") or "").lower()
            if elem_name != wanted and not elem_name.endswith("." + wanted):
                continue
            found = _language_body(elem)
            if found is not None:
                yield pou_elem, found[0], found[1]
