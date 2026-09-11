# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Tests for the Function Block Diagram renderer and the ST emitter.

Plain script rather than pytest, matching tools/ci/, so it runs under both
Python 3 and the IronPython 2.7 that CODESYS embeds.

    python tools/ladder/tests/test_fbd.py
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
import layout  # noqa: E402
import fbd_render  # noqa: E402
import parse_ld  # noqa: E402
import parse_fbd  # noqa: E402
import st_render  # noqa: E402
from model import Assign, Call, Label, Network, OutputRef, Pou, Signal  # noqa: E402
from render import write  # noqa: E402

# Referenced through the charset table rather than as literal glyphs: this
# source file has to stay pure ASCII for IronPython 2.7 to load it at all.
U = charset.UNICODE

FIXTURES = os.path.join(HERE, "fixtures", "codesys")
FBD_SOURCE = os.path.join(FIXTURES, "FbTesting.xml")
LD_SOURCE = os.path.join(FIXTURES, "LDTesting.xml")
SFC_SOURCE = os.path.join(FIXTURES, "SFCTesting.xml")

def box(node):
    """The Call a wire reads, unwrapping the pin the wire names.

    A wire that reads a named output pin arrives as an OutputRef around the
    call, so that a box read through two pins stays one box.
    """
    return node.call if isinstance(node, OutputRef) else node


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


def check_golden(name, rendered, golden_path):
    # Goldens hold box-drawing characters, so the encoding cannot be left to
    # the platform default - and neither can printing them on a mismatch.
    handle = io.open(golden_path, encoding="utf-8")
    try:
        expected = handle.read().replace("\r\n", "\n").rstrip("\n").split("\n")
    finally:
        handle.close()
    if rendered != expected:
        write(["--- expected ---"] + expected + ["--- actual ---"] + rendered)
    check_equal(name, rendered, expected)


# --- parsing ---------------------------------------------------------------

pous = parse_fbd.parse_pous(FBD_SOURCE)
check_equal("one FBD pou is found", len(pous), 1)

pou = pous[0]
check_equal("pou name", pou.name, "FB_TESTING")
check_equal("language is recorded", pou.language, "FBD")
check_equal("two networks", len(pou.networks), 2)

# localVars constant="true" is a separate group and must not merge with VAR.
check_equal("constant scope", pou.variables[0].scope, "VAR CONSTANT")
check_equal("constant initial value", pou.variables[0].initial_value, "5000")
check_equal("namespaced derived type", pou.variables[1].type_name, "ifmIOcommon.SystemSupply")

# Comments carry the network's intent and nest their text in an xhtml element.
comment1, tree1 = pou.networks[0].comment, pou.networks[0].outputs[0]
check("network 1 comment is captured", comment1.startswith("// Function Block to monitor supply voltage"))

hostile_comment = "// first\nsecond *) third"
check_equal(
    "network comments cannot break generated block comments",
    fbd_render.render_pou(Pou("HOSTILE", "program", networks=[Network(hostile_comment, [Signal("x")])]))[3],
    "(* Network 1: first second * ) third *)",
)
check_equal(
    "ST network comments cannot break generated block comments",
    st_render.render_pou(Pou("HOSTILE", "program", networks=[Network(hostile_comment, [Signal("x")])]))[3],
    "(* Network 1: first second * ) third *)",
)

# A title is a second field, and can break the block comment just as a
# comment can. With no comment beside it, the title is the heading.
hostile_title = "one *) two"
check_equal(
    "network titles cannot break generated block comments",
    fbd_render.render_pou(
        Pou("HOSTILE", "program", networks=[Network("", [Signal("x")], title=hostile_title)])
    )[3],
    "(* Network 1: one * ) two *)",
)

check("network 1 is a call", isinstance(tree1, Call))
check_equal("network 1 instance", tree1.instance_name, "fbSystemSupply")
check_equal("network 1 type", tree1.type_name, "ifmIOcommon.SystemSupply")
check_equal("network 1 has three inputs", len(tree1.inputs), 3)
check_equal("first pin name", tree1.inputs[0][0], "eChannel")
check("first pin source is a signal", isinstance(tree1.inputs[0][1], Signal))
check_equal("first pin value", tree1.inputs[0][1].label, "ifmIOcommon.SYS_VOLTAGE_CHANNEL.VBB15")

# An unconnected pin exports as an element with an empty expression, not as a
# missing element - so it reaches the tree as a Signal carrying no label.
check_equal("unwired pin name", tree1.inputs[2][0], "eFilter")
check_equal("unwired pin has an empty label", tree1.inputs[2][1].label, "")
check("unwired pin is not drawn with a wire", not fbd_render._is_wired(tree1.inputs[2][1]))

# CODESYS writes an assignment straight onto the output pin.
outputs = dict(tree1.outputs)
check_equal("output assignment is captured", outputs["uiOutVoltage"], "uiCurrSupplyVolt")

# Network 2 nests three calls: GT -> TOF -> SupplySwitch.
comment2, tree2 = pou.networks[1].comment, pou.networks[1].outputs[0]
check_equal("network 2 root", tree2.instance_name, "fbSupplySwitch")

# The pin a wire reads is on the wire, not on the box it reads: a box is one
# box however many of its pins are read.
tof_wire = tree2.inputs[1][1]
check("the wire into fbSupplySwitch names its pin", isinstance(tof_wire, OutputRef))
check_equal("wire leaves TOF on Q", tof_wire.pin, "Q")
tof = tof_wire.call
check_equal("nested TOF", tof.instance_name, "TOF_0")
check("TOF knows Q is read", "Q" in tof.wired_outputs)
gt = box(tof.inputs[0][1])
check_equal("nested GT", gt.type_name, "GT")

