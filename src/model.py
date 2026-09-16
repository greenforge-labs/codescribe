# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Data model for a Ladder Diagram network.

Two layers live here:

* ``Node`` - a single graphical element exactly as it appears in the PLCopen
  body, still wired by ``localId``. This is a faithful, dumb transcription of
  the XML.
* The ``Expr`` classes - the same logic rearranged into the series/parallel
  tree that a renderer can actually draw. Coordinates are deliberately dropped
  at this point: layout is derived from topology so that nudging a block in the
  CODESYS editor does not churn the diff.
"""

import re

# A bare identifier, member access or literal - something safe to negate or
# nest without brackets. Anything else (operators, calls, spaces) must be
# parenthesised: expressions are free-form ST, often typed without spaces,
# and NOT binds above comparison in IEC 61131-3, so "NOT iCount>5" states
# "(NOT iCount)>5". The % covers direct addresses like %IX0.0.
_SIMPLE_TERM = re.compile(r"^[A-Za-z0-9_.#%]+$")


def is_simple_term(text):
    """True when text can be negated or nested without changing its grouping."""
    return _SIMPLE_TERM.match(text) is not None


# Element kinds we understand. Anything else is carried through as an opaque
# element so unknown logic is visibly wrong rather than silently missing.
LEFT_RAIL = "leftPowerRail"
RIGHT_RAIL = "rightPowerRail"
CONTACT = "contact"
COIL = "coil"
BLOCK = "block"
IN_VARIABLE = "inVariable"
OUT_VARIABLE = "outVariable"
JUMP = "jump"
RETURN = "return"
LABEL = "label"
# Carries no logic, but CODESYS writes one above each network that has a
# comment, so it marks where one network begins.
COMMENT = "comment"
# The network's title, exported as a vendorElement. Also a header, also a
# boundary, and often the only description a network carries.
TITLE = "networktitle"

RAILS = (LEFT_RAIL, RIGHT_RAIL)


class Connection(object):
    """One wire arriving at an element.

    ``source_pin`` is the formalParameter on the *upstream* element's output
    (CODESYS writes ``formalParameter="Q"`` on the connection itself), while
    ``target_pin`` is the input pin on *this* element. Only blocks have named
    pins; for contacts and coils both are None.

    ``negated`` is the bubble CODESYS draws on the *pin itself* (negated="true"
    on the pin's variable element) - separate from a negated inVariable, and
    just as logic-inverting if dropped.

    ``edge`` is the P or N CODESYS draws on the pin: the pin sees a single
    scan when its value changes, not the value itself. A block behind one
    runs once per edge, and reads as running every cycle without it.
    """

    def __init__(self, ref_id, source_pin=None, target_pin=None, negated=False, edge=None):
        self.ref_id = ref_id
        self.source_pin = source_pin
        self.target_pin = target_pin
        self.negated = negated
        self.edge = edge  # "rising" | "falling" | None

    def __repr__(self):
        return "Connection(%s, source_pin=%r, target_pin=%r)" % (self.ref_id, self.source_pin, self.target_pin)


class Node(object):
    """One graphical element from an LD body, still wired by localId."""

    def __init__(
        self,
        local_id,
        kind,
        label=None,
        negated=False,
        edge=None,
        storage=None,
        inputs=None,
        type_name=None,
        instance_name=None,
        outputs=None,
        st_code=None,
        negated_outputs=None,
        stored_outputs=None,
    ):
        self.st_code = st_code if st_code is not None else []  # blocks only: inline ST
        self.local_id = local_id
        self.kind = kind
        self.label = label
        self.negated = negated
        self.edge = edge  # "rising" | "falling" | None
        self.storage = storage  # "set" | "reset" | None
        self.inputs = inputs if inputs is not None else []
        self.type_name = type_name  # blocks only
        self.instance_name = instance_name  # blocks only, absent for operators
        self.outputs = outputs if outputs is not None else []  # blocks only: (pin, assigned_var)
        # blocks only: output pins whose in-place negation bubble inverts the
        # value leaving them
        self.negated_outputs = negated_outputs if negated_outputs is not None else set()
        # blocks only: {pin: "set" | "reset"} for inline assignments that store
        self.stored_outputs = dict(stored_outputs) if stored_outputs is not None else {}
        # blocks only: set by the network builder; see box_name
        self.ordinal = None

    def __repr__(self):
        return "Node(%s, %s, %r, inputs=%r)" % (self.local_id, self.kind, self.label, self.inputs)


def box_name(box):
    """The name a box is written under when the text names it instead of a wire.

    An instance has its own name. A box without one - an operator, or an
    EXECUTE box - is named by its type, and two such boxes of one type in one
    network would then be indistinguishable: rewiring a coil from one to the
    other would change nothing in the export. So where a network holds two or
    more of them and one is named, each carries an ordinal, printed after its
    type in its title and in every reference to it.
    """
    if box.instance_name:
        return box.instance_name
    base = box.type_name or "?"
    if box.ordinal:
        return "%s#%d" % (base, box.ordinal)
    return base


def _numbered_type(box):
    """A box title's type part: 'ADD', or 'ADD #2' when it carries an ordinal."""
    base = box.type_name or "?"
    if box.ordinal:
        return "%s #%d" % (base, box.ordinal)
    return base


def component_finder(nodes):
    """Union-find over the wires, ignoring direction.

    Two outputs fed from one block belong to the same network, so grouping has
    to follow wires backwards as well as forwards. Connections to elements
    outside ``nodes`` are ignored, which is how a caller keeps a shared
    anchor - an LD power rail - from fusing every network into one.
    """
    parent = {}
    for node in nodes:
        parent[node.local_id] = node.local_id

    def find(item):
        root = item
        while parent[root] != root:
            root = parent[root]
        while parent[item] != root:
            parent[item], item = root, parent[item]
        return root

    for node in nodes:
        for connection in node.inputs:
            if connection.ref_id not in parent:
                continue
            left, right = find(node.local_id), find(connection.ref_id)
            if left != right:
                parent[left] = right
    return find


def label_name(tree):
    """The jump target a parsed label carries, or None for anything else.

    FBD parses a label into a Label; LD parses it into an Element whose kind
    says label. The two are different classes, and treating only one of them
    as a label leaves the other in the network's body.
    """
    if isinstance(tree, Label):
        return tree.name
    if isinstance(tree, Element) and tree.kind == LABEL:
        return tree.label
    return None


def _network(header, trees):
    """(comment, title, label, outputs) - the label lifted out of the trees.

    CODESYS keeps one label per network, so a second one cannot come from an
    export; should one arrive it stays in the body, visible, rather than
    being dropped.
    """
    label = ""
    outputs = []
    for tree in trees:
        name = label_name(tree)
        if name is not None and not label:
            label = name
        else:
            outputs.append(tree)
    return (header[0] or "", header[1] or "", label, outputs)


def assemble_networks(nodes, root_of, outputs_by_root, label_roots=()):
    """Order the components of a body into networks, in editor order.

    Returns [(comment, title, label, [outputs])]. Three things decide where
    a network begins and what it is called:

    * A comment or a title element is a header, and heads the network whose
      elements follow it. A second one of either means the header before it
      headed a network of its own - a network holding nothing but
      documentation. Dropping those silently renumbered every network after
      them, so a reviewer opening "Network 5" in CODESYS read different logic
      under "(* Network 5 *)" in the file.
    * A header is not a reliable boundary on its own: CODESYS writes no
      comment element for a network that has none. Connectivity is what
      separates networks; the header only names the one it precedes.
    * A jump label is stored on the network in CODESYS but exported as a
      free-standing element just before it, so it arrives as a component of
      its own. It belongs to the network that follows it - as that network's
      label, not as part of its body. Left in the body it was drawn as a
      rung, and twice over once the native export supplied the label too.
    """
    label_roots = set(label_roots)
    networks = []
    header = [None, None]
    carried = []
    seen = set()

    for node in nodes:
        if node.kind in (COMMENT, TITLE):
            index = 0 if node.kind == COMMENT else 1
            # A header comes before its network's label, so one arriving after a
            # carried label heads the next network: the label's ends here.
            carries_label = any(label_name(tree) is not None for tree in carried)
            if header[index] is not None or carries_label:
                networks.append(_network(header, list(carried)))
                del carried[:]
                header = [None, None]
            header[index] = node.label or ""
            continue

        root = root_of(node)
        if root is None or root in seen or root not in outputs_by_root:
            continue
        seen.add(root)
        if root in label_roots:
            # A network has one label. A second arriving before any logic means
            # the first labelled a network with none, which ends here - carried
            # on, the second label was left in the next network's body.
            if any(label_name(tree) is not None for tree in carried):
                networks.append(_network(header, list(carried)))
                del carried[:]
                header = [None, None]
            carried.extend(outputs_by_root[root])
            continue

        networks.append(_network(header, carried + outputs_by_root[root]))
        del carried[:]
        header = [None, None]

    if header[0] is not None or header[1] is not None or carried:
        networks.append(_network(header, list(carried)))
    return networks


class Variable(object):
    """One entry from the POU interface, for rendering the declaration block."""

    def __init__(self, name, type_name, initial_value=None, scope="VAR"):
        self.name = name
        self.type_name = type_name
        self.initial_value = initial_value
        self.scope = scope


class Pou(object):
    """A parsed POU. ``networks`` holds one entry per network in the editor.

    Both languages fill it: for FBD each network holds the trees driving its
    outputs, for LD the rungs of that network. A network can hold more than
    one of either - a block driving three outputs is one network in the
    editor, and numbering it as three throws every later number out.
    """

    def __init__(self, name, pou_type, variables=None, networks=None, language=None, declaration_text=None):
        self.name = name
        self.pou_type = pou_type
        self.language = language
        # The declaration exactly as CODESYS wrote it, comments, pragmas and
        # attributes included. None when the export did not carry one, in
        # which case it gets rebuilt from `variables` and loses all three.
        self.declaration_text = declaration_text
        self.variables = variables if variables is not None else []
        self.networks = networks if networks is not None else []

    @property
    def rungs(self):
        """Every LD rung in the POU, network grouping flattened away."""
        return [tree for network in self.networks for tree in network.outputs]


# --- FBD tree --------------------------------------------------------------
#
# FBD has no power rail, so there is no single wire to hang a series/parallel
# tree off. A network is instead a tree of calls: each block pin is fed either
# by a named value or by another block's output.


# How an edge-triggered pin reads. The same spelling the LD contacts use, so
# both languages grep alike.
EDGE_FUNCTION = {"rising": "R", "falling": "F"}


class Signal(object):
    """A named value entering a network: a variable, a literal, or nothing.

    CODESYS can negate an inVariable in place, which is easy to miss and
    inverts the logic if it is dropped. ``edge`` is the pin's own P or N: the
    bubble inverts what arrives, and the edge detector then sees that value
    change, so the negation goes inside.
    """

    def __init__(self, label, negated=False, edge=None):
        self.label = label
        self.negated = negated
        self.edge = edge

    @property
    def text(self):
        label = self.label or ""
        if self.negated:
            # A compound expression must keep its parentheses or the logic
            # regroups - see is_simple_term for the precedence trap.
            label = ("NOT " + label) if is_simple_term(label) else ("NOT (" + label + ")")
        function = EDGE_FUNCTION.get(self.edge)
        if function:
            return function + "(" + label + ")"
        return label

    def __repr__(self):
        return "Signal(%r, negated=%r, edge=%r)" % (self.label, self.negated, self.edge)


class Jump(object):
    """A conditional jump to a label. Terminates its network."""

    def __init__(self, target, condition=None):
        self.target = target
        self.condition = condition

    def __repr__(self):
        return "Jump(%r)" % (self.target,)


class Label(object):
    """A jump target. Marks a point in the network order, carries no logic."""

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Label(%r)" % (self.name,)


class Call(object):
    """An FBD block call - a box with named input and output pins.

    ``inputs`` is [(pin_name, source)] where source is a Call, a Signal or
    None. ``outputs`` is [(pin_name, assigned_variable)]. Pin order is kept
    exactly as exported; unlike LD there is no power pin to hoist.
    """

    def __init__(
        self,
        type_name=None,
        instance_name=None,
        inputs=None,
        outputs=None,
        active_output=None,
        wired_outputs=None,
        st_code=None,
        negated_outputs=None,
        stored_outputs=None,
    ):
        self.type_name = type_name
        self.instance_name = instance_name
        self.inputs = inputs if inputs is not None else []
        self.outputs = outputs if outputs is not None else []
        # The pin a reader gets when it does not name one. Which pin a given
        # reader takes lives on the reader, in an OutputRef.
        if active_output is None and self.outputs:
            active_output = self.outputs[0][0]
        self.active_output = active_output
        # Pins carrying CODESYS's in-place negation bubble: the value leaving
        # them is the inverse of the pin.
        self.negated_outputs = negated_outputs if negated_outputs is not None else set()
        # {pin: "set" | "reset"} for inline assignments that store instead of
        # assigning outright.
        self.stored_outputs = dict(stored_outputs) if stored_outputs is not None else {}
        # An EXECUTE box carries inline ST as its whole body. Dropping it loses
        # the logic entirely while still drawing a plausible-looking box.
        self.st_code = st_code if st_code is not None else []
        # Every output pin something downstream reads. A network sink reads
        # none; a block read through two of its pins has two, and is still one
        # box, called once.
        self.wired_outputs = set(wired_outputs) if wired_outputs is not None else set()
        # Set by the renderer; see box_name.
        self.ordinal = None

    @property
    def output_wired(self):
        """True when anything downstream reads an output of this call."""
        return bool(self.wired_outputs)

    @property
    def title(self):
        if self.instance_name:
            return self.instance_name + " : " + (self.type_name or "?")
        return _numbered_type(self)

    @property
    def is_operator(self):
        """Operators and functions have no instance, so they inline as expressions."""
        return not self.instance_name

    def __repr__(self):
        return "Call(%r, %r)" % (self.type_name, self.instance_name)


class OutputRef(object):
    """The value on one output pin of a Call, as read by its consumer.

    The pin belongs to the wire, not to the box. Holding it on the Call meant
    a block read through two pins was two Calls: drawn twice, and called twice
    in the ST, so a reader concluded a stateful block ran twice per cycle.
    """

    def __init__(self, call, pin):
        self.call = call
        self.pin = pin

    def __repr__(self):
        return "OutputRef(%r, %r)" % (self.call, self.pin)


class Network(object):
    """One FBD network: a comment, and the outputs its logic drives.

    A network can drive several outputs from shared logic - CODESYS draws that
    as one box with the wire branching. Treating each output as its own
    network duplicates the shared expression and makes the numbering disagree
    with the editor, which is what a reviewer compares against.
    """

    def __init__(self, comment="", outputs=None, title="", label="", note=None):
        self.comment = comment
        # CODESYS keeps a network's title separately from its comment, and
        # draws it above one. A network can carry either, both or neither.
        self.title = title
        # The jump-target label CODESYS keeps on the network. PLCopen writes
        # it as a loose element just before the network's body, and the
        # parser lifts it back here; the native export carries it as the
        # property it is, and that one is taken in preference.
        self.label = label
        # Why this network has no body: out-commented, or empty. Set only for
        # networks the PLCopen export left out entirely.
        self.note = note
        self.outputs = outputs if outputs is not None else []

    def __repr__(self):
        return "Network(%r, %r, %d outputs)" % (self.comment, self.title, len(self.outputs))


class Assign(object):
    """An outVariable: a network whose result is stored into a variable.

    Like an inVariable, CODESYS can negate the pin in place - and dropping
    that inverts the stored value.
    """

    def __init__(self, label, source=None, negated=False, storage=None):
        self.label = label
        self.source = source
        self.negated = negated
        # "set" | "reset" | None. A stored value is held until something
        # resets it; rendering one as a plain assignment says it clears as
        # soon as its condition drops, which is the opposite of the program.
        self.storage = storage

    def __repr__(self):
        return "Assign(%r, negated=%r, storage=%r)" % (self.label, self.negated, self.storage)


# --- expression tree -------------------------------------------------------


class Empty(object):
    """A wire with nothing on it - an unconditional rung, or a bare rail."""

    def __eq__(self, other):
        return isinstance(other, Empty)

    def __repr__(self):
        return "Empty()"


class Element(object):
    """A drawable leaf: contact, coil, block call, jump.

    For blocks, ``input_pins`` and ``output_pins`` are lists of
    ``(pin_name, label)``. A label of None marks the pin carrying power flow -
    the one wired into the rung rather than fed from a literal or a side
    branch. That pin is always sorted first so the wire runs straight through.
    """

    def __init__(
        self,
        kind,
        label=None,
        negated=False,
        edge=None,
        storage=None,
        type_name=None,
        instance_name=None,
        input_pins=None,
        output_pins=None,
        active_output=None,
        output_wired=False,
        power_negated=False,
        power_edge=None,
        negated_outputs=None,
        stored_outputs=None,
        pin_blocks=None,
        st_code=None,
        pin_feeds=None,
        pin_marks=None,
        local_id=None,
        ordinal=None,
        power_len=0,
        copy=0,
    ):
        self.kind = kind
        # Blocks only: 0 for the first copy of the box the parser built, 1 for
        # the next, and so on. Only the first carries the instance boxes
        # upstream of it; a later copy names them. See ld_render._keep_first.
        self.copy = copy
        # Blocks only; see box_name.
        self.ordinal = ordinal
        # Blocks only: how many items directly before the box in its rung are
        # the wire that powers it. A later copy of the box is replaced by a
        # reference, and that wire goes with it, since it belongs to the box.
        self.power_len = power_len
        # The localId of the PLCopen node this element was built from. The
        # parser builds one branch per sink, so one node can arrive as several
        # copies; this is what says they are one element in the editor. Two
        # nodes that draw the same are still two elements.
        self.local_id = local_id
        self.label = label
        self.negated = negated
        self.edge = edge
        self.storage = storage
        self.type_name = type_name
        self.instance_name = instance_name
        self.input_pins = input_pins if input_pins is not None else []
        self.output_pins = output_pins if output_pins is not None else []
        self.active_output = active_output
        # Blocks only: the negation bubble on the pin the rung's power enters
        # through, and the set of output pins carrying one. Both invert the
        # logic in place if dropped.
        self.power_negated = power_negated
        # The P or N on that same pin: the block runs once per edge, not once
        # per scan the condition holds.
        self.power_edge = power_edge
        self.negated_outputs = negated_outputs if negated_outputs is not None else set()
        # {pin: "set" | "reset"} for inline assignments that store instead of
        # assigning outright.
        self.stored_outputs = dict(stored_outputs) if stored_outputs is not None else {}
        # True when something downstream actually consumes the active output,
        # so the renderer knows whether to break the box edge with a tee.
        self.output_wired = output_wired
        # Blocks only: whole sub-rungs feeding this block's side pins. A box
        # wired into a side pin has a call of its own to make, with its own
        # inputs; the pin caption only names the output it reads. They are
        # rendered and emitted before this block, in the order the pins were
        # wired, because that is the order they execute in.
        self.pin_blocks = pin_blocks if pin_blocks is not None else []
        # An EXECUTE box carries inline ST as its whole body. Drawing the box
        # without it leaves an empty rectangle where the logic should be.
        self.st_code = st_code if st_code is not None else []
        # Blocks only: {pin: expression} for a side pin fed by a contact chain.
        # A contact reset or enable is drawn as the contact it is, wired into
        # the pin, rather than flattened into the pin caption as text.
        self.pin_feeds = pin_feeds if pin_feeds is not None else {}
        # Blocks only: {pin: (negated, edge)} for a drawn-contact side pin that
        # carries a bubble or a P/N of its own. The caption form spells those
        # out in its text; a drawn contact needs them put on the box wall.
        self.pin_marks = pin_marks if pin_marks is not None else {}

    @property
    def title(self):
        """Caption drawn above a block: 'TON_0 : TON', or just 'GT'."""
        if self.instance_name:
            return self.instance_name + " : " + (self.type_name or "?")
        if self.type_name:
            return _numbered_type(self)
        return self.label or "?"

    def __repr__(self):
        return "Element(%s, %r)" % (self.kind, self.label)


class Series(object):
    """Elements wired left to right - logical AND."""

    def __init__(self, items):
        self.items = items

    def __repr__(self):
        return "Series(%r)" % (self.items,)


class Parallel(object):
    """Branches wired top to bottom - logical OR."""

    def __init__(self, branches):
        self.branches = branches

    def __repr__(self):
        return "Parallel(%r)" % (self.branches,)


def series(items):
    """Build a Series, flattening nested ones and dropping Empty legs."""
    flat = []
    for item in items:
        if isinstance(item, Empty):
            continue
        if isinstance(item, Series):
            flat.extend(item.items)
        else:
            flat.append(item)
    if not flat:
        return Empty()
    if len(flat) == 1:
        return flat[0]
    return Series(flat)


def parallel(branches):
    """Build a Parallel, collapsing the single-branch case."""
    if not branches:
        return Empty()
    if len(branches) == 1:
        return branches[0]
    return Parallel(branches)
