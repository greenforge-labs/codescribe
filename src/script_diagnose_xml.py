# REMEMBER: this is python 2.7
"""Diagnose why PLCopen rendering fails inside CODESYS.

Run this the same way as the other scripts (Tools > Scripting > Execute Script
File, or add it as a toolbar command) with the affected project open. It writes
everything to the message view and changes nothing.

It answers three questions:

  1. Which xml module is actually being imported? CODESYS ships its own XML
     modules in ScriptLib, which is on sys.path and can shadow the standard
     library.
  2. Can that module parse a trivial document, with and without a UTF-8 BOM?
     CODESYS writes a BOM, and older parsers reject it as "illegal data at
     start of file".
  3. What do the first bytes of a real export_xml file actually look like?
"""

from __future__ import print_function

import os
import sys
import tempfile

import scriptengine  # type: ignore

from object_type import ObjectType, get_object_type
from util import print_python_version

PLAIN = b'<?xml version="1.0" encoding="utf-8"?><a><b x="1">hi</b></a>'
WITH_BOM = b"\xef\xbb\xbf" + PLAIN


def report(label, value):
    print("  " + label.ljust(28) + str(value))


def probe_parser():
    print("--- xml module ---")
    try:
        import xml

        report("xml.__file__", getattr(xml, "__file__", "<none>"))
        report("xml.__path__", getattr(xml, "__path__", "<none>"))
    except Exception as error:
        report("import xml FAILED", repr(error))

    try:
        import xml.etree.ElementTree as ET

        report("ElementTree.__file__", getattr(ET, "__file__", "<none>"))
        report("ElementTree.VERSION", getattr(ET, "VERSION", "<none>"))
    except Exception as error:
        report("import ElementTree FAILED", repr(error))
        return None

    for label, data in (("without BOM", PLAIN), ("with BOM", WITH_BOM)):
        try:
            root = ET.fromstring(data)
            report("fromstring " + label, "OK, root tag " + repr(root.tag))
        except Exception as error:
            report("fromstring " + label, "FAILED " + repr(error))

    # parse() takes a different path to fromstring() in some implementations,
    # and parse() is what the renderer actually uses.
    for label, data in (("without BOM", PLAIN), ("with BOM", WITH_BOM)):
        handle, path = tempfile.mkstemp(suffix=".xml")
        try:
            os.write(handle, data)
            os.close(handle)
            tree = ET.parse(path)
            report("parse " + label, "OK, root tag " + repr(tree.getroot().tag))
        except Exception as error:
            report("parse " + label, "FAILED " + repr(error))
        finally:
            if os.path.exists(path):
                os.remove(path)

    return ET


def find_graphical_object(obj, depth=0):
    """First graphical POU in the project.

    has_textual_implementation is False on plenty of objects that are not
    POUs, and the first one found is usually Project Information - whose
    export has no <interface> at all, so probing it says nothing about
    declarations while looking like it did.
    """
    if depth > 12:
        return None
    try:
        children = obj.get_children()
    except Exception:
        return None
    for child in children:
        try:
            if get_object_type(child) == ObjectType.POU and child.has_textual_implementation is False:
                return child
        except Exception:
            pass
        found = find_graphical_object(child, depth + 1)
        if found is not None:
            return found
    return None


def probe_export(ET):
    print("--- a real export_xml file ---")
    project = scriptengine.projects.primary
    if project is None:
        report("project", "none open - open the affected project and re-run")
        return

    target = find_graphical_object(project)
    if target is None:
        report("graphical object", "none found")
        return

    report("object", target.get_name())

    handle, path = tempfile.mkstemp(suffix=".plcopen.xml")
    os.close(handle)
    try:
        target.export_xml(path=path, recursive=False)
        size = os.path.getsize(path)
        report("bytes written", size)
        if size == 0:
            report("verdict", "export_xml wrote an EMPTY file")
            return

        f = open(path, "rb")
        try:
            head = f.read(160)
        finally:
            f.close()
        report("first bytes", repr(head))
        report("starts with BOM", head[:3] == b"\xef\xbb\xbf")

        if ET is not None:
            try:
                ET.parse(path)
                report("parse of real file", "OK")
            except Exception as error:
                report("parse of real file", "FAILED " + repr(error))
    except Exception as error:
        report("export_xml FAILED", repr(error))
    finally:
        if os.path.exists(path):
            os.remove(path)