# An operator has no instance name, so it inlines as an expression in ST.
check("GT is an operator", gt.is_operator)
check("TOF is not an operator", not tof.is_operator)
check_equal("operator title omits the instance", gt.title, "GT")
check_equal("function block title includes it", tof.title, "TOF_0 : TOF")

# --- FBD rendering ---------------------------------------------------------

art = fbd_render.render_pou(pou)
check("art: no trailing whitespace", all(line == line.rstrip() for line in art))
check("art: boxes do not fuse together", not any(U["TR"] + U["TL"] in line for line in art))
# The store hangs off its pin on a wire, outside the box. Written inside, the
# target variable sat among the pin names where it read as another pin.
check(
    "art: output assignment hangs off the pin",
    any("uiOutVoltage" + U["PIN_R"] + "---> uiCurrSupplyVolt".replace("---", U["H"] * 3) in line for line in art),
)
check("art: nested operator box is drawn", any(U["PIN_L"] + "In1   Out1" + U["PIN_R"] in line for line in art))

# A tee marks a real connection, so an unconsumed output must leave the wall
# unbroken. fbSupplySwitch is a network sink: nothing takes its xError.
check("art: sink output is not teed", any("xError" + U["V"] in line for line in art))
check("art: consumed output is teed", any("Out1" + U["PIN_R"] in line for line in art))

# Every position in this export is x="0" y="0". If layout depended on those
# coordinates the three boxes would land on top of each other, so finding each
# title on its own distinct row is what proves layout comes from topology.
title_rows = {}
for row, line in enumerate(art):
    for title in ("GT", "TOF_0 : TOF", "fbSupplySwitch : ifmIOcommon.SupplySwitch"):
        if title in line and title not in title_rows:
            title_rows[title] = row
check_equal("art: all three boxes are placed", len(title_rows), 3)
check_equal("art: no two boxes share a row", len(set(title_rows.values())), 3)

check_golden("art: golden output matches", art, os.path.join(FIXTURES, "FbTesting.art.expected.txt"))

# --- ST emission -----------------------------------------------------------

fbd_st = st_render.render_pou(pou)

SUPPLY_CALL = (
    "fbSystemSupply(eChannel := ifmIOcommon.SYS_VOLTAGE_CHANNEL.VBB15,"
    " eMode := ifmIOcommon.MODE_SYSTEM_SUPPLY.SYS_SUPPLY);"
)
SWITCH_CALL = "fbSupplySwitch(eMode := ifmIOcommon.MODE_SUPPLY_SWITCH.SYS_SUPPLY_SWITCH, xValue := TOF_0.Q);"

check("st: function block becomes a call statement", SUPPLY_CALL in fbd_st)
check("st: output assignment becomes its own statement", "uiCurrSupplyVolt := fbSystemSupply.uiOutVoltage;" in fbd_st)
check("st: comparison operator inlines infix", "TOF_0(IN := uiCurrSupplyVolt > uiMinVoltage, PT := T#5S);" in fbd_st)
check("st: nested output is referenced by pin", SWITCH_CALL in fbd_st)
check("st: unwired pin is omitted", not any("eFilter" in line for line in fbd_st))

check_golden("st: FBD golden matches", fbd_st, os.path.join(FIXTURES, "FbTesting.st.expected.txt"))

ld_pou = parse_ld.parse_pous(LD_SOURCE)[0]
ld_st = st_render.render_pou(ld_pou)
check("st: parallel branch becomes OR", "IF (Sensor1 OR sensor3) AND NOT Sensor2 THEN PowerOn := TRUE; END_IF" in ld_st)
check("st: ladder block becomes a call", "TON_0(IN := PowerOn, PT := T#5S);" in ld_st)
check("st: block chains through its output pin", "CTU_0(CU := TON_0.Q, RESET := PowerOff, PV := 10);" in ld_st)
check("st: reset coil becomes a conditional", "IF CTU_0.Q THEN PowerOff := FALSE; END_IF" in ld_st)

check_golden("st: LD golden matches", ld_st, os.path.join(FIXTURES, "LDTesting.st.expected.txt"))

# --- control flow ----------------------------------------------------------

# Everything below was silently dropped before, which is worse than failing:
# the rendering looked complete while a guard clause and a body of inline ST
# were simply absent.
CONTROL_FLOW = os.path.join(HERE, "fixtures", "fbd_control_flow.plcopen.xml")
flow = parse_fbd.parse_pous(CONTROL_FLOW)[0]
flow_st = st_render.render_pou(flow)
flow_art = fbd_render.render_pou(flow)

# Three, not four: CODESYS stores a jump label on the network it labels, but
# PLCopen exports it as a free-standing element just before that network, so
# it arrives wired to nothing. Counting it as a network of its own put the
# label under its own number and pushed every later number out by one.
check_equal("flow: three networks survive", len(flow.networks), 3)
check_equal("flow: the label is the network's own", flow.networks[2].label, "END")
check("flow: the label is not in the network's body", not any(isinstance(tree, Label) for tree in flow.networks[2].outputs))

