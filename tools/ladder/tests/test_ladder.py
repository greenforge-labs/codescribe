# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Tests for the Ladder Diagram renderer.

Written as a plain script rather than pytest, matching tools/ci/, so it runs
under both Python 3 and the IronPython 2.7 that CODESYS embeds. The renderer
is destined for src/ once it is proven, and it has to pass there too.

    python tools/ladder/tests/test_ladder.py
"""

from __future__ import print_function, unicode_literals

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The renderers live in src/ so CODESYS can load them; tools/ladder keeps only
# the dev CLI and these tests.
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "src"))
sys.path.insert(0, os.path.join(HERE, ".."))

import charset  # noqa: E402
from ld_render import render_declaration, render_pou  # noqa: E402
from model import COIL, CONTACT, LABEL, Element, Parallel, Series  # noqa: E402
from parse_ld import parse_pous  # noqa: E402
from render import write  # noqa: E402

FIXTURES = os.path.join(HERE, "fixtures")
SOURCE = os.path.join(FIXTURES, "motor_control.plcopen.xml")
EXPECTED = os.path.join(FIXTURES, "motor_control.expected.txt")

failures = []


def check(name, condition, detail=""):
    if condition:
        print("OK      " + name)
        return
    failures.append(name)
    # The detail quotes rendered lines, which hold box-drawing characters a
    # Windows console cannot encode. print() raises UnicodeEncodeError on
    # exactly those, which aborts the run at the first golden mismatch - so
    # the failures after it are never reported and the suite looks shorter
    # than it is rather than looking broken.
    sys.stdout.flush()
    write(["FAIL    " + name + ((": " + detail) if detail else "")])


def check_equal(name, actual, expected):
    check(name, actual == expected, "expected %r, got %r" % (expected, actual))


# --- parsing ---------------------------------------------------------------

pous = parse_pous(SOURCE)

check_equal("one LD pou is found", len(pous), 1)

pou = pous[0]
check_equal("pou name", pou.name, "Motor_Control")
check_equal("pou type", pou.pou_type, "program")
check_equal("interface variables", len(pou.variables), 8)
check_equal("derived type resolves to its name", pou.variables[-1].type_name, "TON")
check_equal("initial value is captured", pou.variables[2].initial_value, "FALSE")

check_equal("three rungs", len(pou.rungs), 3)

# Network 1: (Start_PB OR Motor_Run) AND NOT Stop_PB -> Motor_Run
rung1 = pou.rungs[0]
check("rung 1 is a series", isinstance(rung1, Series))
check_equal("rung 1 has three stages", len(rung1.items), 3)
check("rung 1 opens with a parallel branch", isinstance(rung1.items[0], Parallel))
check_equal("seal-in has two branches", len(rung1.items[0].branches), 2)
check_equal("first branch is Start_PB", rung1.items[0].branches[0].label, "Start_PB")
check_equal("second branch is Motor_Run", rung1.items[0].branches[1].label, "Motor_Run")
check("Stop_PB is negated", rung1.items[1].negated)
check_equal("Stop_PB is a contact", rung1.items[1].kind, CONTACT)
check_equal("rung 1 terminates in a coil", rung1.items[2].kind, COIL)
check_equal("coil drives Motor_Run", rung1.items[2].label, "Motor_Run")

# The right power rail anchors the rung but must not become a drawn element.
check(
    "right power rail is not drawn",
    all(not (isinstance(i, Element) and i.kind.endswith("PowerRail")) for i in rung1.items),
)

# Network 2: rising edge into a set coil
rung2 = pou.rungs[1]
check_equal("rising edge is captured", rung2.items[0].edge, "rising")
check_equal("set coil storage", rung2.items[1].storage, "set")

# Network 3: terminal is the coil itself, with no right power rail
rung3 = pou.rungs[2]
check_equal("rung 3 has three stages", len(rung3.items), 3)
check_equal("reset coil storage", rung3.items[2].storage, "reset")

# --- layout independence ---------------------------------------------------

handle = io.open(SOURCE, encoding="utf-8")
try:
    source_text = handle.read()
finally:
    handle.close()

# Shifting every element 500px right must not change a single character of
# output. This is the property that keeps diffs meaningful.
moved = source_text.replace('<position x="', '<position x="9')
# If the fixture is ever regenerated with different attribute order or
# quoting, the replace would match nothing and this check would degenerate to
# comparing a render with itself - green forever, proving nothing.
check("the x shift touched the fixture", moved != source_text)
moved_pou = None
try:
    import io

    # Bytes, not text: the fixture carries an encoding declaration, which
    # ElementTree refuses to parse from an already-decoded stream.
    moved_pou = parse_pous(io.BytesIO(moved.encode("utf-8")))[0]
except Exception as error:  # pragma: no cover - diagnostic path
    check("moved fixture parses", False, repr(error))

if moved_pou is not None:
    check_equal("x shifts do not affect output", render_pou(moved_pou), render_pou(pou))

# The same must hold vertically - a renderer that started ordering rungs by y
# coordinate would break the promise while the x-only check stayed green.
# Only the first few positions are shifted: a uniform prefix is
# order-preserving, so shifting everything could never catch a renderer that
# sorts by coordinate - scrambling relative order is what makes this bite.
moved_down = source_text.replace('" y="', '" y="9', 3)
check("the y shift touched the fixture", moved_down != source_text)
try:
    moved_down_pou = parse_pous(io.BytesIO(moved_down.encode("utf-8")))[0]
    check_equal("y shifts do not affect output", render_pou(moved_down_pou), render_pou(pou))
except Exception as error:  # pragma: no cover - diagnostic path
    check("y-moved fixture parses", False, repr(error))

# --- rendering -------------------------------------------------------------

rendered = render_pou(pou)

check("no trailing whitespace", all(line == line.rstrip() for line in rendered))
# A rebuilt declaration says so before it says anything else: it is not what
# CODESYS holds, and nothing else in the file would tell you.
check("a rebuilt declaration is marked", rendered[0].startswith("(* Declaration rebuilt"))
check("declaration comes first", rendered[1] == "PROGRAM Motor_Control")

# Referenced through the charset table rather than as literal glyphs: this
# source file has to stay pure ASCII for IronPython 2.7 to load it at all.
U = charset.UNICODE

# The seal-in branch closes on its own row: a bottom-left corner, a contact,
# and a bottom-right corner. Matching the shape rather than an exact wire
# length keeps this from breaking every time a variable is renamed.
branch_rows = [line for line in rendered if U["BL"] in line and U["BR"] in line]
check_equal("exactly one branch closes", len(branch_rows), 1)
check("seal-in branch holds a contact", U["CONTACT_L"] in branch_rows[0])
check("branch opens with a tee", any(U["T_DOWN"] in line for line in rendered))
check("negated contact is drawn", any(U["CONTACT_L"] + "/" + U["CONTACT_R"] in line for line in rendered))
check("rising edge contact is drawn", any(U["CONTACT_L"] + "P" + U["CONTACT_R"] in line for line in rendered))
check("set coil is drawn", any("(S)" in line for line in rendered))
check("reset coil is drawn", any("(R)" in line for line in rendered))


# --- character sets --------------------------------------------------------

# The ASCII set exists for terminals and diff viewers that mangle box drawing,
# so its defining property is that nothing in the output is non-ASCII.
charset.use("ascii")
try:
    ascii_rendered = render_pou(pou)
finally:
    charset.use("unicode")

check("ascii charset emits no non-ASCII", all(ord(ch) < 128 for line in ascii_rendered for ch in line))
check("ascii charset still draws the branch", any("+----| |----+" in line for line in ascii_rendered))
check("unicode is restored afterwards", any(U["V"] in line for line in render_pou(pou)))
check_equal("both charsets produce the same shape", len(ascii_rendered), len(rendered))

def check_golden(name, rendered_lines, golden_path):
    # Goldens hold box-drawing characters, so the encoding cannot be left to
    # the platform default - and neither can printing them on a mismatch.
    handle = io.open(golden_path, encoding="utf-8")
    try:
        expected_lines = handle.read().replace("\r\n", "\n").rstrip("\n").split("\n")
    finally:
        handle.close()
    if rendered_lines != expected_lines:
        write(["--- expected ---"] + expected_lines + ["--- actual ---"] + rendered_lines)
    check_equal(name, rendered_lines, expected_lines)


check_golden("golden output matches", rendered, EXPECTED)


# --- a wired OR into a block pin ---------------------------------------------

# Two contacts in parallel feeding a timer's IN pin - a seal-in, the most
# ordinary shape in ladder. PLCopen writes the OR as two <connection> under
# the pin's one connectionPointIn, exactly as it does for a coil. The builder
# read each connection as a pin of its own, so the box drew two IN rows and
# the ST emitted "tmr(IN := xStart, IN := xRun)" - the OR lost, and read as a
# timer with two IN pins. The connections on one pin are now OR'd into it.
import st_render  # noqa: E402

OR_INTO_PIN = os.path.join(FIXTURES, "ld-or-into-block-pin.xml")
or_pou = parse_pous(OR_INTO_PIN)[0]
or_st = st_render.render_pou(or_pou)
or_art = render_pou(or_pou)

check("or into pin: the pin reads the OR", any("tmr(IN := (xStart OR xRun));" in line for line in or_st))
check("or into pin: the timer is called once", len([l for l in or_st if l.strip().startswith("tmr(")]) == 1)
check("or into pin: no duplicate IN argument", not any("IN := xStart, IN := xRun" in line for line in or_st))
check_equal("or into pin: one box is drawn", len([l for l in or_art if "tmr : TON" in l and ";" not in l]), 1)
# The two contacts are drawn in parallel ahead of the box, not as two pins.
check_equal("or into pin: the box has one IN row", len([l for l in or_art if "IN" in l and U["PIN_L"] in l]), 1)
check("or into pin: the branch is drawn", any(U["T_DOWN"] in l for l in or_art) and any(U["BL"] in l for l in or_art))
check("or into pin: both contacts are shown", any("xStart" in l for l in or_art) and any("xRun" in l for l in or_art))


# --- logic fidelity ----------------------------------------------------------

# Shapes that were dropped or inverted: a rung ending in a jump, its label, a
# negated inVariable on a block pin, and an assignment on a block output pin.
import st_render  # noqa: E402

LD_FIDELITY = os.path.join(FIXTURES, "ld_fidelity.plcopen.xml")
fidelity_pou = parse_pous(LD_FIDELITY)[0]
fidelity_st = st_render.render_pou(fidelity_pou)
fidelity_art = render_pou(fidelity_pou)

# The jump rung must survive as a rung at all; the label is the network's,
# not a rung, and is counted with the networks below.
check_equal("fidelity: all six rungs survive", len(fidelity_pou.rungs), 6)

# A jump's target lives in a "label" attribute; losing it drew ">>?" and
# emitted no ST for the whole rung, guard included.
check("fidelity: jump target is drawn", any(">>SKIP" in line for line in fidelity_art))
# A jump decides what runs next, so it is written as CODESYS ST writes it,
# like the label it targets - not as a note about the program.
check("fidelity: guarded jump reaches ST", "IF xGo THEN JMP SKIP; END_IF" in fidelity_st)
check("fidelity: no jump is dressed as a comment", not any("(* JMP" in line for line in fidelity_st))
# A label is the network's own, so it is written under the network's header
# the way the export writes it - and never as a rung.
check("fidelity: label heads its network", "SKIP:" in fidelity_art)
check("fidelity: label is not drawn as a rung", not any("SKIP:" in line and U["T_RIGHT"] in line for line in fidelity_art))
# A jump target is program structure, not documentation: it is written the
# way ST writes it, and not inside the delimiters this file uses for comments.
check("fidelity: label reaches ST", "SKIP:" in fidelity_st)
check("fidelity: the label is not dressed as a comment", not any("(* label" in line for line in fidelity_st + fidelity_art))

# model.Signal's docstring warns that dropping negated inverts the logic; the
# LD block-pin path did exactly that.
check("fidelity: negated pin keeps its NOT in ST", any("RESET := NOT xManual" in line for line in fidelity_st))
check(
    "fidelity: negated pin keeps its NOT beside the box",
    any("NOT xManual" + U["H"] * 2 + U["PIN_L"] + "RESET" in line for line in fidelity_art),
)

# An assignment on a block output pin executes every scan; the diagram drew it
# but the ST - the half reviewers are told to trust - left it out.
check("fidelity: output pin assignment reaches ST", any("iCount := ctr.CV;" in line for line in fidelity_st))
# A store below the first row hangs off its pin outside the box. The first
# row carries the rung's own wire onward, so a store there stays inline.
check(
    "fidelity: output pin assignment hangs off the pin",
    any("CV" + U["PIN_R"] + U["H"] * 3 + "> iCount" in line for line in fidelity_art),
)

# A rung can store through an outVariable element instead of a coil - the
# standard shape for a non-boolean result. It emitted no ST at all, and a
# negated one lost its NOT in the diagram too.
check("fidelity: outVariable store reaches ST", any("xStop := NOT xPress;" in line for line in fidelity_st))
check("fidelity: negated outVariable is marked in the diagram", any("[NOT xStop]" in line for line in fidelity_art))

# The negation bubble on the block's own pins: a negated power input and a
# negated, assigned output pin. Both inverted silently.
check("fidelity: negated power pin inverts in ST", any("tmr2(IN := NOT xRun);" in line for line in fidelity_st))
check("fidelity: negated output pin inverts its assignment", any("xCool := NOT tmr2.Q;" in line for line in fidelity_st))
check("fidelity: negated output pin is marked in the diagram", any("Q =o> xCool" in line for line in fidelity_art))

# A negated output consumed through a SIDE PIN goes via expr_to_text, a
# different path from the power flow - it must keep the NOT too.
check("fidelity: negated output survives into a side pin", any("RESET := NOT tmrA.Q" in line for line in fidelity_st))
check(
    "fidelity: the side pin names what the ST names",
    any("NOT tmrA.Q" + U["H"] * 2 + U["PIN_L"] + "RESET" in line for line in fidelity_art),
)

# The chain feeding a box on a side pin is the BOX's input, not a term of the
# pin's condition. Folding it in ("xB AND NOT tmrA.Q") says the counter also
# resets on NOT xB, and left tmrA with no call at all - a timer that the text
# never runs.
check("fidelity: a side-pin box gets its own call", any("tmrA(IN := xB);" in line for line in fidelity_st))
check("fidelity: a side-pin box is drawn", any("tmrA : TON" in line for line in fidelity_art))
check(
    "fidelity: the side pin does not absorb the box's input",
    not any("xB AND" in line for line in fidelity_st + fidelity_art),
)
check(
    "fidelity: the side-pin call comes before the box that reads it",
    fidelity_st.index("tmrA(IN := xB);") < fidelity_st.index("ctr2(CU := xGo2, RESET := NOT tmrA.Q);"),
)

# The same shape with nothing negated and no chain to absorb: an SR latch
# feeding a counter's RESET. The latch was named in the caption and never
# called.
LD_SIDE_PIN = os.path.join(FIXTURES, "ld_side_pin_latch.plcopen.xml")
side_pin_pou = parse_pous(LD_SIDE_PIN)[0]
side_pin_st = st_render.render_pou(side_pin_pou)
side_pin_art = render_pou(side_pin_pou)

check_equal("side pin: one rung", len(side_pin_pou.rungs), 1)
check("side pin: the latch is called", any("latch(SET1 := xSet, RESET := xClear);" in line for line in side_pin_st))
check("side pin: the pin reads only the latch output", any("RESET := latch.Q1" in line for line in side_pin_st))
check(
    "side pin: the pin names what the ST names",
    any("latch.Q1" + U["H"] * 2 + U["PIN_L"] + "RESET" in line for line in side_pin_art),
)
check("side pin: the latch box is drawn", any("latch : SR" in line for line in side_pin_art))
check("side pin: no chain folded into the pin", not any("xSet AND" in line for line in side_pin_st + side_pin_art))


# --- one editor network, several outputs -------------------------------------

# A timer driving three outputs. One network per sink made it three networks,
# each drawing the box again and calling the timer again, and threw out the
# number of every network after it. CODESYS exports one power rail for the
# whole body, so the rungs cannot be told apart by what they hang off - only
# by what they are connected to.
TWO_COILS = os.path.join(FIXTURES, "36-3-ld-two-coils.xml")
two_coils_pou = parse_pous(TWO_COILS)[0]
two_coils_st = st_render.render_pou(two_coils_pou)
two_coils_art = render_pou(two_coils_pou)

check_equal("two coils: two networks, not four", len(two_coils_pou.networks), 2)
check_equal("two coils: three outputs in the first", len(two_coils_pou.networks[0].outputs), 3)
check_equal(
    "two coils: one header per network",
    len([line for line in two_coils_art if line.startswith("(* Network")]),
    2,
)
check_equal("two coils: the timer is called once", len([l for l in two_coils_st if l.startswith("tmr(")]), 1)
check_equal("two coils: one box is drawn", len([l for l in two_coils_art if "tmr : TON" in l]), 1)

# All three outputs still there, and the second and third name the pin they
# read rather than redrawing the box that produces it.
check("two coils: the plain coil stores", "xOut1 := tmr.Q;" in two_coils_st)
check("two coils: the set coil latches", "IF tmr.Q THEN xOut2 := TRUE; END_IF" in two_coils_st)
check("two coils: the outVariable stores the other pin", "tElapsed := tmr.ET;" in two_coils_st)
check("two coils: a later output names the box", any("[tmr.ET]" in line for line in two_coils_art))

# A value feeding a side pin is drawn to the left of the box on a wire into
# the pin, the way the editor draws it. Written inside as "PT := T#2S" it
# reads as part of the pin name, and widens the box by every value in it.
check("two coils: the pin value sits outside the box", any("T#2S" + U["H"] * 2 + U["PIN_L"] + "PT" in line for line in two_coils_art))
check("two coils: no value is left inside a box", not any(" := " in line for line in two_coils_art))

# The same shape in a real SP11 export: LDTesting with one coil added to its
# first network.
SP11_TWO_COILS = os.path.join(FIXTURES, "36-3-ld-two-coils-sp11.xml")
sp11 = parse_pous(SP11_TWO_COILS)[0]
sp11_st = st_render.render_pou(sp11)

check_equal("sp11 two coils: two networks, not three", len(sp11.networks), 2)
check_equal("sp11 two coils: both coils in network 1", len(sp11.networks[0].outputs), 2)
check("sp11 two coils: the added coil is kept", any("Lamp :=" in line for line in sp11_st))
check_equal("sp11 two coils: the timer is called once", len([l for l in sp11_st if l.startswith("TON_0(")]), 1)


# --- an EXECUTE box on a rung ------------------------------------------------

# An EXECUTE box has no body of its own: the whole of it is inline ST in an
# addData element. The FBD renderer has always drawn it; the ladder one drew
# an empty rectangle and dropped every line of the logic.
LD_EXECUTE = os.path.join(FIXTURES, "ld_execute.plcopen.xml")
execute_pou = parse_pous(LD_EXECUTE)[0]
execute_st = st_render.render_pou(execute_pou)
execute_art = render_pou(execute_pou)

check_equal("execute: the inline ST is read", len(execute_pou.networks[0].outputs[0].items[-1].st_code), 4)
check("execute: the diagram shows the body", any("iCount := iCount + 1;" in line for line in execute_art))
check("execute: the body is inside the box", any(U["V"] + " iCount := iCount + 1;" in line for line in execute_art))
check("execute: the box is still drawn", any("EXECUTE" in line for line in execute_art))
# The rung condition is what decides whether the box runs, so it guards the
# body rather than being dropped for looking redundant.
check("execute: the ST guards the body with the rung", "IF xRun THEN" in execute_st)
check("execute: the body reaches the ST", any("iCount := iCount + 1;" in line for line in execute_st))
check("execute: no call to a box with no body", not any(line.startswith("EXECUTE(") for line in execute_st))


# --- edge detection on a block pin -------------------------------------------

# A contact has always carried its P; the block pin the rung's power enters
# through had nowhere to put one, so a counter that counts once per change
# rendered as one that counts every cycle its input is true.
PIN_EDGE = os.path.join(FIXTURES, "36-5-ld-pin-edge.xml")
pin_edge_pou = parse_pous(PIN_EDGE)[0]
pin_edge_st = st_render.render_pou(pin_edge_pou)
pin_edge_art = render_pou(pin_edge_pou)

check("ld pin edge: the ST shows the trigger", "ctr(CU := R(xCount), RESET := xRst, PV := 10);" in pin_edge_st)
check("ld pin edge: the box wall carries the marker", any("PCU" in line for line in pin_edge_art))
check("ld pin edge: an unmarked pin stays unmarked", not any("R(xRst)" in line for line in pin_edge_st))

# The contact form, which already worked, must keep working: same spelling in
# the ST, same letter in the diagram.
check("ld pin edge: a contact still triggers", "xEdge := R(xA);" in pin_edge_st)
check("ld pin edge: a contact still draws its P", any(U["CONTACT_L"] + "P" + U["CONTACT_R"] in line for line in pin_edge_art))


# --- network comments, and a network that holds only one ---------------------

# An LD network's comment never reached its header: the parser did not know
# the element existed, so every header read a bare "(* Network n *)".
LD_COMMENT = os.path.join(FIXTURES, "36-6-ld-comment.xml")
ld_comment_pou = parse_pous(LD_COMMENT)[0]
ld_comment_art = render_pou(ld_comment_pou)

check_equal("ld comment: two networks", len(ld_comment_pou.networks), 2)
check_equal("ld comment: the comment is read", ld_comment_pou.networks[1].comment, "XXX - WARNING: Timer then counter")
check("ld comment: it reaches the header", "(* Network 2: XXX - WARNING: Timer then counter *)" in ld_comment_art)

# A network holding nothing but a comment was dropped, and every network after
# it renumbered.
LD_EMPTY = os.path.join(FIXTURES, "36-6-ld-empty-network.xml")
ld_empty_pou = parse_pous(LD_EMPTY)[0]
ld_empty_art = render_pou(ld_empty_pou)

check_equal("ld empty: three networks", len(ld_empty_pou.networks), 3)
check_equal("ld empty: the middle one has no rungs", len(ld_empty_pou.networks[1].outputs), 0)
check_equal(
    "ld empty: the numbering follows the editor",
    [line for line in ld_empty_art if line.startswith("(* Network")],
    ["(* Network 1 *)", "(* Network 2: SECTION: safety interlocks *)", "(* Network 3 *)"],
)
# A header with nothing under it: the number is occupied, the body is empty,
# and the next network carries the next number.
empty_at = ld_empty_art.index("(* Network 2: SECTION: safety interlocks *)")
check_equal("ld empty: the comment-only network has no body", ld_empty_art[empty_at + 1], "")
check_equal("ld empty: Network 3 follows it", ld_empty_art[empty_at + 2], "(* Network 3 *)")
check_equal("ld empty: and holds the timer", len(ld_empty_pou.networks[2].outputs), 1)

# A jump label is stored on its network in CODESYS but exported just before
# it, wired to nothing. Counting it as a network of its own put it under a
# number of its own and pushed every later number out by one; carrying it
# into the network's body drew it as a rung, and twice over once the native
# export supplied the label as well. It is the network's label, nothing else.
check_equal("fidelity: six networks, not seven", len(fidelity_pou.networks), 6)
check_equal("fidelity: the label is the network's own", fidelity_pou.networks[1].label, "SKIP")
check_equal("fidelity: and is not in its body", len(fidelity_pou.networks[1].outputs), 1)
check(
    "fidelity: no label element is left in any body",
    not any(
        isinstance(rung, Element) and rung.kind == LABEL
        for network in fidelity_pou.networks
        for rung in network.outputs
    ),
)

# A negated wired output feeding a coil, and only one bubble drawn for it.
check("fidelity: negated wired output inverts the coil", any("xFin := NOT ctr2.Q;" in line for line in fidelity_st))
check("fidelity: no double bubble on a wired negated output", not any("Q oo" in line for line in fidelity_art))

# A negated power pin fed straight from the rail still states its inversion,
# instead of emitting a bare call identical to the un-negated case.
check("fidelity: rail-fed negated power pin is stated", any("tmrD(IN := NOT TRUE);" in line for line in fidelity_st))


# --- an EXECUTE box's EN pin bubble and edge in ST ---------------------------

# The EXECUTE branch of the LD walker used the rung condition raw, skipping
# the bubble and the P or N that every other block's power pin gets. A negated
# EN then read as an unguarded run, and a bare rail with a negated EN as an
# unconditional one - the exact inverse of when the program runs the code.
import st_render  # noqa: E402


def _execute(power_negated=False, power_edge=None):
    return Element(
        kind="block", type_name="EXECUTE", input_pins=[("EN", None)],
        output_pins=[("ENO", None)], st_code=["a := 1;"],
        power_negated=power_negated, power_edge=power_edge, active_output="ENO",
    )


def _contact(name):
    return Element(kind=CONTACT, label=name)


neg = st_render.rung_to_statements(Series([_contact("xRun"), _execute(power_negated=True)]))
check("execute EN: a negated EN inverts the guard", "IF NOT xRun THEN" in neg)
edge = st_render.rung_to_statements(Series([_contact("xRun2"), _execute(power_edge="rising")]))
check("execute EN: an edge EN triggers on the change", "IF R(xRun2) THEN" in edge)
bare = st_render.rung_to_statements(_execute(power_negated=True))
check("execute EN: a bare rail with a negated EN never runs it", "IF NOT TRUE THEN" in bare)
check("execute EN: a bare negated EN is not emitted unconditionally", bare[0] != "a := 1;")


# --- a stateless operator read by more than one rung -------------------------

# An operator whose output feeds two coils is not named ("OR.Out1" points at
# no variable) and not drawn twice: the two rungs share the box, so they are
# merged into one wire that branches after it, the box drawn once. The ladder
# path used to name the second read.
OPERATOR_ACROSS = os.path.join(FIXTURES, "ld-operator-across-rungs.xml")
opr_pou = parse_pous(OPERATOR_ACROSS)[0]
opr_art = render_pou(opr_pou)

check("operator reuse: the operator is not named as an instance", not any("OR.Out1" in line for line in opr_art))
check("operator reuse: the operator is not referenced in brackets", not any("[OR" in line for line in opr_art))
check_equal("operator reuse: the shared box is drawn once", len([l for l in opr_art if "In1   Out1" in l]), 1)
check("operator reuse: the readers branch off the box", any(U["T_DOWN"] in l for l in opr_art))
check("operator reuse: both coils are still driven", any("xA" in l for l in opr_art) and any("xB" in l for l in opr_art))


# --- a head shared by several branches is drawn once -------------------------

# The parser builds one branch per sink, so a contact chain or a block that
# feeds several sinks was repeated down every branch - drawn again and again,
# which read as separate rungs rather than one wire that branches after a
# shared head. The diagram now pulls the common prefix out in front, the way
# the editor draws it.
SHARED_PREFIX = os.path.join(FIXTURES, "ld-shared-prefix-branches.xml")
shared_pou = parse_pous(SHARED_PREFIX)[0]
shared_art = render_pou(shared_pou)

# xGo feeds two coils. It is drawn once, then the wire branches to each coil.
check_equal("shared prefix: the shared contact is drawn once", len([l for l in shared_art if "xGo" in l]), 1)
check("shared prefix: both coils are still drawn", any("xA" in l for l in shared_art) and any("xB" in l for l in shared_art))
check("shared prefix: the wire branches after the contact", any(U["T_DOWN"] in l for l in shared_art))
# The two coils sit on their own rows, one per branch.
xa_row = [i for i, l in enumerate(shared_art) if "xA" in l][0]
xb_row = [i for i, l in enumerate(shared_art) if "xB" in l][0]
check("shared prefix: the coils are on different rows", xa_row != xb_row)


# --- separate sinks that share a box are one branched rung -------------------

# A box whose output feeds two sinks reaches each through its own sink, so the
# parser builds a rung apiece and each redraws the box. That reads as two
# separate networks when it is one wire that splits after the box - the shape
# a RETURN and a coil sharing a block's ENO make. The rungs are now merged:
# the box is drawn once and the readers branch off it.
SHARED_BOX_SINKS = os.path.join(FIXTURES, "ld-return-and-coil-share-a-box.xml")
shared_box_pou = parse_pous(SHARED_BOX_SINKS)[0]
shared_box_art = render_pou(shared_box_pou)

check_equal("shared box sinks: the box is drawn once", len([l for l in shared_box_art if "In2   Out2" in l]), 1)
check_equal("shared box sinks: one rung header, one network", len([l for l in shared_box_art if l.startswith("(* Network")]), 1)
check("shared box sinks: the box output branches", any(U["T_DOWN"] in l for l in shared_box_art))
check("shared box sinks: the RETURN is drawn", any("<RETURN>" in l for l in shared_box_art))
check("shared box sinks: the coil branch is drawn", any("( )" in l for l in shared_box_art))
check("shared box sinks: the edge contact is on the coil branch", any(U["CONTACT_L"] + "P" + U["CONTACT_R"] in l for l in shared_box_art))
# The two sinks are on their own rows, not stacked into one.
return_row = [i for i, l in enumerate(shared_box_art) if "<RETURN>" in l][0]
coil_row = [i for i, l in enumerate(shared_box_art) if "( )" in l][0]
check("shared box sinks: RETURN and the coil are on different rows", return_row != coil_row)


# --- a contact reads a block output without naming the pin -------------------

# CODESYS often wires a contact to a block's output without naming the pin, so
# the connection carries no formalParameter. That read still consumes the
# block, so its output must tee - and the box must build the same whether the
# reader named the pin or not, or two rungs that share the box (a RETURN and a
# coil off one ENO) would not line up and would not merge. This is the shape a
# real Network 5 makes.
UNNAMED = os.path.join(FIXTURES, "ld-contact-reads-block-unnamed-pin.xml")
unnamed_pou = parse_pous(UNNAMED)[0]
unnamed_art = render_pou(unnamed_pou)

check_equal("unnamed pin: the box is drawn once", len([l for l in unnamed_art if "In2   Out2" in l]), 1)
check_equal("unnamed pin: one network, one header", len([l for l in unnamed_art if l.startswith("(* Network")]), 1)
check("unnamed pin: the box output branches", any(U["T_DOWN"] in l for l in unnamed_art))
check("unnamed pin: the consumed output is teed", any("ENO" + U["PIN_R"] in l for l in unnamed_art))
check("unnamed pin: no untee'd wire runs from the box", not any("ENO" + U["V"] + U["H"] in l for l in unnamed_art))
check("unnamed pin: RETURN and the coil are both drawn", any("<RETURN>" in l for l in unnamed_art) and any("( )" in l for l in unnamed_art))


# --- byte order mark -------------------------------------------------------

# CODESYS writes a BOM on every export_xml file, and the ElementTree it ships
# in ScriptLib rejects one outright. CPython's expat accepts it silently, and
# so does stock IronPython, so no amount of CI could catch this by parsing
# alone - it only reproduces inside CODESYS. Asserting on the bytes handed to
# the parser is what makes it catchable here.
import plcopen  # noqa: E402

BOM = b"\xef\xbb\xbf"
CODESYS_FIXTURES = os.path.join(FIXTURES, "codesys")

bom_fixtures = 0
for name in sorted(os.listdir(CODESYS_FIXTURES)):
    if not name.endswith(".xml"):
        continue
    bom_fixtures += 1
    path = os.path.join(CODESYS_FIXTURES, name)
    raw = open(path, "rb").read()
    # The fixtures are real exports, so they should still carry their BOM. If
    # one loses it, this test stops proving anything.
    check(name + " is a real export, BOM and all", raw.startswith(BOM))
    check_equal(name + " is fed to the parser without its BOM", plcopen.read_document(path)[:1], b"<")

# If the fixtures move, the loop above runs zero times and the BOM contract -
# the one that only reproduces inside CODESYS - silently stops being tested.
check("the BOM sweep found the real exports", bom_fixtures >= 3, "found %d" % bom_fixtures)

check_equal(
    "leading whitespace is dropped too",
    plcopen.read_document(io.BytesIO(BOM + b"\n  <a/>")),
    b"<a/>",
)
check_equal(
    "a document with no BOM is untouched",
    plcopen.read_document(io.BytesIO(b"<a/>")),
    b"<a/>",
)


# --- non-ASCII content -----------------------------------------------------

# The parser CODESYS ships works byte-wise and rejects UTF-8 multi-byte
# sequences, so one degree sign in a comment loses the whole POU. Numeric
# character references are ASCII and every parser expands them identically.
DEGREE = b'<a><b>Temp \xc2\xb0C</b></a>'

check_equal(
    "non-ASCII becomes a numeric character reference",
    plcopen.read_document(io.BytesIO(DEGREE)),
    b"<a><b>Temp &#176;C</b></a>",
)
check("escaped bytes are pure ASCII", all(b < 128 for b in bytearray(plcopen.read_document(io.BytesIO(DEGREE)))))

# The whole point: the parsed text must come back unchanged.
import xml.etree.ElementTree as ET  # noqa: E402

check_equal(
    "the character survives the round trip",
    ET.fromstring(plcopen.read_document(io.BytesIO(DEGREE)))[0].text,
    u"Temp \u00b0C",
)
check_equal(
    "pure ASCII documents are left alone",
    plcopen.read_document(io.BytesIO(b"<a>plain</a>")),
    b"<a>plain</a>",
)

# A failure has to explain itself, so the next CODESYS run needs no separate
# diagnostic script.
handle = io.open(os.path.join(FIXTURES, "codesys", "LDTesting.xml"), "rb")
try:
    clean = handle.read()
finally:
    handle.close()

import tempfile  # noqa: E402

descriptor, suspect_path = tempfile.mkstemp(suffix=".xml")
try:
    os.write(descriptor, clean.replace(b"<contact", b"<\x0ccontact", 1))
    os.close(descriptor)
    notes = plcopen.describe_suspect_characters(suspect_path)
    check("a control character is reported", any("control character 0x0C" in note for note in notes))
    check("the report carries a line number", any("line " in note for note in notes))
finally:
    if os.path.exists(suspect_path):
        os.remove(suspect_path)

check_equal("a clean file reports nothing suspect", plcopen.describe_suspect_characters(SOURCE), [])


# --- plaintext declarations ------------------------------------------------

# The structured <interface> has nowhere to put a comment, a pragma or an
# attribute. export_xml(declarations_as_plaintext=True) carries the real text,
# and a pragma like {attribute 'qualified_only'} changes what the code means -
# so paraphrasing it away is worse than not showing it.
DECLARATION = """{attribute 'qualified_only'}
PROGRAM PLAIN
VAR
    xStart : BOOL;  // start button, NO contact
    (* the seal-in *)
    xRun : BOOL := FALSE;
