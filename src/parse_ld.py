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
    )


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
            base = expr.instance_name or expr.type_name or "?"
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
    the pin it takes instead.
    """
    pin = via_pin
    if pin is None and node.outputs:
        pin = node.outputs[0][0]
    base = node.instance_name or node.type_name or "?"
    return Element(
        kind=IN_VARIABLE,
        label=(base + "." + pin) if pin else base,
        negated=pin in node.negated_outputs,
    )


def _build_block(node, by_id, visiting, via_pin, drawn):
    """Build a block call, separating power flow from parameter inputs.

    Exactly one input carries the rung's power flow. Pins fed by a literal or
    an inVariable are parameters, not power, so the first genuinely wired pin
    wins and the rest become captions inside the box.
    """
    if node.local_id in drawn:
        return _block_reference(node, via_pin)
    drawn.add(node.local_id)

    power_expr = Empty()
    power_pin = None
    power_negated = False
    power_edge = None
    side_pins = []
    pin_blocks = []

    for connection in node.inputs:
        upstream = by_id.get(connection.ref_id)
        if upstream is None:
            side_pins.append((connection.target_pin, "?"))
            continue
        sub_expr = _build_expr(upstream, by_id, visiting, connection.source_pin, drawn)
        if upstream.kind == IN_VARIABLE:
            # Flattened through expr_to_text, not taken from the raw label:
            # an in-place negated inVariable must keep its NOT, or the pin
            # silently inverts.
            side_pins.append((connection.target_pin, _pin_text(sub_expr, connection, pin_blocks)))
        elif power_pin is None:
            power_pin = connection.target_pin
            power_expr = sub_expr
            # The pin's own negation bubble; it inverts the power flow at the
            # box wall, after everything the rung has accumulated. The P or N
            # on that pin sits there too.
            power_negated = connection.negated
            power_edge = connection.edge
        else:
            side_pins.append((connection.target_pin, _pin_text(sub_expr, connection, pin_blocks)))

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
        output_wired=via_pin is not None,
        st_code=list(node.st_code),
        power_negated=power_negated,
        power_edge=power_edge,
        negated_outputs=set(node.negated_outputs),
        stored_outputs=node.stored_outputs,
        pin_blocks=pin_blocks,
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


def _build_expr(node, by_id, visiting, via_pin=None, drawn=None):
    """Walk backwards from a node to the power rail, building series/parallel.

    A node's expression is everything feeding it (OR'd together if there is
    more than one input) followed by the node itself. ``drawn`` carries the
    blocks already built for this network, so a block read by several outputs
    is drawn and called once.
    """
    if drawn is None:
        drawn = set()
    if node.local_id in visiting:
        # Feedback loops are not legal in a rung, but a malformed export should
        # produce a visible marker rather than blow the stack.
        return Element(kind="cycle", label="<cycle at %s>" % node.local_id)

    visiting = visiting | set([node.local_id])

    if node.kind == BLOCK:
        return _build_block(node, by_id, visiting, via_pin, drawn)

    branches = []
    for connection in node.inputs:
        upstream = by_id.get(connection.ref_id)
        if upstream is None:
            continue
        branches.append(_build_expr(upstream, by_id, visiting, connection.source_pin, drawn))

    incoming = parallel(branches) if branches else Empty()

    if node.kind in RAILS:
        # Rails are anchors, not symbols - they contribute nothing to draw.
        return incoming

    return series([incoming, _to_element(node)])


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

    # A block read by several outputs is built once, on the first rung that
    # reaches it; the rest name its output pin. The set is per POU, and a
    # block belongs to one network, so this cannot leak across networks.
    drawn = set()

    rungs_by_root = {}
    for node in nodes:
        if node.local_id in consumed or node.kind in (LEFT_RAIL, COMMENT, TITLE):
            # An unconnected left rail is an empty rung, not a terminal.
            continue
        expr = _build_expr(node, by_id, set(), None, drawn)
        if isinstance(expr, Empty):
            # An unconnected rail or a stray element with nothing on it.
            continue
        rungs_by_root.setdefault(root_of(node), []).append(expr)

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