# A jump terminates a network. Leaving it out of SINK_KINDS dropped the entire
# guard network, because nothing else consumed the OR feeding it.
check("flow: the guard network is not dropped", any("JMP END" in line for line in flow_st))
check("flow: the jump condition is kept", any("Mode.Current = Mode.ESTOP" in line for line in flow_st))
check("flow: the jump target is drawn", any(">> END" in line for line in flow_art))
check("flow: the label is shown", "END:" in flow_st)
check("flow: the label heads the diagram too", "END:" in flow_art)
check("flow: the label is not drawn as a rung", not any("END:" in line and line != "END:" for line in flow_art))
check("flow: the label is not dressed as a comment", not any("(* label" in line for line in flow_st + flow_art))

# negated="true" on an inVariable inverts the logic if it is ignored.
guard = flow.networks[0].outputs[0]
check_equal("flow: negation reaches the tree", box(guard.condition).inputs[0][1].negated, True)
check_equal("flow: negation renders", box(guard.condition).inputs[0][1].text, "NOT xInitDone")
check("flow: negation survives into ST", any("(NOT xInitDone) OR" in line for line in flow_st))

# An EXECUTE box is nothing but inline ST; drawing the box alone loses it all.
execute = flow.networks[2].outputs[0]
check_equal("flow: inline ST is captured", len(execute.st_code), 4)
check("flow: inline ST reaches the ST output", any("Status.Faulted := FALSE;" in line for line in flow_st))
# The EN pin genuinely guards the box, so it has to show up as a condition
# rather than being dropped for looking redundant.
check("flow: the EN guard wraps the inline ST", any(line == "IF xInitDone THEN" for line in flow_st))
check("flow: inline ST reaches the diagram", any("Status.Faulted := FALSE;" in line for line in flow_art))

# Operators read as operators, not as function calls.
check("flow: arithmetic inlines infix", any("RawPressure / 100" in line for line in flow_st))
check("flow: conversions stay function calls", any("REAL_TO_UINT(" in line for line in flow_st))
check(
    "flow: compound operands are bracketed",
    any("(NOT xInitDone) OR (Mode.Current = Mode.ESTOP)" in line for line in flow_st),
)


# --- logic fidelity ----------------------------------------------------------

# Shapes whose mishandling renders the *inverse* of the program, or fabricates
# logic that is not there. For a review artifact that is worse than a crash.
FIDELITY = os.path.join(HERE, "fixtures", "fbd_fidelity.plcopen.xml")
fid = parse_fbd.parse_pous(FIDELITY)[0]
fid_st = st_render.render_pou(fid)
fid_art = fbd_render.render_pou(fid)

# A connector terminates its network, so all seven must survive.
check_equal("fidelity: all seven networks survive", len(fid.networks), 7)

# negated="true" on an outVariable inverts the logic if it is dropped.
check("fidelity: negated output inverts in ST", any("xInverted := NOT xIn;" in line for line in fid_st))
check("fidelity: negated output is marked in the diagram", any("o> xInverted" in line for line in fid_art))

# A connector names a wire; the continuation re-emits it. Before these were
# handled, the AND network vanished and the consumer rendered "xBoth := FALSE;"
# - fabricated logic, not just missing logic.
check("fidelity: connector network keeps its logic", any("C1 := xRun AND xReady;" in line for line in fid_st))
check("fidelity: continuation resolves to the named wire", any("xBoth := C1;" in line for line in fid_st))
check("fidelity: nothing is fabricated as FALSE", not any(":= FALSE" in line for line in fid_st))
check("fidelity: the connector's source reaches the diagram", any("xRun" in line for line in fid_art))

# The negation bubble on a block's own input pin, distinct from a negated
# inVariable element. Dropping it computes AND where the program computes
# AND NOT.
check("fidelity: negated input pin inverts in ST", any("xMasked := xRun2 AND (NOT xReady2);" in line for line in fid_st))
check("fidelity: negated input pin reaches the diagram", any("NOT" in line and "xReady2" in line for line in fid_art))

# The same bubble on an output pin carrying an inline assignment: the stored
# value is the inverse of the pin.
check("fidelity: negated output pin inverts its assignment", any("xIdle := NOT tmr.Q;" in line for line in fid_st))
check(
    "fidelity: negated output pin is marked in the diagram",
    any("Q" + U["PIN_R"] + U["H"] * 3 + "o> xIdle" in line for line in fid_art),
)

# NOT binds tighter than OR in IEC 61131-3, so a negated compound expression
# must keep its parentheses or the logic regroups.
check("fidelity: negated compound expression keeps its grouping", any("xGuard := NOT (xA OR xB);" in line for line in fid_st))

# Expressions are free-form ST and are routinely typed without spaces; NOT
# still binds above the comparison, so "NOT iCount>5" states (NOT iCount)>5.
check("fidelity: spaceless compound keeps its grouping", any("xHot := NOT (iCount>5);" in line for line in fid_st))


# --- fan-out ---------------------------------------------------------------

# One source driving several outputs is a single network in the editor.
# Treating each output as its own network split every one of them in two and
# duplicated the shared expression, so the numbering disagreed with CODESYS.
FANOUT = os.path.join(HERE, "fixtures", "fbd_fanout.plcopen.xml")
fan = parse_fbd.parse_pous(FANOUT)[0]
fan_st = st_render.render_pou(fan)
fan_art = fbd_render.render_pou(fan)

check_equal("fanout: three networks, not five", len(fan.networks), 3)
check_equal("fanout: the OR drives two outputs", len(fan.networks[0].outputs), 2)
check_equal("fanout: the timer drives two outputs", len(fan.networks[1].outputs), 2)
check_equal("fanout: a plain network keeps one", len(fan.networks[2].outputs), 1)

