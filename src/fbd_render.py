# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Render a parsed Function Block Diagram as ASCII boxes.

Layout is derived from the call tree, not from the exported coordinates. Each
block's inputs are rendered to its left and stacked vertically, so a pin fed
by another block gets that block's whole box beside it. Pin rows are placed at
whatever row their source ended up on, which keeps every wire horizontal.
"""

from __future__ import unicode_literals

import charset
from layout import Block, centred, stack
from ld_render import network_headers, render_declaration
from model import Assign, Call, Jump, Label, OutputRef, Signal


def _render_signal(node):
    return Block([node.text], 0)


def _render_label(node):
    # "NAME:" is how a label is written in ST, and how the ladder renderer
    # already draws one. Inside (* *) it reads as documentation, which is the
    # one thing a jump target is not.
    return Block([node.name + ":"], 0)


def _render_jump(node, drawn, subs=None):
    chars = charset.active()
    tail = chars["H"] * 3 + ">> " + (node.target or "?")
    if node.condition is None:
        return Block([tail], 0)
    source = _render(node.condition, drawn, subs)
    lines = source.padded(source.width)
    out = []
    for index, line in enumerate(lines):
        out.append(line + tail if index == source.connect_row else line)
    return Block(out, source.connect_row)


def _store_head(node):
    """The arrow head on a store: its set/reset marker, or its negation.

    A set or reset holds the target until the other one fires. Drawing it as
    a plain arrow says the store follows its input, which is the opposite.
    """
    if node.storage == "set":
        return "(S)> "
    if node.storage == "reset":
        return "(R)> "
    # The negation circle CODESYS draws on the pin, as an "o" on the wire.
    return "o> " if node.negated else "> "


def _render_assign(node, drawn, subs=None):
    chars = charset.active()
    source = _render(node.source, drawn, subs) if node.source is not None else Block([""], 0)
    lines = source.padded(source.width)
    head = _store_head(node)
    tail = chars["H"] * 3 + head + (node.label or "?")
    out = []
    for index, line in enumerate(lines):
        out.append(line + tail if index == source.connect_row else line)
    return Block(out, source.connect_row)


def _pin_arrow(box, pin):
    """The inline form, for a store on a pin that also feeds a wire onward."""
    storage = box.stored_outputs.get(pin)
    if storage == "set":
        return " =S> "
    if storage == "reset":
        return " =R> "
    return " =o> " if pin in box.negated_outputs else " => "


def _pin_head(box, pin):
    """The arrow head on a store written straight onto an output pin.

    The same heads a store on a wire uses: "o>" for the negation bubble,
    "(S)>" and "(R)>" for the set and reset a pin can carry.
    """
    storage = box.stored_outputs.get(pin)
    if storage == "set":
        return "(S)> "
    if storage == "reset":
        return "(R)> "
    return "o> " if pin in box.negated_outputs else "> "


def _is_wired(source):
    """False for a pin CODESYS exported with no source, or an empty expression.

    Those must not be drawn with a wire running off to the left, because there
    is nothing out there feeding them.
    """
    if source is None:
        return False
    return not (isinstance(source, Signal) and not source.label)


def _render_call(call, read_pin, drawn, subs=None):
    chars = charset.active()
    input_blocks = []
    for _pin, source in call.inputs:
        input_blocks.append(_render(source, drawn, subs) if source is not None else Block([""], 0))

    left_lines, pin_rows = stack(input_blocks)
    # A minimum lead-in, so a source exactly as wide as the column still shows
    # a wire and back-to-back boxes do not fuse into one run of borders.
    left_width = (max([len(line) for line in left_lines]) + 2) if left_lines else 0

    # Only the rows where a source hands off to a pin get their wire extended;
    # a nested box's own internal wires already end at that box's edge.
    handoff = set()
    for index, pin_and_source in enumerate(call.inputs):
        if _is_wired(pin_and_source[1]):
            handoff.add(pin_rows[index])

    left = []
    for index, line in enumerate(left_lines):
        fill = chars["H"] if index in handoff else " "
        left.append(line + fill * (left_width - len(line)))

    input_rows = list(pin_rows)
    output_rows = []
    for index in range(len(call.outputs)):
        if index < len(input_rows):
            output_rows.append(input_rows[index])
        else:
            # More outputs than inputs: the surplus hangs below the last pin.
            base = input_rows[-1] if input_rows else -1
            output_rows.append(base + index - len(input_rows) + 1)

    all_rows = (input_rows + output_rows) or [0]
    box_first, box_last = min(all_rows), max(all_rows)

    # The title and top border sit two rows above the first pin, so everything
    # shifts down if the first pin would land at the very top of the grid.
    shift = max(0, 2 - box_first)
    if shift:
        left = [" " * left_width] * shift + left
        input_rows = [row + shift for row in input_rows]
        output_rows = [row + shift for row in output_rows]
        box_first += shift
        box_last += shift

    in_at = {}
    for index, pin_and_source in enumerate(call.inputs):
        in_at[input_rows[index]] = pin_and_source[0] or "?"

    # A store written on an output pin hangs off that pin on a wire of its
    # own, the way CODESYS draws it. Writing it inside the box put the target
    # variable in among the pin names, where it reads as another pin.
    out_at = {}
    tail_at = {}
    for index, pin_and_assignment in enumerate(call.outputs):
        pin, assigned = pin_and_assignment
        text = pin or "?"
        if assigned and pin not in call.wired_outputs:
            tail_at[output_rows[index]] = chars["H"] * 3 + _pin_head(call, pin) + assigned
        elif assigned:
            # The pin already carries a wire onward; a second thing hung off
            # the same row would cross it.
            text += _pin_arrow(call, pin) + assigned
        elif pin in call.negated_outputs:
            text += " o"
        out_at[output_rows[index]] = text

    title = call.title
    widths = [len(title)]
    for row in range(box_first, box_last + 1):
        widths.append(len(in_at.get(row, "")) + 3 + len(out_at.get(row, "")))
    inner = max(widths)

    height = max(len(left), box_last + 2)
    left += [" " * left_width] * (height - len(left))

    # handoff was computed before the shift; recompute against the final rows.
    handoff_pins = set()
    for index, pin_and_source in enumerate(call.inputs):
        if _is_wired(pin_and_source[1]):
            handoff_pins.add(input_rows[index])

    # An output pin only breaks the box wall with a tee if a consumer is
    # actually there to receive it - and a box read through two pins breaks
    # it twice.
    pins = [pin for pin, _assigned in call.outputs]
    live_output_rows = set()
    for pin in call.wired_outputs:
        if pin in pins:
            live_output_rows.add(output_rows[pins.index(pin)])

    lines = []
    for row in range(height):
        if row == box_first - 2:
            box = centred(title, inner + 2)
        elif row == box_first - 1:
            box = chars["TL"] + chars["H"] * inner + chars["TR"]
        elif row == box_last + 1:
            box = chars["BL"] + chars["H"] * inner + chars["BR"]
        elif box_first <= row <= box_last:
            left_pin = in_at.get(row, "")
            right_pin = out_at.get(row, "")
            left_edge = chars["PIN_L"] if row in handoff_pins else chars["V"]
            wired_out = row in live_output_rows or row in tail_at
            right_edge = chars["PIN_R"] if wired_out else chars["V"]
            gap = inner - len(left_pin) - len(right_pin)
            box = left_edge + left_pin + " " * gap + right_pin + right_edge + tail_at.get(row, "")
        else:
            box = " " * (inner + 2)
        lines.append(left[row] + box)

    # The wire leaves on whichever output pin this consumer asked for.
    pin_rows = {}
    for index, pin in enumerate(pins):
        pin_rows[pin] = output_rows[index]

    wanted = read_pin if read_pin is not None else call.active_output
    connect_row = box_first
    if wanted in pin_rows:
        connect_row = pin_rows[wanted]
    elif output_rows:
        connect_row = output_rows[0]

    return Block(lines, connect_row, pin_rows)


def _reference(call, pin):
    """The name of a box already drawn in this network, on the pin being read.

    Only an instance can be referred to this way: an operator has no name to
    print, and being stateless it costs nothing to draw again.
    """
    if not call.instance_name:
        return None
    text = call.instance_name + "." + pin if pin else call.instance_name
    if pin in call.negated_outputs:
        text = "NOT " + text
    return text


# Stands in for a shared box while the branch that reads it is drawn, so the
# row the wire arrives on can be found once the branch has been composed.
# Composition is text, so a marker in the text is the cheapest way to carry a
# position through it, and it never survives into the output. One marker per
# pin, so a branch that reads two pins can say which wire arrives where. They
# are control characters, skipping the ones str.strip and str.split treat as
# whitespace, because a line ending in one is stripped like any other.
MARKERS = [chr(code) for code in list(range(1, 9)) + list(range(14, 28))]


class _Shared(object):
    """The box a network is joined around, while its readers are composed.

    ``pins`` names the pins a reader may take a wire from; None allows any.
    A read of any other pin falls back to naming the box in text, the way a
    box already drawn is named, and so does a read once the markers run out.
    """

    def __init__(self, call, pins=None):
        self.call = call
        self.pins = pins
        self.markers = {}

    def marker(self, pin):
        """The stand-in for a wire from ``pin``, or None to name it instead."""
        if self.pins is not None and pin not in self.pins:
            return None
        if pin not in self.markers:
            if len(self.markers) >= len(MARKERS):
                return None
            self.markers[pin] = MARKERS[len(self.markers)]
        return self.markers[pin]


def _render(node, drawn, subs=None):
    """Draw one tree. ``drawn`` holds the boxes this network has already shown.

    A block read by two of the network's outputs is one block that runs once.
    Where both readers hang straight off it the fan-out draws it once and
    branches, but a reader sitting behind another box is a tree of its own,
    and drawing that tree from scratch put a second copy of the same instance
    on the page - two timers where the program has one. The first tree to
    reach a box draws it; the rest name the pin they read, exactly as the
    ladder renderer does.
    """
    call = node.call if isinstance(node, OutputRef) else node
    if isinstance(call, Call):
        pin = node.pin if isinstance(node, OutputRef) else call.active_output
        if subs is not None and subs.call is call:
            # Drawn once already, on the left of this branch; the wire into it
            # comes from the junction rather than from another copy of the box.
            marker = subs.marker(pin)
            if marker is not None:
                return Block([marker], 0)
        if id(call) in drawn:
            reference = _reference(call, pin)
            if reference is not None:
                return Block([reference], 0)
        else:
            drawn.add(id(call))
        return _render_call(call, pin, drawn, subs)
    if isinstance(node, Assign):
        return _render_assign(node, drawn, subs)
    if isinstance(node, Jump):
        return _render_jump(node, drawn, subs)
    if isinstance(node, Label):
        return _render_label(node)
    if isinstance(node, Signal):
        return _render_signal(node)
    raise TypeError("cannot render %r" % (node,))


def _assign_tail(node):
    chars = charset.active()
    head = "o " if node.negated and not node.storage else _store_head(node)
    return chars["H"] * 2 + head + (node.label or "?")


def _fanout_groups(source, outputs):
    """[(rows, outputs)] - one group per output pin that is read.

    Outputs reading the same pin share one wire and are branched off it, so
    they stack on consecutive rows under that pin. Outputs reading different
    pins do not share anything: each leaves the box on its own pin's row, and
    joining them into one junction column would draw two signals as one.
    """
    order = []
    at_pin = {}
    for output in outputs:
        pin = output.source.pin if isinstance(output.source, OutputRef) else None
        if pin not in at_pin:
            at_pin[pin] = []
            order.append(pin)
        at_pin[pin].append(output)
    order.sort(key=lambda pin: source.pin_rows.get(pin, source.connect_row))

    groups = []
    taken = set()
    for pin in order:
        rows = []
        row = source.pin_rows.get(pin, source.connect_row)
        for output in at_pin[pin]:
            while row in taken:
                row += 1
            taken.add(row)
            rows.append(row)
            row += 1
        groups.append((rows, at_pin[pin]))
    return groups


def _render_fanout(outputs, drawn):
    """One source driving several outputs: draw it once and branch.

    This is how CODESYS shows it, and drawing the box once per output would
    both misrepresent the program and double the width of the diff.
    """
    chars = charset.active()
    source = _render(outputs[0].source, drawn)
    # A short lead before the junction, so the branch is not welded to the box
    # edge. padded() extends the wire row and pads the rest with spaces.
    width = source.width + 2
    groups = _fanout_groups(source, outputs)

    tails = {}
    joints = {}
    verticals = set()
    for rows, group in groups:
        for row, output in zip(rows, group):
            tails[row] = output
        if len(rows) == 1:
            joints[rows[0]] = chars["H"]
            continue
        # One wire, branched: the junction column belongs to this pin alone.
        joints[rows[0]] = chars["T_DOWN"]
        joints[rows[-1]] = chars["BL"]
        for row in rows[1:-1]:
            joints[row] = chars["T_RIGHT"]
        for row in range(rows[0] + 1, rows[-1]):
            verticals.add(row)

    # Only the row a wire actually leaves the box on is extended to the
    # junction; the rows below it are carried by the junction column.
    lines = source.padded(width, wire_rows=set(rows[0] for rows, _group in groups))

    last = max(tails)
    while len(lines) <= last:
        lines.append(" " * width)

    out = []
    for row, line in enumerate(lines):
        joint = joints.get(row, chars["V"] if row in verticals else " ")
        tail = _assign_tail(tails[row]) if row in tails else ""
        out.append(line + joint + tail)

    return Block(out, min(tails))


def _shared_source(outputs):
    """The single source every output hangs off, or None.

    Identity, not equality: the parser memoises shared nodes, so two outputs
    fed by one block hold the very same object - through an OutputRef each
    when they read different pins of it.
    """
    if len(outputs) < 2:
        return None
    if not all(isinstance(output, Assign) for output in outputs):
        return None
    sources = [output.source for output in outputs]
    if sources[0] is None:
        return None
    boxes = [source.call if isinstance(source, OutputRef) else source for source in sources]
    return sources[0] if all(box is boxes[0] for box in boxes) else None


def _shared_call(outputs):
    """The one box this network reads from more than one place, or None.

    A box read twice is one box that runs once, and the second reader is a
    branch off its pin - not a second copy, and not a name in text. Only an
    instance qualifies: an operator has no name, no state, and nothing is
    gained by joining two copies of it.

    More than one shared box in a network needs a real two-dimensional
    layout, which this renderer does not have; those fall back to naming the
    box, which is wrong-looking but never wrong.
    """
    counts = {}
    order = []

    def walk(node):
        call = node.call if isinstance(node, OutputRef) else node
        if isinstance(call, Call):
            if id(call) in counts:
                counts[id(call)] += 1
                return
            counts[id(call)] = 1
            order.append(call)
            for _pin, source in call.inputs:
                if source is not None:
                    walk(source)
        elif isinstance(node, Assign):
            if node.source is not None:
                walk(node.source)
        elif isinstance(node, Jump):
            if node.condition is not None:
                walk(node.condition)

    for tree in outputs:
        walk(tree)

    shared = [call for call in order if counts[id(call)] > 1 and call.instance_name]
    return shared[0] if len(shared) == 1 else None


def _entry_rows(block, shared):
    """[(row, pin)] for every wire into the shared box, in row order.

    Each marker is replaced by a piece of wire, so the branch's own lead-in
    joins up with the junction it is placed against.
    """
    chars = charset.active()
    entries = []
    for row, line in enumerate(block.lines):
        for pin, marker in shared.markers.items():
            if marker in line:
                line = line.replace(marker, chars["H"])
                entries.append((row, pin))
        block.lines[row] = line
    entries.sort(key=lambda entry: entry[0])
    return entries


def _reads_pins(tree, call):
    """The pins a tree reads ``call`` through, in the order it meets them."""
    found = []

    def walk(node):
        inner = node.call if isinstance(node, OutputRef) else node
        if inner is call:
            pin = node.pin if isinstance(node, OutputRef) else call.active_output
            if pin not in found:
                found.append(pin)
            return
        if isinstance(inner, Call):
            for _pin, source in inner.inputs:
                if source is not None:
                    walk(source)
        elif isinstance(node, Assign):
            if node.source is not None:
                walk(node.source)
        elif isinstance(node, Jump):
            if node.condition is not None:
                walk(node.condition)

    walk(tree)
    return found


def _split_readers(outputs, call):
    """([(tree, pins)], [tree]) - the outputs that read the shared box, and the rest."""
    readers = []
    others = []
    for tree in outputs:
        pins = _reads_pins(tree, call)
        if pins:
            readers.append((tree, pins))
        else:
            others.append(tree)
    return readers, others


def _place_branches(branches, pin_rows, default_row):
    """{index: top row} for each composed branch.

    Branches are taken pin by pin down the box, and stacked so no two overlap:
    the first reader of a pin sits level with the pin, and each later one goes
    under whatever came before it. A branch that reads several pins is placed
    by its topmost pin, and last among that pin's readers - the one position
    from which its other wires can arrive without crossing anything.
    """

    def row_of(pin):
        return pin_rows.get(pin, default_row)

    top_pin = []
    for _block, entries in branches:
        top_pin.append(min(entries, key=lambda entry: (row_of(entry[1]), entry[0]))[1])

    order = []
    for pin in sorted(set(top_pin), key=row_of):
        group = [index for index, read in enumerate(top_pin) if read == pin]
        group.sort(key=lambda index: len(set(read for _row, read in branches[index][1])) > 1)
        order.extend(group)

    tops = {}
    next_top = None
    for index in order:
        block, entries = branches[index]
        entry = min([row for row, read in entries if read == top_pin[index]])
        wanted = row_of(top_pin[index]) - entry
        tops[index] = wanted if next_top is None else max(wanted, next_top)
        next_top = tops[index] + len(block.lines)
    return tops


def _reader_rows(branches, tops):
    """{pin: [row]} - the rows the wires from each pin arrive on, in order."""
    rows = {}
    for index, block_and_entries in enumerate(branches):
        for row, pin in block_and_entries[1]:
            rows.setdefault(pin, []).append(tops[index] + row)
    for pin in rows:
        rows[pin].sort()
    return rows


def _junction(row, position, columns, reader_rows, row_of):
    """One cell of the junction columns between a shared box and its readers.

    Each pin that is read has a column of its own, the lowest pin's nearest
    the box. A column carries the pin's wire down from the pin's row to the
    last reader of it, breaking out to each reader on the way. Every other
    cell is a wire passing through - on its way out to a column further from
    the box, or in from one nearer it to a reader - or nothing.
    """
    chars = charset.active()
    pin = columns[position]
    pin_row = row_of(pin)
    rows = reader_rows[pin]
    if row == pin_row:
        if rows[0] != pin_row:
            return chars["TR"]
        return chars["T_DOWN"] if len(rows) > 1 else chars["H"]
    if row in rows:
        return chars["BL"] if row == rows[-1] else chars["T_RIGHT"]
    if pin_row < row < rows[-1]:
        return chars["V"]
    for other, other_pin in enumerate(columns):
        if other > position and row == row_of(other_pin):
            return chars["H"]
        if other < position and row in reader_rows[other_pin]:
            return chars["H"]
    return " "


def _compose_branches(readers, call, drawn, every_pin):
    """[(block, entries)] - each reader drawn on its own, its wires marked.

    With ``every_pin`` each read of the shared box becomes a wire; without
    it only the first pin a reader takes is wired and the rest are named in
    text, the way a box already drawn is named.
    """
    branches = []
    for tree, pins in readers:
        shared = _Shared(call, None if every_pin else pins[:1])
        block = _render(tree, drawn, shared)
        branches.append((block, _entry_rows(block, shared)))
    return branches


def _wires_cross(branches, tops, pin_rows, default_row):
    """True when the placed branches cannot be wired without a crossing.

    A pin's column runs from the pin's row down to the last reader of it,
    and a lower pin's column sits inside a higher pin's. Every wire is then
    clear of every column it passes only if each pin's readers all sit below
    every reader of the pins above it, and none sits above its own pin.
    """

    def row_of(pin):
        return pin_rows.get(pin, default_row)

    reader_rows = _reader_rows(branches, tops)
    last = None
    for pin in sorted(reader_rows, key=row_of):
        rows = reader_rows[pin]
        if rows[0] < row_of(pin):
            return True
        if last is not None and rows[0] <= last:
            return True
        last = rows[-1]
    return False


def _render_joined(readers, call, drawn):
    """Draw a shared box once and branch its readers off the pins they read.

    The box goes on the left; each reader is composed on its own to the right
    of it and hangs off a junction column, level with the row its wire leaves
    the box on. Readers of one pin share a column, which is what the editor
    draws; readers of different pins get a column each, because joining two
    pins into one column draws two signals as one.

    A reader that takes two pins from the box gets two wires, unless the
    wires would then have to cross: then it keeps the wire from the first
    pin it reads and names the other in text, which is wrong-looking but
    never wrong.
    """
    chars = charset.active()
    drawn.add(id(call))
    source = _render_call(call, None, set())
    default_row = source.connect_row

    for every_pin in (True, False):
        shown = set(drawn)
        branches = _compose_branches(readers, call, shown, every_pin)
        tops = _place_branches(branches, source.pin_rows, default_row)
        if not every_pin or not _wires_cross(branches, tops, source.pin_rows, default_row):
            break
    drawn.update(shown)

    shift = -min([top for top in tops.values()] + [0])
    for index in tops:
        tops[index] += shift

    def row_of(pin):
        return source.pin_rows.get(pin, default_row) + shift

    reader_rows = _reader_rows(branches, tops)
    # Inner to outer: the lowest pin nearest the box, so that no column has
    # to be crossed by a wire leaving the box above it.
    columns = sorted(reader_rows, key=row_of, reverse=True)
    leaves = set(row_of(pin) for pin in columns)

    lines = [" " * source.width] * shift + list(source.lines)
    height = max([len(lines)] + [tops[index] + len(block.lines) for index, (block, _entries) in enumerate(branches)])

    # The wire leaves the box once per pin that is read; everything below that
    # is carried by the junction column, so only a pin's own row is filled
    # across to it. Filling every reader row drew a wire out of the box's
    # bottom border.
    width = source.width + 2
    out = []
    for row in range(height):
        line = lines[row] if row < len(lines) else ""
        line += (chars["H"] if row in leaves else " ") * (width - len(line))
        for position in range(len(columns)):
            line += _junction(row, position, columns, reader_rows, row_of)
        tail = ""
        for index, block_and_entries in enumerate(branches):
            block = block_and_entries[0]
            if tops[index] <= row < tops[index] + len(block.lines):
                tail = block.lines[row - tops[index]]
                break
        out.append((line + tail).rstrip())
    return out


def _execute_bodies(outputs):
    """The inline ST of every EXECUTE box in a network, laid out for the page.

    Each body once, in the order the boxes are met - a box behind another
    runs first, so its body comes first.
    """
    seen = set()
    found = []

    def walk(node):
        call = node.call if isinstance(node, OutputRef) else node
        if isinstance(call, Call):
            if id(call) in seen:
                return
            seen.add(id(call))
            for _pin, source in call.inputs:
                if source is not None:
                    walk(source)
            if call.st_code:
                found.append(call)
        elif isinstance(node, Assign):
            if node.source is not None:
                walk(node.source)
        elif isinstance(node, Jump):
            if node.condition is not None:
                walk(node.condition)

    for tree in outputs:
        walk(tree)

    lines = []
    for call in found:
        lines.append("")
        lines.extend("    " + line for line in call.st_code)
    return lines


def _render_outputs(outputs, drawn):
    """The diagram of one network's outputs, joined or branched as they share."""
    if _shared_source(outputs) is not None:
        return _render_fanout(outputs, drawn).lines

    shared = _shared_call(outputs)
    if shared is not None:
        readers, others = _split_readers(outputs, shared)
        lines = _render_joined(readers, shared, drawn)
        # An output that reads nothing from the shared box is a drawing of its
        # own, and goes below the joined one rather than into its columns.
        for tree in others:
            lines.extend(_render(tree, drawn).lines)
        return lines

    lines = []
    for tree in outputs:
        lines.extend(_render(tree, drawn).lines)
    return lines


def render_network(network):
    """Render one network, which may drive several outputs from one source."""
    outputs = getattr(network, "outputs", [network])
    # Per network: a box drawn for one output must not be drawn again for the
    # next, but a box shared between two networks is two boxes on the page.
    drawn = set()
    # An EXECUTE box's body is the logic; drawing the box without it would be
    # an empty rectangle where a dozen lines of ST should be. The box is found
    # wherever it sits - behind the store its ENO feeds, or behind another
    # box - and not only when it is the network's own output.
    return _render_outputs(outputs, drawn) + _execute_bodies(outputs)


def render_pou(pou):
    """Render a whole FBD POU: declaration, then one box tree per network."""
    lines = render_declaration(pou)
    lines.append("")

    if not pou.networks:
        lines.append("(* no networks *)")

    for index, network in enumerate(pou.networks):
        lines.extend(network_headers(index + 1, network))
        lines.extend(render_network(network))
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()

    return [line.rstrip() for line in lines]
