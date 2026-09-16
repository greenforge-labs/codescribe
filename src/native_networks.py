# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Number the rendered networks the way the CODESYS editor numbers them.

The rendering is derived from a PLCopen export, but PLCopen is not what a
reviewer holds next to it - the native xml is, and the two disagree about
what a network is. CODESYS omits from PLCopen every network that carries no
elements: an out-commented one (Toggle Network Comment State) goes entirely,
comment included, and so does an empty one. Numbering what survives 1..n
therefore drifts from what the editor shows, silently, and a reviewer opening
"Network 5" in CODESYS reads different logic under "(* Network 5 *)".

The native export, which codescribe writes immediately before rendering,
carries the full list: every network in editor order with its out-commented
flag, its comment, its title, its label and its items. That list is the
authority for the *structure* - how many networks there are, in what order,
and what each is called. PLCopen supplies only the logic, and the two are
joined by matching networks that carry logic, in order.

That is the whole of the alignment, and it is deliberately not a positional
match over both lists. Matching position for position means guessing which
side an absent network belongs to, and getting it wrong silently; matching
only the networks that both sides agree exist leaves nothing to guess.

The native format is proprietary and undocumented, so everything here is
best-effort: any surprise degrades to None and the caller falls back to
sequential numbering, saying so in the file.
"""

import os

from model import Network
import plcopen
import xmlbackend

# Said in the file itself, under the number the network occupies. A reviewer
# reading only the .txt has to learn that logic exists here without
# executing, which is the fact the silent drop hid.
NOTE_OUT_COMMENTED = "out-commented in CODESYS - does not execute; diagram not exported, see the native xml"
NOTE_EMPTY = "empty network"


class NativeNetwork(object):
    """One network as the native export records it."""

    def __init__(self, out_commented=False, empty=False, comment="", title="", label=""):
        self.out_commented = out_commented
        self.empty = empty
        self.comment = comment
        self.title = title
        # The jump-target label CODESYS stores on the network itself. The
        # parser lifts the free-standing element PLCopen writes into the
        # network it precedes; this one is the editor's own, and is taken
        # in preference.
        self.label = label

    @property
    def has_logic(self):
        """True when this network has a body PLCopen would have exported."""
        return not self.out_commented and not self.empty

    def __repr__(self):
        return "NativeNetwork(out_commented=%r, empty=%r, comment=%r, title=%r, label=%r)" % (
            self.out_commented,
            self.empty,
            self.comment,
            self.title,
            self.label,
        )


def read_networks(path):
    """[NativeNetwork] in editor order, or None if the file yields none.

    Networks live under <List2 Name="NetworkList">; each entry carries its
    flags as <Single Name="..."> children. Entries without an OutCommented
    flag are not networks and are skipped. None rather than [] on any
    trouble: the caller treats None as "no authority available" and keeps the
    sequential numbering.
    """
    try:
        if not os.path.exists(path):
            return None
        root = xmlbackend.parse(plcopen.read_document(path))
    except Exception:
        return None

    networks = []
    for elem in root.iter():
        if plcopen.tag(elem) != "List2" or elem.get("Name") != "NetworkList":
            continue
        for net in elem:
            out_commented = None
            comment = ""
            title = ""
            label = ""
            items_elem = None
            for child in net:
                tag_name, name = plcopen.tag(child), child.get("Name")
                if tag_name == "Single" and name == "OutCommented":
                    out_commented = (child.text or "").strip() == "True"
                elif tag_name == "Single" and name == "Comment":
                    comment = (child.text or "").strip()
                elif tag_name == "Single" and name == "Title":
                    title = (child.text or "").strip()
                elif tag_name == "Single" and name == "Label":
                    label = (child.text or "").strip()
                elif tag_name == "List2" and name == "NetworkItems":
                    items_elem = child
            if out_commented is None:
                continue
            # The .NET element wrapper has no __len__, so emptiness is probed
            # by iterating.
            empty = items_elem is None or not any(True for _ in items_elem)
            networks.append(
                NativeNetwork(out_commented=out_commented, empty=empty, comment=comment, title=title, label=label)
            )
    return networks or None


def _carries_logic(network):
    """True for a parsed network that PLCopen exported a body for.

    A network the parser built from a comment element alone has no outputs,
    and neither has one built from a jump label alone: the parser lifts the
    label onto the network, where CODESYS keeps it. Neither is something the
    native list has a body for, so neither takes part in the match.
    """
    return bool(getattr(network, "outputs", []))


def align(native, parsed):
    """[Network] numbered as the editor numbers them, or None.

    One entry per native network, in editor order, carrying that network's
    own comment, title and label. The networks that carry logic take their
    bodies from the parsed list in order; the rest render as a placeholder
    saying why they have none.

    None when the two disagree about how many networks carry logic. That
    means an assumption broke - a body split in two, or a CODESYS that does
    export out-commented networks after all - and misnumbering silently is
    worse than saying so.
    """
    if not native:
        return None

    bodies = [network for network in parsed if _carries_logic(network)]
    if len(bodies) != len([network for network in native if network.has_logic]):
        return None

    aligned = []
    index = 0
    for entry in native:
        outputs = []
        note = None
        if entry.has_logic:
            outputs = bodies[index].outputs
            index += 1
        elif entry.out_commented:
            note = NOTE_OUT_COMMENTED
        else:
            note = NOTE_EMPTY
        aligned.append(Network(comment=entry.comment, outputs=outputs, title=entry.title, label=entry.label, note=note))
    return aligned