# Both outputs of a network sit under its one header, with its one comment.
header_rows = [row for row, line in enumerate(fan_st) if line.startswith("(* Network")]
check_equal("fanout: three headers, not five", len(header_rows), 3)
check("fanout: the comment lands on the network", "Conveyor off is the opposite" in fan_st[header_rows[0]])
check_equal(
    "fanout: both stores share a header",
    fan_st[header_rows[0] + 1 : header_rows[0] + 3],
    [
        "Flags.ConvOn := Flags.FwdSolOn OR Flags.RevSolOn;",
        "Flags.ConvOff := NOT (Flags.FwdSolOn OR Flags.RevSolOn);",
    ],
)

# The sharper case: the block is called once in the program, so emitting the
# call per output would misstate what runs.
check_equal("fanout: the block is called once", len([l for l in fan_st if l.startswith("TON_0(")]), 1)
check("fanout: both stores are still made", "Status.Done := TON_0.Q;" in fan_st and "Status.Latched := TON_0.Q;" in fan_st)

# The shared source is drawn once and branched, not drawn per output.
check_equal("fanout: one OR box is drawn", len([l for l in fan_art if "In1   Out1" in l]), 1)
check("fanout: the branch is drawn", any(U["T_DOWN"] in l and "Flags.ConvOn" in l for l in fan_art))
check("fanout: the negated leg keeps its bubble", any(U["BL"] in l and "o Flags.ConvOff" in l for l in fan_art))

# Identity, not equality, is what tells a fan-out from two equal expressions.
# The wires differ - each names the pin it reads - but the box behind them is
# one object.
first, second = fan.networks[0].outputs
check("fanout: shared nodes are one object", box(first.source) is box(second.source))


# --- one instance read through two of its pins -------------------------------

# A timer whose Q feeds one store and whose ET feeds another. Memoising the
# tree on (localId, pin) made that two timers: two boxes drawn, and two calls
# emitted, so a reader concluded the timer ran twice each cycle.
TWO_PINS = os.path.join(HERE, "fixtures", "36-2-fbd-two-output-pins.xml")
two_pins = parse_fbd.parse_pous(TWO_PINS)[0]
two_pins_st = st_render.render_pou(two_pins)
# The network alone: render_pou would also give us the declaration, where
# "tmr : TON" appears again as the variable it is.
two_pins_art = fbd_render.render_network(two_pins.networks[0])

check_equal("two pins: one network", len(two_pins.networks[0].outputs), 2)
check(
    "two pins: both stores read the same box",
    box(two_pins.networks[0].outputs[0].source) is box(two_pins.networks[0].outputs[1].source),
)
check_equal(
    "two pins: the pins are on the wires",
    sorted(output.source.pin for output in two_pins.networks[0].outputs),
    ["ET", "Q"],
)
check_equal("two pins: the timer is called once", len([l for l in two_pins_st if l.startswith("tmr(")]), 1)
check("two pins: Q is stored", "xQ := tmr.Q;" in two_pins_st)
check("two pins: ET is stored", "tEt := tmr.ET;" in two_pins_st)
check_equal("two pins: one box is drawn", len([l for l in two_pins_art if "tmr : TON" in l]), 1)

# Two pins are two wires, not one branched wire: a junction column here would
# draw ET and Q as the same signal.
check("two pins: Q leaves on its own row", any(l.rstrip().endswith("> xQ") and "Q" + U["PIN_R"] in l for l in two_pins_art))
check("two pins: ET leaves on its own row", any(l.rstrip().endswith("> tEt") and "ET" + U["PIN_R"] in l for l in two_pins_art))
check("two pins: no junction between different pins", not any(U["T_DOWN"] in l and "xQ" in l for l in two_pins_art))


# --- one box read by two of a network's outputs ------------------------------

# Where both readers hang straight off the box the fan-out draws it once and
# branches. A reader sitting behind another box is a tree of its own, and
# drawing that tree from scratch put a second copy of the same instance on the
# page - two timers where the program has one. This is FB_TESTING network 9 in
# the GraphicalTesting project.
SHARED_BOX = os.path.join(HERE, "fixtures", "fbd_shared_box.plcopen.xml")
shared = parse_fbd.parse_pous(SHARED_BOX)[0]
shared_st = st_render.render_pou(shared)
shared_art = fbd_render.render_network(shared.networks[0])

check_equal("shared box: one network", len(shared.networks), 1)
check_equal("shared box: two outputs", len(shared.networks[0].outputs), 2)
check_equal("shared box: the timer is called once", len([l for l in shared_st if l.startswith("fbTimer(")]), 1)
check_equal("shared box: one box is drawn", len([l for l in shared_art if "fbTimer : TON" in l]), 1)
check("shared box: both stores are still made", "xDone := fbTimer.Q;" in shared_st and "xAny := fbTimer.Q OR xManual;" in shared_st)

# The second reader hangs off the pin on a junction, not on a copy of the box
# and not on its name in text: the wire is what says the two readers are the
# same signal.
check("shared box: the pin branches", any(U["T_DOWN"] in l and "xDone" in l for l in shared_art))
check("shared box: the branch reaches the operator", any(U["BL"] in l and "In1" in l for l in shared_art))
check("shared box: the box is not named in text", not any("fbTimer.Q" in l for l in shared_art))

# An operator has no instance name to refer to, and being stateless it costs
# nothing to draw again - so it is never the box a network is joined around.
check("shared box: the operator is still drawn", any("Out1" in l for l in shared_art))


# --- EN and ENO on an operator box -------------------------------------------

