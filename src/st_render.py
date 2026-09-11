# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Emit equivalent Structured Text for LD and FBD networks.

The ASCII renderers preserve the shape of the diagram; this preserves the
logic and throws the shape away. It is the better of the two for review: it
diffs line by line, it greps, and reviewers already read ST.

It is a rendering, not a translation - the output is not guaranteed to compile
and must never be fed back into CODESYS. Notably a coil is transparent to
power flow, so the condition carries on past it, which reads oddly in ST but
matches what the rung does.
"""

from ld_render import network_headers, render_declaration
from model import (
    BLOCK,
    COIL,
    JUMP,
    LABEL,
    OUT_VARIABLE,
    RETURN,
    Assign,
    Call,
    Element,
    Jump,
    Label,
    OutputRef,
    Series,
    Signal,
    is_simple_term,
)
from parse_ld import expr_to_text, pin_value


def store_statement(target, value, storage=None, negated=False):
    """One store, however it is drawn: coil, outVariable or output pin.

    A set or reset holds its target until the other one fires, so it has to
    read as a guarded write. Emitting "xLatched := xTrip;" for a set says the
    latch clears the moment its input drops, which is the opposite of what
    the program does.
    """
    value = value or "TRUE"
    target = target or "?"
    if negated:
        value = "NOT " + _operand(value)
    if storage == "set":
        return "IF %s THEN %s := TRUE; END_IF" % (value, target)
    if storage == "reset":
        return "IF %s THEN %s := FALSE; END_IF" % (value, target)
    return "%s := %s;" % (target, value)


def _coil_statement(coil, condition):
    if coil.negated and not coil.storage:
        # A negated coil stores the inverse of the whole rung condition, and
        # brackets it rather than negating only its first term.
        return "%s := NOT (%s);" % (coil.label or "?", condition or "TRUE")
    return store_statement(coil.label, condition, coil.storage)


def rung_to_statements(rung):
    """One rung to a list of ST statements, walking the power flow left to right."""
    items = rung.items if isinstance(rung, Series) else [rung]
    statements = []
    condition = None

    for item in items:
        if isinstance(item, Element) and item.kind == BLOCK:
            # A box wired into one of this box's side pins runs first and has
            # inputs of its own to state. It is a sub-rung with its own power
            # flow, so it walks the same way rather than folding into this
            # rung's condition.
            for pin_block in item.pin_blocks:
                statements.extend(rung_to_statements(pin_block))
            if item.st_code:
                # An EXECUTE box is inline ST already, and the rung condition
                # is what decides whether it runs. Emitting a call to a box
                # that has no body loses the whole of it. The bubble and the
                # P or N on the EN pin gate it just as they gate any other
                # block, so a negated EN inverts the guard and a bare rail
                # with a negated EN never runs it.
                guard = condition
                if item.power_negated or item.power_edge:
                    guard = pin_value(condition or "TRUE", item.power_negated, item.power_edge)
                if guard:
                    statements.append("IF %s THEN" % guard)
                    statements.extend("    " + line for line in item.st_code)
                    statements.append("END_IF")
                else:
                    statements.extend(item.st_code)
                continue
            args = []
            for pin, label in item.input_pins:
                # A label of None is the power pin, fed by the rung so far.
                value = condition if label is None else label
                if label is None and (item.power_negated or item.power_edge):
                    # The bubble and the P or N on the power pin itself. A
                    # bare rail feed has no condition, but the markers must
                    # still be stated or the ST reads as an unmarked level.
                    value = pin_value(value or "TRUE", item.power_negated, item.power_edge)
                if value:
                    args.append("%s := %s" % (pin, value))
            name = item.instance_name or item.type_name or "?"
            statements.append("%s(%s);" % (name, ", ".join(args)))
            # An assignment written straight onto an output pin executes every
            # scan; the diagram draws it, so the ST must say it too. A negated
            # pin stores its inverse.
            for pin, assigned in item.output_pins:
                if assigned:
                    value = "%s.%s" % (name, pin)
                    if pin in item.negated_outputs:
                        value = "NOT " + value
                    statements.append(store_statement(assigned, value, item.stored_outputs.get(pin)))
            condition = (name + "." + item.active_output) if item.active_output else name
            if item.active_output in item.negated_outputs:
                condition = "NOT " + condition
        elif isinstance(item, Element) and item.kind == COIL:
            statements.append(_coil_statement(item, condition))
        elif isinstance(item, Element) and item.kind == OUT_VARIABLE:
            # A store through an outVariable element - the standard shape for
            # a non-boolean result. Power passes through, like a coil, and so
            # does the set/reset a coil can carry.
            statements.append(store_statement(item.label, condition, item.storage, item.negated))
        elif isinstance(item, Element) and item.kind in (JUMP, RETURN):
            # A jump ends the rung; its guard is the rung condition so far.
            # Written as CODESYS ST writes it, like the label it targets:
            # inside (* *) it would read as a note about the program rather
            # than as the thing that decides what runs next.
            statement = ("JMP " + (item.label or "?") + ";") if item.kind == JUMP else "RETURN;"
            if condition:
                statements.append("IF %s THEN %s END_IF" % (condition, statement))
            else:
                statements.append(statement)
        elif isinstance(item, Element) and item.kind == LABEL:
            statements.append("%s:" % (item.label or "?"))
        else:
            text = expr_to_text(item)
            if text:
                condition = text if condition is None else condition + " AND " + text

    return statements


# Operators CODESYS draws as boxes but everyone reads as infix. A conversion
# like REAL_TO_UINT is left as a call, because that is how it reads in ST too.
INFIX_OPERATORS = {
    "AND": "AND",
    "OR": "OR",
    "XOR": "XOR",
    "ADD": "+",
    "SUB": "-",
    "MUL": "*",
    "DIV": "/",
    "MOD": "MOD",
    "GT": ">",
    "GE": ">=",
    "LT": "<",
    "LE": "<=",
    "EQ": "=",
    "NE": "<>",
}


def _operand(text):
    """Parenthesise anything that is not a single term.

    Redundant brackets are preferable to an expression that reads correctly
    but groups wrongly - and "iCount>5" is as compound as "xA OR xB", see
    is_simple_term.
    """
    return text if is_simple_term(text) else "(" + text + ")"


# The enable pair CODESYS draws on a box. EN decides whether the box runs at
# all and ENO reports that it did; neither is an operand, and neither is the
# box's result.
EN_PIN = "EN"
ENO_PIN = "ENO"


def _enable(call, statements, emitted):
    """The EN pin's value as text, or None when the box has no live enable.

    Re-reading the pin is safe: a call is memoised in ``emitted``, so asking
    for its value again returns the same text without emitting the call a
    second time, and a signal has nothing to emit.
    """
    for pin, source in call.inputs:
        if pin != EN_PIN:
            continue
        text = _fbd_value(source, statements, emitted)
        # A box wired to a constant TRUE is a box with no enable worth stating.
        return None if text in (None, "", "TRUE") else text
    return None


def _operator_expression(node, values):
    symbol = INFIX_OPERATORS.get(node.type_name)
    if symbol and len(values) >= 2:
        return (" " + symbol + " ").join(_operand(value) for value in values)
    if node.type_name == "NOT" and len(values) == 1:
        return "NOT " + _operand(values[0])
    return "%s(%s)" % (node.type_name or "?", ", ".join(values))


def _fbd_value(node, statements, emitted=None):
    """Value of a node as ST text, appending any statements it needs first.

    ``emitted`` maps an already-rendered node to its value, so a block
    feeding two outputs is called once rather than once per output.
    """
    if emitted is None:
        emitted = {}
    if node is None:
        return ""

    if isinstance(node, OutputRef):
        # The call is emitted once however many of its pins are read; only the
        # value differs per reader, so it is computed here rather than
        # memoised with the call.
        value = _fbd_value(node.call, statements, emitted)
        if node.call.is_operator:
            if node.pin == ENO_PIN:
                # ENO says the box ran, which is what its EN said. It is not
                # the result: reading it as the expression made "xSumOk := iA
                # + iB + iC;" out of a boolean that only says whether the add
                # ran.
                result = _enable(node.call, statements, emitted) or "TRUE"
            else:
                # An operator has no instance to take a pin from; it inlines
                # as the one expression whichever pin reads it.
                result = value
            # The bubble is on the pin being read, not on whichever pin the
            # box calls its active output - a box that lists ENO first still
            # inverts a negated Out1.
            if node.pin in node.call.negated_outputs:
                result = "NOT " + _operand(result)
            return result
        if not node.pin:
            return value
        text = "%s.%s" % (node.call.instance_name, node.pin)
        if node.pin in node.call.negated_outputs:
            text = "NOT " + text
        return text

    if isinstance(node, Signal):
        return node.text

    if isinstance(node, Label):
        statements.append("%s:" % node.name)
        return ""

    if isinstance(node, Jump):
        condition = _fbd_value(node.condition, statements, emitted)
        # A return arrives here as a jump to "RETURN"; RETURN is a reserved
        # word, so no label can be called that and the two cannot be confused.
        statement = "RETURN;" if node.target == "RETURN" else ("JMP " + (node.target or "?") + ";")
        if condition:
            statements.append("IF %s THEN %s END_IF" % (condition, statement))
        else:
            statements.append(statement)
        return ""

    if isinstance(node, Assign):
        value = _fbd_value(node.source, statements, emitted) or "FALSE"
        statement = store_statement(node.label, value, node.storage, node.negated)
        guard = _assign_guard(node.source, statements, emitted)
        if guard:
            # An operator behind an EN pin computes only while EN holds, and
            # an expression has nowhere to say so - the store it feeds does.
            statement = "IF %s THEN %s END_IF" % (guard, statement)
        statements.append(statement)
        return node.label or "?"

    if isinstance(node, Call):
        if id(node) in emitted:
            return emitted[id(node)]
        pairs = []
        for pin, source in node.inputs:
            value = _fbd_value(source, statements, emitted)
            if value:
                pairs.append((pin, value))

        def remember(value):
            emitted[id(node)] = value
            return value

        if node.st_code:
            # An EXECUTE box is inline ST already, so emit it as itself rather
            # than as a call to a box that has no body.
            guard = dict(pairs).get("EN")
            if guard and guard != "TRUE":
                statements.append("IF %s THEN" % guard)
                statements.extend("    " + line for line in node.st_code)
                statements.append("END_IF")
            else:
                statements.extend(node.st_code)
            # A store written on the ENO pin records that the box ran, which
            # is what its EN said. Dropping it lost the assignment entirely.
            for pin, assigned in node.outputs:
                if assigned and pin == ENO_PIN:
                    reported = guard or "TRUE"
                    if pin in node.negated_outputs:
                        reported = "NOT " + _operand(reported)
                    statements.append(store_statement(assigned, reported, node.stored_outputs.get(pin)))
            return remember("")

        if node.is_operator:
            # Operators and functions have no instance to call, so they inline
            # as an expression rather than a statement. EN is not one of the
            # operands: folding it in made "iSum := xEn + iA + iB + iC;" out
            # of a three-way addition that runs only while xEn.
            expression = _operator_expression(node, [value for pin, value in pairs if pin != EN_PIN])
            # A store written straight onto an output pin - the MOVE-with-EN
            # shape - executes while EN holds. It was dropped: the operator
            # returned before this loop, so the assignment never appeared.
            guard = _enable(node, statements, emitted)
            for pin, assigned in node.outputs:
                if not assigned:
                    continue
                if pin == ENO_PIN:
                    stored = _enable(node, statements, emitted) or "TRUE"
                else:
                    stored = expression
                if pin in node.negated_outputs:
                    stored = "NOT " + _operand(stored)
                statement = store_statement(assigned, stored, node.stored_outputs.get(pin))
                if guard and guard != "TRUE" and pin != ENO_PIN:
                    statement = "IF %s THEN %s END_IF" % (guard, statement)
                statements.append(statement)
            # The bubble on whichever pin a reader takes is applied there, in
            # the OutputRef branch, so the shared expression stays un-negated.
            return remember(expression)

        name = node.instance_name
        statements.append("%s(%s);" % (name, ", ".join("%s := %s" % (pin, value) for pin, value in pairs)))
        for pin, assigned in node.outputs:
            if assigned:
                value = "%s.%s" % (name, pin)
                # A negated output pin stores its inverse.
                if pin in node.negated_outputs:
                    value = "NOT " + value
                statements.append(store_statement(assigned, value, node.stored_outputs.get(pin)))
        result = (name + "." + node.active_output) if node.active_output else name
        if node.active_output in node.negated_outputs:
            result = "NOT " + result
        return remember(result)

    return "?"


def _assign_guard(source, statements, emitted):
    """The EN a store inherits from the operator it reads, if any.

    Only for a store reading an operator's result directly. A function block
    states its own EN as a call argument, and an ENO reader is the enable
    rather than something the enable gates.
    """
    if not isinstance(source, OutputRef) or not source.call.is_operator:
        return None
    if source.pin == ENO_PIN:
        return None
    return _enable(source.call, statements, emitted)


def network_to_statements(network):
    """Statements for one network, which may drive several outputs.

    The shared logic is emitted once: a function block feeding two outputs is
    called once in the program, so calling it twice here would misrepresent
    it. Plain expressions still repeat, which is what ST would say anyway.
    """
    statements = []
    emitted = {}
    for tree in getattr(network, "outputs", [network]):
        before = len(statements)
        value = _fbd_value(tree, statements, emitted)
        if len(statements) == before and value:
            # A bare expression with nothing to assign it to - keep it visible
            # rather than dropping it entirely.
            statements.append("(* " + value + " *)")
    return statements


LD = "LD"


def render_pou(pou):
    """Render a POU as declaration plus ST statements, one block per network.

    A network holds rungs in LD and call trees in FBD; they walk differently,
    so the POU's language picks the walker.
    """
    lines = render_declaration(pou)
    lines.append("")

    for index, network in enumerate(pou.networks):
        lines.extend(network_headers(index + 1, network))
        if pou.language == LD:
            for rung in network.outputs:
                lines.extend(rung_to_statements(rung))
        else:
            lines.extend(network_to_statements(network))
        lines.append("")

    if not pou.networks:
        lines.append("(* no networks *)")

    while lines and lines[-1] == "":
        lines.pop()

    return [line.rstrip() for line in lines]
