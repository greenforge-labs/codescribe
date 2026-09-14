# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Render a parsed Ladder Diagram as rungs.

Layout comes from the expression tree only - the x/y coordinates in the source
XML are deliberately ignored. Dragging a contact sideways in CODESYS must not
show up as a diff.

Composition works on Blocks: a rectangle of text plus the row index its wire
enters and leaves on. Series concatenates Blocks horizontally aligned on that
row; Parallel stacks them and threads a junction column down each side.

Drawing characters come from charset, so the same layout renders as either
box-drawing Unicode or plain ASCII.
"""

from __future__ import unicode_literals

import charset
from layout import Block, centred
from model import BLOCK, COIL, CONTACT, Element, Empty, Parallel, Series, parallel, series

# The letter a contact carries for edge detection, reused on a block's power
# pin so both read the same.
EDGE_MARKER = {"rising": "P", "falling": "N"}

POU_TYPE_KEYWORDS = {
    "program": "PROGRAM",
    "functionBlock": "FUNCTION_BLOCK",
    "function": "FUNCTION",
}


def _one_line(text):
    """Comment text safe to put inside a generated (* *) block.

    A comment can span lines and can contain "*)", either of which would
    terminate the block early and leave the rest of it as code.
    """
    return text.replace("\r", " ").replace("\n", " ").replace("*)", "* )")


def network_headers(number, network):
    """The header lines above one network: its number, title and comment.

    CODESYS keeps a network's title separately from its comment and draws the
    title above it, as the network's heading. So the title goes on the number
    line and the comment below it, in the order the editor shows them. A
    network with no title puts its comment on the number line instead, rather
    than spending a line on an empty heading - most networks have one or the
    other, not both.
    """
    comment = _one_line(network.comment or "").lstrip("/").strip()
    title = _one_line(getattr(network, "title", "") or "").lstrip("/").strip()

    header = "(* Network " + str(number)
    heading = title or comment
    if heading:
        header += ": " + heading
    lines = [header + " *)"]
    if title and comment:
        lines.append("(* " + comment + " *)")
    label = _one_line(getattr(network, "label", "") or "").strip()
    if label:
        # CODESYS keeps the label on the network; PLCopen exports it as a
        # loose element, so it is only known here when the native export has
        # been read. Written as ST writes it - a jump target is program
        # structure, and inside (* *) it would read as a comment.
        lines.append(label + ":")
    note = getattr(network, "note", None)
    if note:
        lines.append("(* " + note + " *)")
    return lines


def _symbol_and_label(element):
    """The drawn symbol, and the caption sitting above it."""
    chars = charset.active()
    kind = element.kind

    if kind == CONTACT:
        if element.edge == "rising":
            middle = "P"
        elif element.edge == "falling":
            middle = "N"
        elif element.negated:
            middle = "/"
        else:
            middle = " "
        return chars["CONTACT_L"] + middle + chars["CONTACT_R"], element.label or ""

    if kind == COIL:
        if element.storage == "set":
            middle = "S"
        elif element.storage == "reset":
            middle = "R"
        elif element.negated:
            middle = "/"
        else:
            middle = " "
        return "(" + middle + ")", element.label or ""

    if kind == "jump":
        return ">>" + (element.label or "?"), ""

    if kind == "return":
        return "<RETURN>", ""

    if kind == "label":
        # A jump target: a marker in the rung order, not a symbol on a wire.
        return (element.label or "?") + ":", ""

    # In/out variables and anything unrecognised draw as a named box so
    # unhandled logic is visible rather than silently dropped. A negated
    # variable spells its NOT out - there is no bubble to draw on a box.
    label = element.label or "?"
    if element.storage == "set":
        # The same marker a set coil carries: this store holds until a reset.
        label = "(S) " + label
    elif element.storage == "reset":
        label = "(R) " + label
    elif element.negated:
        label = "NOT " + label
    return "[" + label + "]", ""


def _pin_arrow(box, pin):
    """The inline form, for a store on the pin the rung's wire leaves by.

    "=o>" is "=>" with the negation bubble: the pin stores its inverse. "=S>"
    and "=R>" are the set and reset a pin can carry, exactly as a coil does.
    """
    storage = box.stored_outputs.get(pin)
    if storage == "set":
        return " =S> "
    if storage == "reset":
        return " =R> "
    return " =o> " if pin in box.negated_outputs else " => "


def _pin_head(box, pin):
    """The arrow head on a store hung off an output pin on its own wire.

    The same heads a coil carries: "o>" for the negation bubble, "(S)>" and
    "(R)>" for a set and a reset.
    """
    storage = box.stored_outputs.get(pin)
    if storage == "set":
        return "(S)> "
    if storage == "reset":
        return "(R)> "
    return "o> " if pin in box.negated_outputs else "> "


def _render_block(element):
    """Draw a function block as a pin box.

    The power pin sorts first, so the wire enters and leaves on the same row.
    Only pins that are genuinely wired get a tee on the box edge; a
    parameterised or unconsumed pin leaves the wall unbroken.
    """
    chars = charset.active()

    # The value feeding a side pin is drawn to the left of the box, on a wire
    # into the pin, the way the editor draws it and the way the FBD renderer
    # already does. Written inside as "PT := T#5S" it reads as part of the pin
    # name, and it widens the box by the length of every value in it.
    left = []
    wired = []
    values = []
    for pin, label in element.input_pins:
        left.append(pin or "?")
        # A label of None is the power pin - it is wired, not parameterised.
        wired.append(label is None)
        values.append("" if label is None else (label or ""))

    # A store written on an output pin hangs off that pin on a wire of its
    # own, as CODESYS draws it. Writing it inside the box put the target
    # variable in among the pin names, where it reads as another pin.
    right = []
    tails = []
    for index, pin_and_assignment in enumerate(element.output_pins):
        pin, assigned = pin_and_assignment
        text = pin or "?"
        wired_out = element.output_wired and pin == element.active_output
        tail = ""
        if assigned and index > 0:
            # Hung off the pin, as CODESYS draws it. Only below the first row:
            # that one carries the rung's own wire onward to the rail, and a
            # store sharing it would read as the rung running through it.
            tail = chars["H"] * 3 + _pin_head(element, pin) + assigned
        elif assigned:
            text += _pin_arrow(element, pin) + assigned
        elif pin in element.negated_outputs and not wired_out:
            # A wired pin draws its bubble on the box edge instead - one
            # bubble, not two.
            text += " o"
        right.append(text)
        tails.append(tail)

    rows = max(len(left), len(right), 1)
    left += [""] * (rows - len(left))
    wired += [False] * (rows - len(wired))
    values += [""] * (rows - len(values))
    right += [""] * (rows - len(right))
    tails += [""] * (rows - len(tails))

    title = element.title
    # An EXECUTE box carries its inline ST as its body: the lines sit inside
    # the box, below the pins, and widen it to the longest of them. Tabs are
    # expanded to spaces so the box's right wall stays straight - a tab counts
    # as one character but draws as several.
    code = [line.expandtabs(4) for line in element.st_code]
    inner = max([len(title)] + [len(left[i]) + 3 + len(right[i]) for i in range(rows)] + [len(line) + 2 for line in code])

    # Two columns to the left of the box: the widest value, then a short wire
    # into the pin. The power pin's row is all wire - the rung feeds that one.
    lead = max([len(value) for value in values] + [0])
    lead = lead + 2 if lead else 0

    def feed(index):
        if not lead:
            return ""
        if wired[index]:
            return chars["H"] * lead
        value = values[index]
        if not value:
            return " " * lead
        return value + chars["H"] * (lead - len(value))

    lines = [" " * lead + centred(title, inner + 2)]
    lines.append(" " * lead + chars["TL"] + chars["H"] * inner + chars["TR"])
    for index in range(rows):
        gap = inner - len(left[index]) - len(right[index])
        # A pin fed from the left breaks the wall, whether the rung feeds it
        # or a value does. A pin with nothing on it leaves the wall unbroken.
        left_edge = chars["PIN_L"] if (wired[index] or values[index]) else chars["V"]
        if wired[index] and element.power_edge in EDGE_MARKER:
            # The P or N on the power pin, drawn on the box wall in the same
            # place the bubble goes and the same letter a contact carries.
            left_edge = EDGE_MARKER[element.power_edge]
        elif wired[index] and element.power_negated:
            # The negation bubble on the power pin, drawn on the box wall.
            left_edge = "o"
        # Only the active output continues onward, and only if consumed - but
        # a pin with a store on it breaks the wall for that wire too.
        onward = index == 0 and element.output_wired
        right_edge = chars["PIN_R"] if (onward or tails[index]) else chars["V"]
        if onward and element.active_output in element.negated_outputs:
            right_edge = "o"
        lines.append(feed(index) + left_edge + left[index] + " " * gap + right[index] + right_edge + tails[index])
    for line in code:
        # A body line of an EXECUTE box, inside the box below the pins.
        lines.append(" " * lead + chars["V"] + " " + line + " " * (inner - len(line) - 1) + chars["V"])
    lines.append(" " * lead + chars["BL"] + chars["H"] * inner + chars["BR"])

    # Row 0 is the title and row 1 the top border, so the first pin is row 2.
    connect_row = 2

    # A lead-in and lead-out stub, so back-to-back boxes do not fuse into one
    # unreadable run of border characters.
    stubbed = []
    for index, line in enumerate(lines):
        stub = chars["H"] if index == connect_row else " "
        stubbed.append(stub + line + stub)

    return Block(stubbed, connect_row)


def _render_element(element):
    if element.kind == BLOCK:
        return _render_block(element)

    chars = charset.active()
    symbol, label = _symbol_and_label(element)
    width = max(len(label) + 2, len(symbol) + 4)

    lead = (width - len(symbol)) // 2
    symbol_line = chars["H"] * lead + symbol + chars["H"] * (width - len(symbol) - lead)

    lead = (width - len(label)) // 2
    label_line = " " * lead + label + " " * (width - len(label) - lead)

    return Block([label_line, symbol_line], 1)


def _render_series(items):
    blocks = [_render(item) for item in items]
    connect_row = max(block.connect_row for block in blocks)
    height = max(connect_row - block.connect_row + len(block.lines) for block in blocks)

    columns = []
    for block in blocks:
        width = block.width
        above = connect_row - block.connect_row
        lines = [" " * width] * above
        # The wire row is padded with wire, not spaces: a box with a store
        # hanging off a lower pin is wider than its own wire row, and padding
        # that with spaces broke the rung in half.
        lines += block.padded(width)
        lines += [" " * width] * (height - len(lines))
        columns.append(lines)

    joined = []
    for row in range(height):
        joined.append("".join(column[row] for column in columns))
    return Block(joined, connect_row)


def _branch_has_block(expr):
    """True when a parallel branch carries a function block somewhere in it."""
    if isinstance(expr, Element):
        return expr.kind == BLOCK
    if isinstance(expr, Series):
        return any(_branch_has_block(item) for item in expr.items)
    if isinstance(expr, Parallel):
        return any(_branch_has_block(branch) for branch in expr.branches)
    return False


def _render_parallel(branches):
    chars = charset.active()
    # The main line - the one drawn straight through, with the rest branching
    # off it - should carry the substance, so a branch holding a block goes
    # first and the plain contacts hang below it, the way the editor draws it.
    # A block buried in a lower branch reads as an indented afterthought. The
    # sort is stable, so branches keep their order otherwise.
    branches = sorted(branches, key=lambda branch: not _branch_has_block(branch))
    blocks = [_render(branch) for branch in branches]
    width = max(block.width for block in blocks)

    stacked = []
    connect_rows = []
    for block in blocks:
        connect_rows.append(len(stacked) + block.connect_row)
        for index, line in enumerate(block.lines):
            # The wire itself extends horizontally; everything else with
            # spaces, so short branches still reach the junction on the right.
            fill = chars["H"] if index == block.connect_row else " "
            stacked.append(line + fill * (width - len(line)))

    junctions = set(connect_rows)
    first, last = connect_rows[0], connect_rows[-1]

    lines = []
    for row, line in enumerate(stacked):
        if row == first:
            # The main line carries straight on and drops a branch downward.
            left, right = chars["T_DOWN"], chars["T_DOWN"]
        elif row == last:
            left, right = chars["BL"], chars["BR"]
        elif row in junctions:
            left, right = chars["T_RIGHT"], chars["T_LEFT"]
        elif first < row < last:
            left = right = chars["V"]
        else:
            left = right = " "
        lines.append(left + line + right)

    return Block(lines, first)


def _render(expr):
    chars = charset.active()
    if isinstance(expr, Empty):
        return Block(["   ", chars["H"] * 3], 1)
    if isinstance(expr, Element):
        return _render_element(expr)
    if isinstance(expr, Series):
        return _render_series(expr.items)
    if isinstance(expr, Parallel):
        return _render_parallel(expr.branches)
    raise TypeError("cannot render %r" % (expr,))


def _signature(expr):
    """A hashable structural fingerprint, so equal drawn elements can be spotted.

    Two elements with the same fingerprint render identically, which is what
    lets a shared prefix be pulled out of parallel branches without changing
    what any branch draws.
    """
    if isinstance(expr, Series):
        return ("series",) + tuple(_signature(item) for item in expr.items)
    if isinstance(expr, Parallel):
        return ("parallel",) + tuple(_signature(branch) for branch in expr.branches)
    if isinstance(expr, Element):
        return (
            "element", expr.kind, expr.label, expr.negated, expr.edge, expr.storage,
            expr.type_name, expr.instance_name, tuple(expr.input_pins), tuple(expr.output_pins),
            expr.active_output, expr.output_wired, expr.power_negated, expr.power_edge,
            tuple(sorted(expr.negated_outputs)), tuple(sorted(expr.stored_outputs.items())),
            tuple(expr.st_code), tuple(_signature(block) for block in expr.pin_blocks),
        )
    return ("empty",)


def _factor(expr):
    """Pull the leading elements shared by every parallel branch out in front.

    The parser builds one branch per sink, so a contact chain or a block that
    feeds several sinks is repeated in each branch - drawn again and again,
    which reads as separate rungs rather than one wire that branches. CODESYS
    draws the shared part once and splits after it; factoring the common
    prefix of the branches produces exactly that. Power flow is unchanged:
    "(P AND a) OR (P AND b)" and "P AND (a OR b)" drive the same rung.
    """
    if isinstance(expr, Series):
        return series([_factor(item) for item in expr.items])
    if isinstance(expr, Parallel):
        branches = [_factor(branch) for branch in expr.branches]

        def items_of(branch):
            return list(branch.items) if isinstance(branch, Series) else [branch]

        parts = [items_of(branch) for branch in branches]
        prefix = []
        while all(part for part in parts):
            first = parts[0][0]
            signature = _signature(first)
            if any(_signature(part[0]) != signature for part in parts):
                break
            prefix.append(first)
            parts = [part[1:] for part in parts]
        if not prefix:
            return parallel(branches)
        return series(prefix + [parallel([series(part) for part in parts])])
    return expr


def _pin_block_rungs(expr, found):
    """Collect the sub-rungs feeding side pins, in the order they execute.

    A box wired into another box's side pin is drawn on a wire of its own
    above the box that reads it, which names it in its pin caption. Deeper
    boxes come first, because that is the order the values are produced in.
    """
    if isinstance(expr, Series):
        for item in expr.items:
            _pin_block_rungs(item, found)
    elif isinstance(expr, Parallel):
        for branch in expr.branches:
            _pin_block_rungs(branch, found)
    elif isinstance(expr, Element):
        for pin_block in expr.pin_blocks:
            _pin_block_rungs(pin_block, found)
            found.append(pin_block)
    return found


def _render_wire(expr):
    """One wire between the rails."""
    chars = charset.active()
    block = _render(expr)
    lines = []
    for row, line in enumerate(block.lines):
        if row == block.connect_row:
            lines.append(chars["T_RIGHT"] + chars["H"] * 2 + line + chars["H"] * 2 + chars["T_LEFT"])
        else:
            lines.append(chars["V"] + "  " + line)
    return lines


def _block_prefix_key(rung):
    """The signature of a rung's head up to and including its first block.

    Two rungs with the same key begin with the same chain into the same box.
    A box read by several sinks is one box that runs once, so those rungs are
    the branches of one wire that splits after it; grouping them by this key
    lets the split be drawn once. A rung with no block returns None and is
    never merged - rungs that share only leading contacts may be separate
    rungs the editor keeps apart, and fusing them would misread the program.
    """
    items = rung.items if isinstance(rung, Series) else [rung]
    prefix = []
    for item in items:
        prefix.append(item)
        if isinstance(item, Element) and item.kind == BLOCK:
            return tuple(_signature(part) for part in prefix)
    return None


def _merge_rungs(rungs):
    """Combine rungs that split after a shared box into one branched rung.

    Rungs sharing a block are gathered into a Parallel, in the order they
    first appear; _factor then pulls the common head (the chain and the box)
    out in front so the box is drawn once and the readers branch off it.
    Everything else is left exactly as it was.
    """
    order = []
    groups = {}
    for rung in rungs:
        key = _block_prefix_key(rung)
        marker = key if key is not None else object()
        if marker not in groups:
            groups[marker] = []
            order.append(marker)
        groups[marker].append(rung)

    merged = []
    for marker in order:
        group = groups[marker]
        merged.append(group[0] if len(group) == 1 else parallel(group))
    return merged


def render_rung(expr):
    """Render one rung, bounded by the power rails.

    Boxes feeding side pins are drawn first, on wires of their own: the
    caption that reads one names only its output, so without the box the
    diagram would not say what feeds it. An EXECUTE box's inline ST is drawn
    inside the box, below its pins, by _render_block.
    """
    lines = []
    for pin_block in _pin_block_rungs(expr, []):
        lines.extend(_render_wire(pin_block))
    # Draw the shared head of parallel branches once, then the split - the way
    # the editor draws it - instead of repeating it down every branch.
    lines.extend(_render_wire(_factor(expr)))
    return lines


def render_declaration(pou):
    """The POU's declaration.

    Verbatim when CODESYS gave us the plaintext version, because that is the
    only form carrying comments, pragmas and attributes - and a pragma like
    {attribute 'qualified_only'} changes what the code means, so paraphrasing
    it away is worse than not showing it. Otherwise rebuilt from the
    structured interface, which is all older exports offer.
    """
    if pou.declaration_text:
        return pou.declaration_text.split("\n")

    # The rebuilt form is not what CODESYS holds: the structured interface has
    # nowhere to put a comment, a pragma or an attribute, and a variable whose
    # type the export omits comes back as UNKNOWN. The summary says how many
    # POUs this happened to; the file has to say that it is one of them.
    keyword = POU_TYPE_KEYWORDS.get(pou.pou_type, "PROGRAM")
    lines = [
        "(* Declaration rebuilt from the structured interface:"
        " comments, pragmas and attributes are missing; an omitted type reads UNKNOWN. *)",
        keyword + " " + pou.name,
    ]

    scope = None
    for variable in pou.variables:
        if variable.scope != scope:
            if scope is not None:
                lines.append("END_VAR")
            lines.append(variable.scope)
            scope = variable.scope
        entry = "    " + variable.name + " : " + variable.type_name
        if variable.initial_value is not None:
            entry += " := " + variable.initial_value
        lines.append(entry + ";")
    if scope is not None:
        lines.append("END_VAR")

    return lines


def render_pou(pou):
    """Render a whole POU: declaration, then the rungs of each network.

    A network can hold more than one rung - a block driving three outputs is
    one network in the editor - so the number belongs to the network, not to
    the rung.
    """
    lines = render_declaration(pou)
    lines.append("")

    if not pou.networks:
        lines.append("(* no rungs *)")

    for index, network in enumerate(pou.networks):
        lines.extend(network_headers(index + 1, network))
        for rung in _merge_rungs(network.outputs):
            lines.extend(render_rung(rung))
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()

    # Trailing whitespace is an artefact of grid composition, and the repo's
    # pre-commit hooks would strip it anyway.
    return [line.rstrip() for line in lines]