# EN decides whether a box runs; it is not one of the things being added. It
# was folded into the operands, so a three-way addition that runs only while
# xEn read as a four-way addition of the enable itself. ENO reports that the
# box ran, and reading it as the box's result made a boolean out of the sum.
enable_st = st_render.render_pou(two_pins)

check("enable: EN is not an operand", "IF xEn THEN iSum := iA + iB + iC; END_IF" in enable_st)
check("enable: no four-way sum survives", not any("xEn + iA" in line for line in enable_st))
check("enable: ENO reports the enable", "xSumOk := xEn;" in enable_st)
check("enable: the ENO store is not itself guarded", not any(line.startswith("IF xEn THEN xSumOk") for line in enable_st))

# A box with no EN wired keeps its plain expression and no guard.
check("enable: an unguarded operator is unchanged", "xAny := fbTimer.Q OR xManual;" in shared_st)


# --- a store that holds: set and reset ---------------------------------------

# storage="set" on an outVariable was dropped, so a latch rendered as
# "xLatched := xTrip;" - text that says the latch clears the moment its input
# drops, where the program holds it.
latch_st = st_render.render_pou(two_pins)
latch_art = fbd_render.render_network(two_pins.networks[1])

check_equal("set: the store is recorded", two_pins.networks[1].outputs[0].storage, "set")
check("set: the ST guards the write", "IF xTrip THEN xLatched := TRUE; END_IF" in latch_st)
check("set: no plain assignment survives", not any("xLatched := xTrip" in line for line in latch_st))
check("set: the arrow is marked", any("(S)> xLatched" in line for line in latch_art))

# The reset counterpart, and the same store written straight onto a block's
# output pin instead of onto a wire.
STORAGE = os.path.join(HERE, "fixtures", "fbd_storage.plcopen.xml")
storage_pou = parse_fbd.parse_pous(STORAGE)[0]
storage_st = st_render.render_pou(storage_pou)
storage_art = fbd_render.render_pou(storage_pou)

check_equal("reset: the store is recorded", storage_pou.networks[0].outputs[0].storage, "reset")
check("reset: the ST guards the write", "IF xClear THEN xLatched := FALSE; END_IF" in storage_st)
check("reset: the arrow is marked", any("(R)> xLatched" in line for line in storage_art))

check_equal("output pin store: recorded on the box", box(storage_pou.networks[1].outputs[0]).stored_outputs["Q"], "set")
check("output pin store: the ST guards the write", "IF tmr.Q THEN xHeld := TRUE; END_IF" in storage_st)
check(
    "output pin store: the pin arrow is marked",
    any("Q" + U["PIN_R"] + U["H"] * 3 + "(S)> xHeld" in line for line in storage_art),
)

# str.center splits an odd remainder on opposite sides under CPython 3 and
# IronPython 2.7, so a box title needing odd padding came out one column
# further right from the dev CLI than from the export CODESYS runs. The two
# have to agree on the byte, or every such line is a phantom diff.
check_equal("centred: the odd space goes right", layout.centred("ab", 5), " ab  ")
check_equal("centred: an even split is unchanged", layout.centred("ab", 6), "  ab  ")
check_equal("centred: no room to centre in", layout.centred("abcd", 3), "abcd")
# The box is 15 columns wide for a 10-character title, so the margin and the
# width are both odd - the one case where CPython puts the extra space on the
# other side from IronPython. Both must produce this line.
check(
    "centred: a title with odd padding sits where CODESYS puts it",
    "             pulse : TP" in storage_art,
)


# --- edge detection on a block pin -------------------------------------------

# edge="rising" on a pin was read by nobody, so a counter that counts once per
# change rendered as one that counts every cycle its input is true. Contacts
# have always carried the marker; the pins had nowhere to put it.
PIN_EDGE = os.path.join(HERE, "fixtures", "36-5-fbd-pin-edge.xml")
pin_edge = parse_fbd.parse_pous(PIN_EDGE)[0]
pin_edge_st = st_render.render_pou(pin_edge)
pin_edge_art = fbd_render.render_network(pin_edge.networks[0])

check_equal("pin edge: the edge reaches the tree", box(pin_edge.networks[0].outputs[0].source).inputs[0][1].edge, "rising")
check("pin edge: the ST shows the trigger", "ctr(CU := R(xPulse), RESET := xRst);" in pin_edge_st)
check("pin edge: the diagram marks the pin", any("R(xPulse)" in line for line in pin_edge_art))
check("pin edge: an unmarked pin stays unmarked", not any("R(xRst)" in line for line in pin_edge_st))


# --- a network that holds only a comment -------------------------------------

# A network with no logic in it was dropped, and its comment then attached to
# the next network - so the file showed one network numbered 1 carrying the
# second network's comment. Every number after a dropped network is wrong,
# and a reviewer opening "Network 5" in CODESYS reads different logic under
# "(* Network 5 *)" in the file.
COMMENT_ONLY = os.path.join(HERE, "fixtures", "36-6-fbd-comment-only-network.xml")
comment_only = parse_fbd.parse_pous(COMMENT_ONLY)[0]
comment_only_art = fbd_render.render_pou(comment_only)

check_equal("comment-only: two networks", len(comment_only.networks), 2)
check_equal("comment-only: the first has no logic", len(comment_only.networks[0].outputs), 0)
check(
    "comment-only: the first keeps its own comment",
    comment_only.networks[0].comment.startswith("// Section header: E-STOP CHAIN"),
)
check_equal("comment-only: the second keeps its own", comment_only.networks[1].comment, "// second network comment")
check_equal(
    "comment-only: the numbering follows the editor",
    [line for line in comment_only_art if line.startswith("(* Network")],
    ["(* Network 1: Title of network one *)", "(* Network 2: Title of network two *)"],
)