def probe_declarations():
    """Which export_xml call binds, and where the declaration text lands.

    export_xml is a .NET overload set. IronPython resolves it by signature, so
    a keyword call can fail to bind where the same call positionally succeeds
    - and the failure is a TypeError that looks exactly like "this build has
    no such overload". Only trying each shape distinguishes them.
    """
    print("--- plaintext declarations ---")
    project = scriptengine.projects.primary
    if project is None:
        report("project", "none open")
        return

    target = find_graphical_object(project)
    if target is None:
        report("graphical POU", "none found - open a project with an LD or FBD POU")
        return
    report("graphical POU", target.get_name())

    shapes = (
        ("positional (path, rec, folders, plaintext)", lambda o, p: o.export_xml(p, False, False, True)),
        ("keyword", lambda o, p: o.export_xml(path=p, recursive=False, declarations_as_plaintext=True)),
        ("reporter-first", lambda o, p: o.export_xml(None, p, False, False, True)),
        ("plain (no plaintext)", lambda o, p: o.export_xml(p, False)),
    )

    exports = {}
    for label, call in shapes:
        handle, path = tempfile.mkstemp(suffix=".plcopen.xml")
        os.close(handle)
        try:
            call(target, path)
            f = open(path, "rb")
            try:
                exports[label] = f.read()
            finally:
                f.close()
            report(label, "OK, %d bytes" % len(exports[label]))
        except TypeError as error:
            report(label, "no such overload (%s)" % error)
        except Exception as error:
            report(label, "FAILED " + repr(error))
        finally:
            if os.path.exists(path):
                os.remove(path)

    # The flag grows the export, so the text is being written somewhere. Name
    # every addData in each version and report what the flag adds - guessing
    # at where it lands has already cost two round trips.
    plain = exports.get("plain (no plaintext)")
    with_text = exports.get("positional (path, rec, folders, plaintext)") or exports.get("keyword")
    if plain is None or with_text is None:
        return

    report("size difference", "%d bytes added by the flag" % (len(with_text) - len(plain)))

    def data_names(content):
        names = []
        index = content.find(b'<data name="')
        while index >= 0:
            start = index + len(b'<data name="')
            end = content.find(b'"', start)
            names.append(content[start:end])
            index = content.find(b'<data name="', end)
        return names

    before, after = data_names(plain), data_names(with_text)
    added = [name for name in after if name not in before]
    report("addData names, plain", "%d: %s" % (len(before), sorted(set(before))))
    report("addData names, plaintext", "%d: %s" % (len(after), sorted(set(after))))
    report("names only with the flag", added or "(none - the text is not in an addData)")

    for name in added[:2]:
        marker = with_text.find(b'<data name="' + name)
        report("  " + str(name), repr(with_text[marker : marker + 600]))

    if not added:
        # Same data names in both, so the extra bytes are inside one of them.
        for index in range(min(len(plain), len(with_text))):
            if plain[index : index + 1] != with_text[index : index + 1]:
                report("first difference at byte", index)
                report("  plain", repr(plain[max(0, index - 100) : index + 300]))
                report("  plaintext", repr(with_text[max(0, index - 100) : index + 300]))
                break


print("=== codescribe xml diagnosis ===")
print_python_version()
element_tree = probe_parser()
probe_export(element_tree)
probe_declarations()
print("--- sys.path ---")
for entry in sys.path:
    print("  " + str(entry))
print("=== end ===")
