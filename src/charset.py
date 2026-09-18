# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Drawing characters for the graphical renderers.

The glyphs are written as \\u escapes rather than literal box-drawing
characters on purpose: CODESYS runs these scripts under IronPython 2.7, which
enforces PEP 263 and refuses to load a source file containing a non-ASCII byte
without an encoding declaration. Escapes keep the source pure ASCII while the
output is Unicode.

The rendered text is written as UTF-8, matching the .st files CODESCRIBE
already exports.

An ASCII set is kept alongside for terminals, diff viewers and pasted-into-
email situations where box drawing turns to mojibake.
"""

from __future__ import unicode_literals

UNICODE = {
    "H": "\u2500",  # horizontal wire
    "V": "\u2502",  # vertical wire
    "TL": "\u250c",  # box corners
    "TR": "\u2510",
    "BL": "\u2514",
    "BR": "\u2518",
    "T_DOWN": "\u252c",  # branch leaves downward
    "T_UP": "\u2534",
    "T_RIGHT": "\u251c",  # wire joins and continues right
    "T_LEFT": "\u2524",  # wire arrives from the left
    # A ladder contact is a pair of bars the wire runs between.
    "CONTACT_L": "\u2524",
    "CONTACT_R": "\u251c",
    # Box edges at a pin: the tee marks a real connection, so an unwired pin
    # stays a plain wall and is visibly different.
    "PIN_L": "\u2524",
    "PIN_R": "\u251c",
}

ASCII = {
    "H": "-",
    "V": "|",
    "TL": "+",
    "TR": "+",
    "BL": "+",
    "BR": "+",
    "T_DOWN": "+",
    "T_UP": "+",
    "T_RIGHT": "+",
    "T_LEFT": "+",
    "CONTACT_L": "|",
    "CONTACT_R": "|",
    "PIN_L": "|",
    "PIN_R": "|",
}

SETS = {"unicode": UNICODE, "ascii": ASCII}

_active = UNICODE


def use(name):
    """Select the character set by name. Returns the set now in use."""
    global _active
    if name not in SETS:
        raise ValueError("unknown charset %r, expected one of %s" % (name, ", ".join(sorted(SETS))))
    _active = SETS[name]
    return _active


def active():
    return _active
