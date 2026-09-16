# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Text-grid composition shared by the graphical renderers.

A Block is a rectangle of text plus the row its wire enters and leaves on.
Renderers build small Blocks for leaves and compose them; nothing else needs
to know about absolute coordinates.
"""

from __future__ import unicode_literals

import charset


class Block(object):
    def __init__(self, lines, connect_row, pin_rows=None, sink_rows=None):
        self.lines = lines
        self.connect_row = connect_row
        # For a box: the row each output pin sits on, so a caller branching
        # several wires off it can leave each one level with the pin it
        # reads instead of guessing.
        self.pin_rows = pin_rows if pin_rows is not None else {}
        # Rows that end in a coil, a return or another sink and so run to the
        # right power rail on their own, rather than merging back into one
        # wire. Two coils off one contact are two rung ends, not a loop.
        self.sink_rows = set(sink_rows) if sink_rows is not None else set()

    @property
    def width(self):
        if not self.lines:
            return 0
        return max(len(line) for line in self.lines)

    def padded(self, width, wire_rows=None, fill=None):
        """Lines padded to ``width``, extending wires horizontally.

        Rows listed in ``wire_rows`` (defaulting to this Block's own connect
        row) are filled with the wire character so a short branch still reaches
        the junction on its right. Every other row is filled with spaces.
        """
        if wire_rows is None:
            wire_rows = set([self.connect_row])
        if fill is None:
            fill = charset.active()["H"]
        out = []
        for index, line in enumerate(self.lines):
            out.append(line + (fill if index in wire_rows else " ") * (width - len(line)))
        return out


def centred(text, width):
    """``text`` centred in ``width``, with any odd space on the right.

    str.center splits an odd remainder the other way round under IronPython
    2.7 than under CPython 3, so a file rendered inside CODESYS and the same
    file rendered by the dev CLI differ by one column on any box whose title
    needs odd padding. Doing the arithmetic here settles it: the left padding
    is the floor, which is what CODESYS itself produces.
    """
    if width <= len(text):
        return text
    lead = (width - len(text)) // 2
    return " " * lead + text + " " * (width - len(text) - lead)


def stack(blocks):
    """Stack Blocks vertically. Returns (lines, absolute connect rows)."""
    lines = []
    connect_rows = []
    for block in blocks:
        connect_rows.append(len(lines) + block.connect_row)
        lines.extend(block.lines)
    return lines, connect_rows
