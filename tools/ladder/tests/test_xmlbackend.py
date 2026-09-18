# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Tests for the XML backend, and for the two backends agreeing.

The golden files are generated under CPython with ElementTree and consumed by
CODESYS with System.Xml. If the backends disagree anywhere, CODESYS silently
renders something the goldens never saw. So the important test here can only
run where both backends exist - the IronPython CI job - and it is written to
report loudly when it is skipped rather than passing quietly.

    python tools/ladder/tests/test_xmlbackend.py
"""

from __future__ import print_function, unicode_literals

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "src"))
sys.path.insert(0, os.path.join(HERE, ".."))

from render import write  # noqa: E402

import plcopen  # noqa: E402
import xmlbackend  # noqa: E402

FIXTURES = os.path.join(HERE, "fixtures")
CODESYS = os.path.join(FIXTURES, "codesys")

failures = []


def astral_reference():
    """A character outside the Basic Multilingual Plane, as one reference.

    IronPython holds strings as UTF-16, so such a character is a surrogate
    pair, and encoding it a unit at a time writes two numeric references for
    one character. A lone surrogate is not a legal XML character: System.Xml
    accepts it, expat rejects the whole document - an export that parses
    inside CODESYS and nowhere else.

    Written as the UTF-8 bytes a real file holds, so this source stays ASCII
    and loads under both interpreters.
    """
    data = b"<x>hi \xf0\x9f\x98\x80 there</x>"
    return plcopen._to_ascii(data)


def check(name, condition, detail=""):
    if condition:
        print("OK      " + name)
        return
    failures.append(name)
    # See test_fbd: a detail quoting rendered lines cannot go through print()
    # on a Windows console without aborting the run.
    sys.stdout.flush()
    write(["FAIL    " + name + ((": " + detail) if detail else "")])


def check_equal(name, actual, expected):
    check(name, actual == expected, "expected %r, got %r" % (expected, actual))


def every_fixture():
    paths = []
    for folder in (FIXTURES, CODESYS):
        for name in sorted(os.listdir(folder)):
            if name.endswith(".xml"):
                paths.append(os.path.join(folder, name))
    return paths


SAMPLE = (
    b'<?xml version="1.0" encoding="utf-8"?>'
    b'<root xmlns="http://example/ns">'
    b'<a name="one" empty="">text<b/>tail</a>'
    b"<a/>"
    b"</root>"
)


# --- the active backend behaves like ElementTree ---------------------------

print("available backends: " + ", ".join(xmlbackend.available()))
print("active backend:     " + xmlbackend.active())

root = xmlbackend.parse(SAMPLE)

# U+1F600 is one character; it must come back as one reference, not as the
# two surrogates it is stored as.
check_equal("an astral character is one reference", astral_reference(), b"<x>hi &#128512; there</x>")
check("no lone surrogate reaches the parser", b"&#55357;" not in astral_reference())

check_equal("namespace is stripped from the tag", plcopen.tag(root), "root")
first = list(root)[0]
check_equal("attributes read back", first.get("name"), "one")
# "not written" and "written empty" are different, and callers rely on it.
check_equal("an absent attribute is None", first.get("missing"), None)
check_equal("an empty attribute is not None", first.get("empty"), "")
check_equal("a default is honoured", first.get("missing", "fallback"), "fallback")
# Leading text only, as ElementTree defines it - not a flattened InnerText,
# which would fold "tail" in and make the backends disagree.
check_equal("text stops at the first child element", first.text, "text")
check_equal("an element with no text is None", list(root)[1].text, None)
check_equal("iteration yields child elements", len(list(root)), 2)
check_equal("iter walks the whole tree", len(list(root.iter())), 4)
# Pre-order, like ElementTree - a stack walk is easy to get backwards.
check_equal("iter is in document order", [plcopen.tag(e) for e in root.iter()], ["root", "a", "b", "a"])
# Children are cached per element, so repeated find_child calls stay cheap.
check("repeated iteration is stable", list(root)[0] is list(root)[0])

# POUs are found without walking the document, but an unusual layout must
# still work rather than silently rendering nothing.
NESTED = b'<project><wrapper><pou name="X" pouType="program"><body><LD/></body></pou></wrapper></project>'
check_equal(
    "a pou outside types/pous is still found",
    [p.get("name") for p in plcopen.find_pous(xmlbackend.parse(NESTED))],
    ["X"],
)


# --- the two backends must agree -------------------------------------------


def first_difference(left, right, path="/"):
    """Where two trees first disagree, or None. Reported, not just counted.

    A bare "the trees differ" sends whoever sees it back to CI to guess again;
    the whole value of this test is that it can say which element and which
    field, in a place no debugger reaches.
    """
    left_tag, right_tag = plcopen.tag(left), plcopen.tag(right)
    if left_tag != right_tag:
        return "%s tag %r vs %r" % (path, left_tag, right_tag)
    if left.text != right.text:
        return "%s<%s> text %r vs %r" % (path, left_tag, left.text, right.text)
    left_children, right_children = list(left), list(right)
    if len(left_children) != len(right_children):
        return "%s<%s> child count %d vs %d (%r vs %r)" % (
            path,
            left_tag,
            len(left_children),
            len(right_children),
            [plcopen.tag(c) for c in left_children][:6],
            [plcopen.tag(c) for c in right_children][:6],
        )
    for index in range(len(left_children)):
        child_path = "%s%s[%d]/" % (path, plcopen.tag(left_children[index]), index)
        found = first_difference(left_children[index], right_children[index], child_path)
        if found:
            return found
    return None


def attribute_values(elem, names):
    return [elem.get(name) for name in names]


if len(xmlbackend.available()) < 2:
    # Not a pass. The comparison below is the whole point of this file, and it
    # cannot run here.
    print("")
    print("SKIPPED the backend comparison: only %s is available on this host." % xmlbackend.active())
    print("        It runs in the IronPython CI job, where System.Xml exists.")
    print("")
else:
    for path in every_fixture():
        name = os.path.basename(path)
        data = plcopen.read_document(path)

        one = xmlbackend.parse(data, xmlbackend.ELEMENT_TREE)
        two = xmlbackend.parse(data, xmlbackend.SYSTEM_XML)
        difference = first_difference(one, two)
        check(name + ": both backends build the same tree", difference is None, difference or "")

        # Shape equality would not catch attributes, which is where most of
        # the parsing decisions actually live.
        interesting = ("localId", "refLocalId", "formalParameter", "negated", "typeName", "name", "edge", "storage")
        left = [attribute_values(e, interesting) for e in one.iter()]
        right = [attribute_values(e, interesting) for e in two.iter()]
        check(name + ": both backends read the same attributes", left == right)

    # The contract that actually matters: identical rendered output.
    import fbd_render  # noqa: E402
    import ld_render  # noqa: E402
    import parse_fbd  # noqa: E402
    import parse_ld  # noqa: E402

    for path in every_fixture():
        name = os.path.basename(path)
        rendered = {}
        for backend in (xmlbackend.ELEMENT_TREE, xmlbackend.SYSTEM_XML):
            previous = xmlbackend.use(backend)
            try:
                lines = []
                for pou in parse_ld.parse_pous(path):
                    lines.extend(ld_render.render_pou(pou))
                for pou in parse_fbd.parse_pous(path):
                    lines.extend(fbd_render.render_pou(pou))
                rendered[backend] = lines
            finally:
                xmlbackend.use(previous)
        check(
            name + ": both backends render identically",
            rendered[xmlbackend.ELEMENT_TREE] == rendered[xmlbackend.SYSTEM_XML],
        )

print("")
if failures:
    print("%d check(s) failed" % len(failures))
else:
    print("all checks passed")
sys.exit(1 if failures else 0)