# The title is a second field CODESYS draws above the comment, and can be the
# only description a network has. It was skipped with the rest of the
# vendorElements. It heads the network, so it goes on the number line and the
# comment follows it, in the order the editor shows them.
check_equal("comment-only: titles are read", comment_only.networks[0].title, "Title of network one")
check_equal(
    "comment-only: the title heads the network and the comment follows",
    comment_only_art[comment_only_art.index("(* Network 1: Title of network one *)") + 1],
    "(* Section header: E-STOP CHAIN (documentation-only network) *)",
)


# --- a shared box read through two different pins ----------------------------

# A timer whose ET feeds a store and whose Q feeds an OR box. The readers were
# stacked in the order the export listed them and hung off one junction
# column, so the second reader took whatever row the first left free: the OR
# box was wired from the ET row while the ST said tmr.Q, and with the readers
# the other way round ET was drawn into the Q column. A reader sits level with
# the pin it reads, and readers of different pins get a column each.
TWO_READERS = os.path.join(HERE, "fixtures", "r2-1-fbd-shared-box-q-and-et.xml")
TWO_READERS_SWAPPED = os.path.join(HERE, "fixtures", "r2-1-fbd-shared-box-et-and-q.xml")


def wire_rows(art):
    """The row of each wire: Q into the OR box, and ET out to its store."""
    q_rows = [row for row, line in enumerate(art) if "Q" + U["PIN_R"] in line]
    et_rows = [row for row, line in enumerate(art) if "ET" + U["PIN_R"] in line]
    or_rows = [row for row, line in enumerate(art) if U["PIN_L"] + "In1   Out1" in line]
    store_rows = [row for row, line in enumerate(art) if line.rstrip().endswith("> tElapsed")]
    return q_rows, et_rows, or_rows, store_rows


for order, path in (("Q and ET", TWO_READERS), ("ET and Q", TWO_READERS_SWAPPED)):
    pou_two = parse_fbd.parse_pous(path)[0]
    st_two = st_render.render_pou(pou_two)
    art_two = fbd_render.render_network(pou_two.networks[0])
    q_rows, et_rows, or_rows, store_rows = wire_rows(art_two)

    check_equal(order + ": one box is drawn", len([line for line in art_two if "tmr : TON" in line]), 1)
    check("st " + order + ": the OR reads Q", "xAny := tmr.Q OR xManual;" in st_two)
    check("st " + order + ": the store reads ET", "tElapsed := tmr.ET;" in st_two)
    check_equal(order + ": Q leaves the box on one row", len(q_rows), 1)
    check_equal(order + ": ET leaves the box on one row", len(et_rows), 1)
    # The wire into the OR box is the one leaving Q: the same row, unbroken.
    check_equal(order + ": the OR box is wired from the Q row", or_rows, q_rows)
    check(
        order + ": the Q wire runs straight into the OR box",
        "Q" + U["PIN_R"] in art_two[q_rows[0]]
        and set(art_two[q_rows[0]].split("Q" + U["PIN_R"])[1].split(U["PIN_L"] + "In1")[0]) == set([U["H"]]),
    )
    # The store cannot sit level with ET, because the OR box is in the way; so
    # ET's wire turns down a column of its own and the store hangs off that.
    check(order + ": the ET wire turns down its own column", "ET" + U["PIN_R"] + U["H"] * 2 + U["TR"] in art_two[et_rows[0]])
    check_equal(order + ": the store hangs below the ET row", len(store_rows) == 1 and store_rows[0] > et_rows[0], True)
    check(order + ": the store is fed from the ET column", art_two[store_rows[0]].lstrip().startswith(U["BL"]))
    check(order + ": the ET row does not feed the OR box", U["PIN_L"] + "In1" not in art_two[et_rows[0]])
    check(order + ": no junction between the two pins", not any(U["T_DOWN"] in line for line in art_two))

check_equal(
    "shared pins: the drawing does not depend on the order of the readers",
    fbd_render.render_network(parse_fbd.parse_pous(TWO_READERS)[0].networks[0]),
    fbd_render.render_network(parse_fbd.parse_pous(TWO_READERS_SWAPPED)[0].networks[0]),
)

# An output that reads nothing from the shared box was stacked with the
# readers, and being first it was placed at row 0 - beside the title. It is a
# drawing of its own, and goes below the joined one.
aside_timer = Call("TON", "tmr", inputs=[("IN", Signal("xStart"))], outputs=[("Q", None), ("ET", None)])
aside_timer.wired_outputs.add("Q")
aside = Network(
    "",
    [
        Assign("xOther", Signal("xIn")),
        Assign("xDone", OutputRef(aside_timer, "Q")),
        Assign("xAny", Call("OR", inputs=[("In1", OutputRef(aside_timer, "Q")), ("In2", Signal("xManual"))], outputs=[("Out1", None)])),
    ],
)
aside_art = fbd_render.render_network(aside)
check_equal("aside: the title row holds the title alone", aside_art[0].strip(), "tmr : TON")
check("aside: the plain store goes below the joined drawing", aside_art[-1].rstrip().endswith("> xOther"))
check("aside: the joined drawing is still branched", any(U["T_DOWN"] in line and "xDone" in line for line in aside_art))


# --- an EXECUTE box whose ENO pin is wired -----------------------------------