END_VAR"""


def with_interface(interface):
    body = '<body><LD><leftPowerRail localId="1"><connectionPointOut/></leftPowerRail>'
    body += '<coil localId="2"><connectionPointIn><connection refLocalId="1"/></connectionPointIn>'
    body += "<variable>xRun</variable></coil></LD></body>"
    document = '<project><types><pous><pou name="PLAIN" pouType="program">'
    document += interface + body + "</pou></pous></types></project>"
    return io.BytesIO(document.encode("utf-8"))


PLAINTEXT_INTERFACE = (
    "<interface><localVars><variable name=\"xStart\"><type><BOOL/></type></variable></localVars>"
    '<addData><data name="http://www.3s-software.com/plcopenxml/declarations" handleUnknown="implementation">'
    "<Declarations>" + DECLARATION + "</Declarations></data></addData></interface>"
)
STRUCTURED_INTERFACE = '<interface><localVars><variable name="xStart"><type><BOOL/></type></variable></localVars></interface>'

plain_pou = parse_pous(with_interface(PLAINTEXT_INTERFACE))[0]
check_equal("the plaintext declaration is picked up", plain_pou.declaration_text, DECLARATION)

declaration = render_declaration(plain_pou)
check_equal("it is used verbatim, line for line", declaration, DECLARATION.split("\n"))
check("a pragma survives", any("{attribute 'qualified_only'}" in line for line in declaration))
check("a line comment survives", any("// start button, NO contact" in line for line in declaration))
check("a block comment survives", any("(* the seal-in *)" in line for line in declaration))

# It has to reach the rendered file, not just the model.
check_equal("the rendering leads with it", render_pou(plain_pou)[0], "{attribute 'qualified_only'}")

# Older exports carry no plaintext, and must still render something.
structured_pou = parse_pous(with_interface(STRUCTURED_INTERFACE))[0]
check_equal("no plaintext means none is invented", structured_pou.declaration_text, None)
check_equal("the structured interface is the fallback", render_declaration(structured_pou)[1], "PROGRAM PLAIN")
check("the fallback says it is one", render_declaration(structured_pou)[0].startswith("(* Declaration rebuilt"))
check("the fallback still lists the variable", any("xStart : BOOL;" in line for line in render_declaration(structured_pou)))

# The shape CODESYS actually writes, confirmed by diagnosing a real project:
# a data element named ".../interfaceasplaintext", sitting at POU level rather
# than inside <interface> despite the name, with the text nested below it.
# The first two attempts at this searched only inside <interface>, and then
# only two levels down.
REAL_SHAPE = (
    "<interface><localVars><variable name=\"xStart\"><type><BOOL/></type></variable></localVars></interface>"
    "<addData><data name=\"http://www.3s-software.com/plcopenxml/interfaceasplaintext\""
    ' handleUnknown="implementation"><InterfaceAsPlainText><xhtml xmlns="http://www.w3.org/1999/xhtml">'
    + DECLARATION
    + "</xhtml></InterfaceAsPlainText></data></addData>"
)


def with_pou_level_add_data(extra):
    body = '<body><LD><leftPowerRail localId="1"><connectionPointOut/></leftPowerRail>'
    body += '<coil localId="2"><connectionPointIn><connection refLocalId="1"/></connectionPointIn>'
    body += "<variable>xRun</variable></coil></LD></body>"
    document = '<project><types><pous><pou name="PLAIN" pouType="program">'
    document += extra.replace("</interface>", "</interface>" + body, 1) + "</pou></pous></types></project>"
    return io.BytesIO(document.encode("utf-8"))


real_pou = parse_pous(with_pou_level_add_data(REAL_SHAPE))[0]
check_equal("the real CODESYS shape is found", real_pou.declaration_text, DECLARATION)
check("nested text is reached, not just two levels", "// start button, NO contact" in (real_pou.declaration_text or ""))

# The addData element name is a proprietary extension that has moved between
# CODESYS versions, so the lookup matches on shape rather than on a name that
# would silently fall back to the lossy path if it ever changed again.
RENAMED = PLAINTEXT_INTERFACE.replace("Declarations", "DeclarationText").replace(
    "plcopenxml/declarations", "plcopenxml/pou-declaration"
)
check_equal(
    "a renamed addData element is still found",
    parse_pous(with_interface(RENAMED))[0].declaration_text,
    DECLARATION,
)

DECOY = '<data name="vendor-metadata"><text>VAR fake END_VAR</text></data>'
AMBIGUOUS = PLAINTEXT_INTERFACE.replace("<addData>", "<addData>" + DECOY, 1)
check_equal(
    "ambiguous declaration-like addData is rejected",
    parse_pous(with_interface(AMBIGUOUS))[0].declaration_text,
    None,
)


# --- real CODESYS export ---------------------------------------------------

# Exported from CODESYS V3.5 SP11 via Project > Export > PLCopenXML. This is
# the dialect that actually matters; the hand-authored fixture above only
# covers what the spec says.
CODESYS_SOURCE = os.path.join(FIXTURES, "codesys", "LDTesting.xml")
CODESYS_EXPECTED = os.path.join(FIXTURES, "codesys", "LDTesting.expected.txt")

codesys_pous = parse_pous(CODESYS_SOURCE)
check_equal("codesys: one LD pou", len(codesys_pous), 1)

ld_test = codesys_pous[0]
check_equal("codesys: pou name", ld_test.name, "LD_TEST")
check_equal("codesys: two networks", len(ld_test.rungs), 2)

# CODESYS writes edge="none"/storage="none" rather than omitting the attribute.
network1 = ld_test.rungs[0]
check_equal("codesys: literal 'none' edge is normalised away", network1.items[1].edge, None)
check("codesys: negated contact survives", network1.items[1].negated)
check_equal("codesys: set coil", network1.items[2].storage, "set")

# typeName and instanceName are attributes in CODESYS's output. Reading them as
# child elements is what produced "[?]" boxes on the first run.
network2 = ld_test.rungs[1]
blocks = [item for item in network2.items if getattr(item, "kind", None) == "block"]
check_equal("codesys: two blocks in network 2", len(blocks), 2)
check_equal("codesys: block type name", blocks[0].type_name, "TON")
check_equal("codesys: block instance name", blocks[0].instance_name, "TON_0")
check_equal("codesys: block title", blocks[0].title, "TON_0 : TON")

# The power pin sorts first and carries no caption; parameter pins carry one.
check_equal("codesys: TON power pin is IN", blocks[0].input_pins[0], ("IN", None))
check_equal("codesys: TON PT is a parameter", blocks[0].input_pins[1], ("PT", "T#5S"))

# A second wired input cannot be drawn as another horizontal wire, so it is
# flattened to text inside the pin.
check_equal("codesys: CTU power pin is CU", blocks[1].input_pins[0], ("CU", None))
check_equal("codesys: CTU RESET is flattened to text", blocks[1].input_pins[1], ("RESET", "PowerOff"))
check_equal("codesys: CTU PV is a literal", blocks[1].input_pins[2], ("PV", "10"))

# The consumer's connection names the output pin it draws from.
check_equal("codesys: active output follows the wire", blocks[0].active_output, "Q")
check_equal("codesys: active output sorts first", blocks[0].output_pins[0][0], "Q")

codesys_rendered = render_pou(ld_test)
check("codesys: no trailing whitespace", all(line == line.rstrip() for line in codesys_rendered))
check_golden("codesys: golden output matches", codesys_rendered, CODESYS_EXPECTED)

print("")
if failures:
    print("%d check(s) failed" % len(failures))
else:
    print("all checks passed")
sys.exit(1 if failures else 0)
