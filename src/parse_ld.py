# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Parse Ladder Diagram bodies out of PLCopen XML.

The XML-level helpers live in plcopen.py; this module owns the LD-specific
part: turning a flat list of wired elements into one series/parallel
expression tree per rung.
"""

from model import (
    BLOCK,
    COMMENT,
    EDGE_FUNCTION,
    IN_VARIABLE,
    JUMP,
    LABEL,
    LEFT_RAIL,
    RAILS,
    RETURN,
    RIGHT_RAIL,
    TITLE,
    CONTACT,
    COIL,
    Element,
    Empty,
    Network,
    Node,
    Parallel,
    Pou,
    Series,
    assemble_networks,
    box_name,
    component_finder,
    is_simple_term,
    parallel,
    series,
)
from plcopen import (
    attr,
    block_connections,
    block_outputs,
    block_st_code,
    child_text,
    comment_text,
    declaration_text,
    direct_connections,
    find_child,
    is_true,
    iter_bodies,
    negated_output_pins,
    network_title,
    parse_interface,
    stored_output_pins,
    tag,
)

VENDOR_ELEMENT = "vendorElement"

# Elements that carry logic. Rails are structural: they anchor a rung but draw
# nothing themselves; a comment and a network title carry no logic either, but
# both head the network they precede.
KNOWN_KINDS = (
    LEFT_RAIL,
    RIGHT_RAIL,
    CONTACT,
    COIL,
    BLOCK,
    "inVariable",
    "outVariable",
    JUMP,
    RETURN,
    LABEL,
    COMMENT,
    VENDOR_ELEMENT,
)


def _node_label(elem, kind):
    if kind == BLOCK:
        # typeName and instanceName are attributes in CODESYS's output, not
        # the child elements a literal schema reading would suggest.
        return elem.get("instanceName") or elem.get("typeName")
    if kind in (JUMP, LABEL):
        # The target is a "label" attribute, not a child element - same as in
        # FBD bodies. Reading child elements here loses the target entirely.
        return elem.get("label")
    return child_text(elem, "variable") or child_text(elem, "expression")


def parse_ld_body(body_elem):
    """Return an ordered list of Nodes from an <LD> body element."""
    nodes = []
    for child in body_elem:
        kind = tag(child)
        if kind not in KNOWN_KINDS:
            continue
        local_id = child.get("localId")
        if local_id is None:
            continue

        if kind == COMMENT:
            # No logic of its own, but CODESYS writes one above each network
            # that has a comment, and it names the network that follows it.
            nodes.append(Node(local_id=local_id, kind=COMMENT, label=comment_text(child)))
            continue

        if kind == VENDOR_ELEMENT:
            title = network_title(child)
            if title is not None:
                nodes.append(Node(local_id=local_id, kind=TITLE, label=title))
            continue

        is_block = kind == BLOCK
        nodes.append(
            Node(
                local_id=local_id,
                kind=kind,
                label=_node_label(child, kind),
                negated=is_true(child, "negated"),
                edge=attr(child, "edge"),
                storage=attr(child, "storage"),
                inputs=block_connections(child) if is_block else direct_connections(child),
                type_name=child.get("typeName") if is_block else None,
                instance_name=child.get("instanceName") if is_block else None,
                outputs=block_outputs(child) if is_block else None,
                st_code=block_st_code(child) if is_block else None,
                negated_outputs=negated_output_pins(child) if is_block else None,
                stored_outputs=stored_output_pins(child) if is_block else None,
            )
        )
    return nodes


# --- graph to expression tree ----------------------------------------------


def _to_element(node):
    return Element(
        kind=node.kind,
        label=node.label,
        negated=node.negated,
        edge=node.edge,
        storage=node.storage,
        local_id=node.local_id,
    )


# While the networks are built: the set of localIds of boxes with no instance
# name that a caption has named, wherever in the caption they sit. None at any
# other time, such as when the ST renderer flattens an expression.
_naming = None


def expr_to_text(expr):
    """Flatten an expression to one line of ST-ish text.

    Used for a block's side inputs: a RESET pin fed by its own contact chain
    cannot be drawn as a second horizontal wire without a genuine 2-D layout,
    so it is written into the pin as "RESET := PowerOff" instead.
    """
    if isinstance(expr, Empty):
        return ""
    if isinstance(expr, Series):
        parts = [part for part in (expr_to_text(item) for item in expr.items) if part]
        return " AND ".join(parts)
    if isinstance(expr, Parallel):
        parts = [part for part in (expr_to_text(branch) for branch in expr.branches) if part]
        return "(" + " OR ".join(parts) + ")"
    if isinstance(expr, Element):
        if expr.kind == BLOCK:
            base = box_name(expr)
            if _naming is not None and not expr.instance_name and expr.local_id is not None:
                _naming.add(expr.local_id)
            text = (base + "." + expr.active_output) if expr.active_output else base
            # The negation bubble on the consumed output inverts what leaves
            # the box - on this flattened path just like on the power flow.
            if expr.active_output in expr.negated_outputs:
                return "NOT " + text
            return text
        label = expr.label or ""
        if expr.edge == "rising":
            return "R(" + label + ")"
        if expr.edge == "falling":
            return "F(" + label + ")"
        if expr.negated:
            return "NOT " + _bracket(label)
        return label
    return "?"


def _bracket(text):
    """Parenthesise a compound term before negating or nesting it.

    NOT binds above OR, AND and even comparison in IEC 61131-3, so both
    "NOT xA OR xB" and the spaceless "NOT iCount>5" regroup the logic their
    bracketed forms state.
    """
    if is_simple_term(text):
        return text
    return "(" + text + ")"


def _block_reference(node, via_pin):
    """A box already drawn in this network, named by the output being read.

    A block driving three outputs is one box that runs once. Rebuilding it for
    every output drew it three times and called it three times, which reads as
    three timers where the program has one; every reader after the first names
    the pin it takes instead. Only an instance can be named this way - an
    operator has no name, so its caller redraws it rather than reach here.
    """
    pin = via_pin
    if pin is None and node.outputs:
        pin = node.outputs[0][0]
    base = box_name(node)
    return Element(
        kind=IN_VARIABLE,
        label=(base + "." + pin) if pin else base,
        negated=pin in node.negated_outputs,
        local_id=node.local_id,
    )


def _is_contact_chain(expr):
    """True when an expression is nothing but contacts (and bare wire).

    A side pin fed by one is drawn as those contacts, wired into the pin; a
    pin fed by a literal, a box or anything else keeps its flattened caption.
    """
    if isinstance(expr, Element):
        return expr.kind == CONTACT
    if isinstance(expr, Series):
        parts = [item for item in expr.items if not isinstance(item, Empty)]
        return bool(parts) and all(_is_contact_chain(item) for item in parts)
    if isinstance(expr, Parallel):
        return bool(expr.branches) and all(_is_contact_chain(branch) for branch in expr.branches)
    return False


def _build_block(node, by_id, visiting, via_pin, drawn, consumed=None):
    """Build a block call, separating power flow from parameter inputs.

    Exactly one input carries the rung's power flow. Pins fed by a literal or
    an inVariable are parameters, not power, so the first genuinely wired pin
    wins and the rest become captions inside the box.
    """
    read_pin = via_pin
    if read_pin is None and node.outputs:
        read_pin = node.outputs[0][0]
    if node.local_id in drawn.pins:
        # Drawn once already. A stateful function block is one box that runs
        # once, so the next reader names the pin it takes. A stateless
        # operator has no instance to name - "OR.Out1" points at no variable -
        # so a reader of the same pin redraws it, and the rung merge then draws
        # the copies as one box. A reader of a different pin cannot merge: the
        # copies differ in the pin the wire leaves by, and a redraw is a second
        # box where the editor has one. That reader names the pin instead, and
        # box_name numbers the box if its type alone would not say which.
        if node.instance_name or drawn.pins[node.local_id] != read_pin:
            if not node.instance_name:
                drawn.named.add(node.local_id)
            return _block_reference(node, via_pin)
    else:
        drawn.order[node.local_id] = len(drawn.order)
    drawn.pins[node.local_id] = read_pin

    power_expr = Empty()
    power_pin = None
    power_negated = False
    power_edge = None
    side_pins = []
    pin_blocks = []
    pin_feeds = {}
    pin_marks = {}

    # Several connections landing on one pin are a wired OR into that pin -
    # the same several-<connection>-under-one-connectionPointIn shape a coil
    # or a contact collects into a Parallel. Grouped by pin so those branches
    # feed the pin as one OR, rather than being spread across duplicate
    # captions ("IN := xStart, IN := xRun") that lose the OR and read as two
    # separate pins.
    order = []
    grouped = {}
    for connection in node.inputs:
        if connection.target_pin not in grouped:
            grouped[connection.target_pin] = []
            order.append(connection.target_pin)
        grouped[connection.target_pin].append(connection)

    for pin in order:
        connections = grouped[pin]
        branches = []
        all_from_variables = True
        for connection in connections:
            upstream = by_id.get(connection.ref_id)
            if upstream is None:
                continue
            if upstream.kind != IN_VARIABLE:
                all_from_variables = False
            branches.append(_build_expr(upstream, by_id, visiting, connection.source_pin, drawn, consumed))
        # The bubble and the P or N ride on the pin, so every connection to it
        # carries the same pair; the first speaks for the group.
        negated = connections[0].negated
        edge = connections[0].edge
        if not branches:
            side_pins.append((pin, "?"))
            continue
        feed = branches[0] if len(branches) == 1 else parallel(branches)
        if all_from_variables:
            # Flattened through expr_to_text, not taken from the raw label:
            # an in-place negated inVariable must keep its NOT, or the pin
            # silently inverts.
            side_pins.append((pin, _pin_text(feed, connections[0], pin_blocks)))
        elif power_pin is None:
            power_pin = pin
            power_expr = feed
            # The pin's own negation bubble; it inverts the power flow at the
            # box wall, after everything the rung has accumulated. The P or N
            # on that pin sits there too.
            power_negated = negated
            power_edge = edge
        else:
            # A side pin fed by contacts - a reset or enable off the rail - is
            # drawn as the contacts it is, wired into the pin, rather than
            # flattened into the caption. The text form stays for the ST. The
            # pin's own bubble or P/N goes on the box wall, as the power pin's
            # does; a pin carrying both keeps the caption, which spells out
            # the two where the wall has room for one.
            if _is_contact_chain(feed) and not (negated and edge):
                pin_feeds[pin] = feed
                if negated or edge:
                    pin_marks[pin] = (negated, edge)
            side_pins.append((pin, _pin_text(feed, connections[0], pin_blocks)))

    input_pins = []
    if power_pin is not None:
        # None marks the power pin, and it sorts first so the wire runs
        # straight through the box instead of jogging to another row.
        input_pins.append((power_pin, None))
    input_pins.extend(side_pins)

    active = via_pin
    if active is None and node.outputs:
        active = node.outputs[0][0]
    output_pins = [out for out in node.outputs if out[0] == active]
    output_pins += [out for out in node.outputs if out[0] != active]

    element = Element(
        kind=BLOCK,
        label=node.label,
        type_name=node.type_name,
        instance_name=node.instance_name,
        input_pins=input_pins,
        output_pins=output_pins,
        active_output=active,
        # via_pin is set by whatever consumed this block; a block terminating
        # the rung has none.
        # Wired when a pin was named, or when anything downstream reads the
        # block at all - a contact reading a block output does not always
        # name the pin, and the box must still tee where it is consumed.
        output_wired=via_pin is not None or (consumed is not None and node.local_id in consumed),
        pin_feeds=pin_feeds,
        pin_marks=pin_marks,
        st_code=list(node.st_code),
        power_negated=power_negated,
        power_edge=power_edge,
        negated_outputs=set(node.negated_outputs),
        stored_outputs=node.stored_outputs,
        pin_blocks=pin_blocks,
        local_id=node.local_id,
        ordinal=node.ordinal,
    )
    return series([power_expr, element])


def _pin_expr_text(expr, hoisted):
    """A side pin's condition text, hoisting any box out of it.

    A box wired into a side pin is not a term of that pin's condition: it is
    a call in its own right, and everything to its left on the wire is its
    input, not the pin's. Flattening the whole chain into the caption states
    logic the program does not have - "RESET := xB AND NOT tmrA.Q" for a
    rung that resets on NOT tmrA.Q alone - so the chain up to and including
    the box is hoisted into ``hoisted`` to be rendered and called as its own
    sub-rung, and only the output the pin reads is named here. This is what
    the power path already does; see rung_to_statements.
    """
    if isinstance(expr, Series):
        items = expr.items
        # The last box on the wire is the one the pin reads. Anything before
        # it feeds it, anything after it operates on its output.
        cut = -1
        for index, item in enumerate(items):
            if isinstance(item, Element) and item.kind == BLOCK:
                cut = index
        if cut < 0:
            return expr_to_text(expr)
        hoisted.append(series(items[: cut + 1]))
        parts = [part for part in (expr_to_text(item) for item in items[cut:]) if part]
        return " AND ".join(parts)
    if isinstance(expr, Parallel):
        parts = [part for part in (_pin_expr_text(branch, hoisted) for branch in expr.branches) if part]
        return "(" + " OR ".join(parts) + ")"
    if isinstance(expr, Element) and expr.kind == BLOCK:
        # A box feeding the pin directly still has a call to make; without
        # this it is named in the caption and never called at all.
        hoisted.append(expr)
        return expr_to_text(expr)
    return expr_to_text(expr)


def pin_value(text, negated=False, edge=None):
    """A value as the pin receives it: bubble first, then edge detection.

    The bubble inverts what arrives; the P or N then triggers on that value
    changing. Dropping the edge renders a block that runs once per change as
    one that runs every cycle its input is true.
    """
    if negated:
        text = "NOT " + _bracket(text) if text else "NOT ?"
    function = EDGE_FUNCTION.get(edge)
    if function:
        return function + "(" + (text or "?") + ")"
    return text


def _pin_text(sub_expr, connection, hoisted):
    """A side pin's caption, honouring the pin's own bubble and edge."""
    return pin_value(_pin_expr_text(sub_expr, hoisted), connection.negated, connection.edge)


def _build_expr(node, by_id, visiting, via_pin=None, drawn=None, consumed=None):
    """Walk backwards from a node to the power rail, building series/parallel.

    A node's expression is everything feeding it (OR'd together if there is
    more than one input) followed by the node itself. ``drawn`` carries the
    blocks already built for this network, so a block read by several outputs
    is drawn and called once.
    """
    if drawn is None:
        drawn = _Built()
    if node.local_id in visiting:
        # Feedback loops are not legal in a rung, but a malformed export should
        # produce a visible marker rather than blow the stack.
        return Element(kind="cycle", label="<cycle at %s>" % node.local_id)

    visiting = visiting | set([node.local_id])

    if node.kind == BLOCK:
        return _build_block(node, by_id, visiting, via_pin, drawn, consumed)

    branches = []
    for connection in node.inputs:
        upstream = by_id.get(connection.ref_id)
        if upstream is None:
            continue
        branches.append(_build_expr(upstream, by_id, visiting, connection.source_pin, drawn, consumed))

    incoming = parallel(branches) if branches else Empty()

    if node.kind in RAILS:
        # Rails are anchors, not symbols - they contribute nothing to draw.
        return incoming

    return series([incoming, _to_element(node)])


class _Built(object):
    """The blocks built so far for one POU."""

    def __init__(self):
        # {localId: the pin the block was first built for}
        self.pins = {}
        # {localId: the order blocks were first built in}. That follows the
        # rungs in export order; a box hoisted into a side pin is built after
        # the box that reads it, though it is drawn above it.
        self.order = {}
        # localIds of boxes with no instance name that the text names - in a
        # reference to a pin, or anywhere in a side pin's caption
        self.named = set()


def _number_named_boxes(logic, find, built):
    """Give an ordinal to each box that its type alone would not identify.

    Only in a network holding two or more boxes of one type with no instance
    name, and only where the text names one of them; everywhere else a box is
    written as it always was. Numbered in the order the boxes are first built,
    which is fixed by the export and so stable from one export to the next.
    Returns True when any box was numbered, so the networks must be rebuilt.
    """
    groups = {}
    for node in logic:
        if node.kind == BLOCK and not node.instance_name:
            groups.setdefault((find(node.local_id), node.type_name), []).append(node)

    numbered = False
    for group in groups.values():
        if len(group) < 2 or not any(node.local_id in built.named for node in group):
            continue
        # A box never built draws nowhere; it goes last, in export order.
        group.sort(key=lambda node: (node.local_id not in built.order, built.order.get(node.local_id, 0)))
        for index, node in enumerate(group):
            node.ordinal = index + 1
        numbered = True
    return numbered


def build_networks(nodes):
    """Group a flat node list into Networks, each holding its rungs.

    A rung is identified by its terminal: an element nothing else consumes.
    That is the right power rail where one exists, and the coil itself where
    the export omits it - CODESYS exports the right rail unconnected.

    Networks are the connected components, as in parse_fbd - but the rails
    are left out of the grouping. CODESYS exports one left rail for the whole
    LD body, not one per network, so every rung in the POU hangs off the same
    element and following that wire would fuse the lot into a single network.
    One network per sink is no better: a block driving three outputs is one
    network in the editor, and numbering it as three throws out every number
    after it.
    """
    by_id = {}
    for node in nodes:
        by_id[node.local_id] = node

    logic = [node for node in nodes if node.kind not in RAILS and node.kind not in (COMMENT, TITLE)]
    known = set(node.local_id for node in logic)
    find = component_finder(logic)

    def root_of(node):
        """Which network a terminal belongs to.

        A right power rail is an anchor rather than logic, so it is not in the
        grouping itself - but it is the terminal of the rung that ends at it,
        and it belongs to that rung's network.
        """
        if node.local_id in known:
            return find(node.local_id)
        for connection in node.inputs:
            if connection.ref_id in known:
                return find(connection.ref_id)
        return node.local_id

    consumed = set()
    for node in nodes:
        for connection in node.inputs:
            consumed.add(connection.ref_id)

    def build_rungs():
        # A block read by several outputs is built once, on the first rung that
        # reaches it; the rest name its output pin. Per POU, and a block belongs
        # to one network, so this cannot leak across networks.
        global _naming
        built = _Built()
        rungs_by_root = {}
        _naming = built.named
        try:
            for node in nodes:
                if node.local_id in consumed or node.kind in (LEFT_RAIL, COMMENT, TITLE):
                    # An unconnected left rail is an empty rung, not a terminal.
                    continue
                expr = _build_expr(node, by_id, set(), None, built, consumed)
                if isinstance(expr, Empty):
                    # An unconnected rail or a stray element with nothing on it.
                    continue
                rungs_by_root.setdefault(root_of(node), []).append(expr)
        finally:
            _naming = None
        return rungs_by_root, built

    for node in logic:
        node.ordinal = None
    rungs_by_root, built = build_rungs()
    # Which boxes the text names is known only once the rungs are built, and
    # their names are written while building - so a numbered POU builds twice.
    if _number_named_boxes(logic, find, built):
        rungs_by_root, built = build_rungs()

    # A component that is nothing but a jump label is the label of the network
    # that follows it, not a network of its own.
    label_roots = set()
    for root, rungs in rungs_by_root.items():
        if rungs and all(isinstance(rung, Element) and rung.kind == LABEL for rung in rungs):
            label_roots.add(root)

    def network_root(node):
        if node.kind == LEFT_RAIL:
            return None
        return root_of(node)

    return [
        Network(comment=comment, title=title, label=label, outputs=rungs)
        for comment, title, label, rungs in assemble_networks(nodes, network_root, rungs_by_root, label_roots)
    ]


LANGUAGE = "LD"


def pou_from_body(pou_elem, body_elem):
    """Build a Pou from an already-located <LD> body.

    Split out from parse_pous so a caller handling several languages can make
    a single pass over the document instead of re-reading and re-parsing it
    once per language.
    """
    return Pou(
        name=pou_elem.get("name") or "<unnamed>",
        pou_type=pou_elem.get("pouType") or "program",
        language=LANGUAGE,
        variables=parse_interface(find_child(pou_elem, "interface")),
        declaration_text=declaration_text(pou_elem),
        networks=build_networks(parse_ld_body(body_elem)),
    )


def parse_pous(source):
    """Parse every LD POU in a PLCopen file. Other languages are skipped.

    ``source`` is a path or a file object, as accepted by ElementTree.
    """
    pous = []
    for pou_elem, language, body in iter_bodies(source):
        if language == LANGUAGE:
            pous.append(pou_from_body(pou_elem, body))
    return pous