# The body was printed only when the network's own output was the EXECUTE
# call. Wire its ENO to a variable and the output is a store, so the box was
# drawn - an empty rectangle - and the two lines of ST inside it were gone.
ENO_WIRED = os.path.join(HERE, "fixtures", "r2-2-fbd-execute-eno-wired.xml")
eno = parse_fbd.parse_pous(ENO_WIRED)[0]
eno_st = st_render.render_pou(eno)
eno_art = fbd_render.render_network(eno.networks[0])

check("execute eno: the box is drawn", any(line.strip() == "EXECUTE" for line in eno_art))
check("execute eno: the wire to the store is drawn", any("ENO" + U["PIN_R"] + U["H"] * 3 + "> xRan" in line for line in eno_art))
check_equal("execute eno: the body follows the diagram", eno_art[-2:], ["    a := 1;", "    b := 2;"])
check_equal("execute eno: a blank line separates the body", eno_art[-3], "")
check_equal("execute eno: the body is printed once", len([line for line in eno_art if line.strip() == "a := 1;"]), 1)
check("execute eno: the ST guards the body with EN", "IF xRun THEN" in eno_st and "    a := 1;" in eno_st)
check("execute eno: the ENO store reads the enable", "xRan := xRun;" in eno_st)

# The same box behind another box: still found, still printed once, and a
# box two outputs share is not printed per output.
deep_execute = Call("EXECUTE", inputs=[("EN", Signal("xRun"))], outputs=[("ENO", None)], st_code=["c := 3;"])
deep_execute.wired_outputs.add("ENO")
deep = Network(
    "",
    [
        Assign("xBoth", Call("AND", inputs=[("In1", OutputRef(deep_execute, "ENO")), ("In2", Signal("xOk"))], outputs=[("Out1", None)])),
        Assign("xRan", OutputRef(deep_execute, "ENO")),
    ],
)
deep_art = fbd_render.render_network(deep)
check_equal("execute deep: the body of a nested box is printed once", len([line for line in deep_art if line.strip() == "c := 3;"]), 1)
check_equal("execute deep: it follows the diagram", deep_art[-1], "    c := 3;")


# --- one expression reading two pins of a shared box -------------------------

# xAlarm := ctr.Q AND (ctr.CV > 5). Each read of the shared box was replaced
# by a marker byte while the branch was composed, and only the first marker
# was resolved: the second stayed in the file as a control character, and
# the CV pin had no wire. Every read is a wire from its own pin now, and the
# file holds no byte below a space.
CONTROL_CHARACTERS = [chr(code) for code in range(1, 32)]


def control_free(lines):
    return not any(character in line for line in lines for character in CONTROL_CHARACTERS)


TWO_PINS_ONE_READER = os.path.join(HERE, "fixtures", "r2-3-fbd-counter-q-and-cv-in-one-expression.xml")
two_reads = parse_fbd.parse_pous(TWO_PINS_ONE_READER)[0]
two_reads_st = st_render.render_pou(two_reads)
two_reads_art = fbd_render.render_network(two_reads.networks[0])

check("two reads: no control character in the output", control_free(two_reads_art))
check("two reads: the ST reads both pins", "xAlarm := ctr.Q AND (ctr.CV > 5);" in two_reads_st)
check_equal("two reads: one box is drawn", len([line for line in two_reads_art if "ctr : CTU" in line]), 1)
check("two reads: the box is not named in text", not any("ctr." in line for line in two_reads_art))
q_line = [line for line in two_reads_art if "Q" + U["PIN_R"] in line][0]
cv_line = [line for line in two_reads_art if "CV" + U["PIN_R"] in line][0]
check("two reads: Q is wired straight into the AND box", U["PIN_L"] + "In1   Out1" + U["PIN_R"] + U["H"] * 3 + "> xAlarm" in q_line)
check("two reads: CV is wired, down a column of its own", "CV" + U["PIN_R"] + U["H"] * 2 + U["TR"] in cv_line)
gt_lines = [line for line in two_reads_art if line.lstrip().startswith(U["BL"]) and U["PIN_L"] + "In1   Out1" in line]
check_equal("two reads: the CV column feeds the GT box", len(gt_lines), 1)
check("two reads: the GT box feeds In2 of the AND box", gt_lines and U["PIN_L"] + "In2" in gt_lines[0])

# The same two reads the other way up: (ctr.CV > 5) AND ctr.Q puts the CV
# read above the Q read, where a wire from CV would have to cross the wire
# from Q. Then the first read keeps its wire and the second is named.
crossing_counter = Call("CTU", "ctr", inputs=[("CU", Signal("xPulse")), ("PV", Signal("10"))], outputs=[("Q", None), ("CV", None)])
crossing_counter.wired_outputs.update(["Q", "CV"])
crossing_gt = Call("GT", inputs=[("In1", OutputRef(crossing_counter, "CV")), ("In2", Signal("5"))], outputs=[("Out1", None)], wired_outputs=["Out1"])
crossing_and = Call("AND", inputs=[("In1", crossing_gt), ("In2", OutputRef(crossing_counter, "Q"))], outputs=[("Out1", None)], wired_outputs=["Out1"])
crossing = Network("", [Assign("xAlarm", crossing_and)])
crossing_art = fbd_render.render_network(crossing)
check("crossing reads: no control character in the output", control_free(crossing_art))
check_equal("crossing reads: one box is drawn", len([line for line in crossing_art if "ctr : CTU" in line]), 1)
check("crossing reads: the first read is wired", any("CV" + U["PIN_R"] + U["H"] in line and U["PIN_L"] + "In1   Out1" in line for line in crossing_art))
check("crossing reads: the second read is named", any("ctr.Q" + U["H"] * 2 in line and U["PIN_L"] + "In2" in line for line in crossing_art))
check("crossing reads: no wire runs from Q", not any("Q" + U["PIN_R"] + U["H"] in line for line in crossing_art))


# --- a fan-out spread across two pins ----------------------------------------

# A timer whose Q feeds two stores and whose ET feeds a third. Every reader
# hangs straight off the box, so _shared_source claimed it and _render_fanout
# stacked all three in one column: ET, pushed past Q's second reader, landed
# on the box's bottom border and its wire ran out of the "corner". A shared
# instance read across more than one pin now goes through the joined
# renderer, which gives each pin a column of its own.
TWO_PIN_FANOUT = os.path.join(HERE, "fixtures", "fbd-fanout-two-pins.xml")
tpf = parse_fbd.parse_pous(TWO_PIN_FANOUT)[0]
tpf_st = st_render.render_pou(tpf)
tpf_art = fbd_render.render_network(tpf.networks[0])

check_equal("two-pin fanout: one box is drawn", len([l for l in tpf_art if "tmr : TON" in l]), 1)
check_equal("two-pin fanout: the timer is called once", len([l for l in tpf_st if l.startswith("tmr(")]), 1)
check("two-pin fanout: Q reaches both stores", "xA := tmr.Q;" in tpf_st and "xB := tmr.Q;" in tpf_st)
check("two-pin fanout: ET reaches its store", "tC := tmr.ET;" in tpf_st)
# The defect: a wire running straight out of the box's bottom-right corner.
check("two-pin fanout: no wire leaves the bottom border", not any(U["BR"] + U["H"] in l for l in tpf_art))
# Q teed to two readers, ET on its own row to its store.
check("two-pin fanout: Q branches to two readers", any("Q" + U["PIN_R"] in l and U["T_DOWN"] in l for l in tpf_art))
check("two-pin fanout: ET turns down its own column", any("ET" + U["PIN_R"] in l and U["TR"] in l for l in tpf_art))
check("two-pin fanout: every store is reached", all(any(name in l for l in tpf_art) for name in ("xA", "xB", "tC")))


# --- a store written on an operator's output pin -----------------------------

# The MOVE-with-EN shape: an operator gated by EN, its result written straight
# onto an output pin. The operator branch returned its expression before the
# output-pin loop, so the store was dropped from the ST - the diagram drew the
# wire, the ST said nothing. The store now appears, guarded by EN.
move = Call("MOVE", inputs=[("EN", Signal("xCond")), ("In", Signal("iSrc"))], outputs=[("ENO", None), ("Out", "iDst")])
move_st = st_render.network_to_statements(Network("", [move]))
check("operator store: the guarded store is emitted", "IF xCond THEN iDst := MOVE(iSrc); END_IF" in move_st)

add = Call("ADD", inputs=[("EN", Signal("xEn")), ("In1", Signal("iA")), ("In2", Signal("iB"))], outputs=[("ENO", None), ("Out1", "iSum")])
add_st = st_render.network_to_statements(Network("", [add]))
check("operator store: the sum is stored under its guard", "IF xEn THEN iSum := iA + iB; END_IF" in add_st)

# A bubble on Out1 while ENO is listed first: the box's active output is ENO,
# so the negation used to be looked for on the wrong pin and lost. The bubble
# is on the pin the reader takes.
neg_out = Call("ADD", inputs=[("EN", Signal("xEn")), ("In1", Signal("iA")), ("In2", Signal("iB"))],
               outputs=[("ENO", None), ("Out1", None)], negated_outputs=set(["Out1"]), wired_outputs=["Out1"])
neg_out_st = st_render.network_to_statements(Network("", [Assign("iSum", OutputRef(neg_out, "Out1"))]))
check("operator negate: a negated Out1 inverts though ENO is first", "IF xEn THEN iSum := NOT (iA + iB); END_IF" in neg_out_st)

# A negated ENO reports the inverse of the enable.
neg_eno = Call("ADD", inputs=[("EN", Signal("xEn")), ("In1", Signal("iA")), ("In2", Signal("iB"))],
               outputs=[("ENO", None), ("Out1", None)], negated_outputs=set(["ENO"]), wired_outputs=["ENO"])
neg_eno_st = st_render.network_to_statements(Network("", [Assign("ok", OutputRef(neg_eno, "ENO"))]))
check("operator negate: a negated ENO inverts the enable", "ok := NOT xEn;" in neg_eno_st)

# An EXECUTE box whose ENO is stored: the store records that it ran.
exec_eno = Call("EXECUTE", inputs=[("EN", Signal("xRun"))], outputs=[("ENO", "xDid")], st_code=["a := 1;"])
exec_eno_st = st_render.network_to_statements(Network("", [exec_eno]))
check("execute store: the body is guarded", "IF xRun THEN" in exec_eno_st and "    a := 1;" in exec_eno_st)
check("execute store: the ENO store records the run", "xDid := xRun;" in exec_eno_st)


# --- language dispatch -----------------------------------------------------

check_equal("LD parser ignores FBD bodies", parse_ld.parse_pous(FBD_SOURCE), [])
check_equal("FBD parser ignores LD bodies", parse_fbd.parse_pous(LD_SOURCE), [])
check_equal("SFC is skipped by both", parse_ld.parse_pous(SFC_SOURCE) + parse_fbd.parse_pous(SFC_SOURCE), [])

print("")
if failures:
    print("%d check(s) failed" % len(failures))
else:
    print("all checks passed")
sys.exit(1 if failures else 0)
