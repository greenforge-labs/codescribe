# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Parse XML with whatever the host can do fastest.

CODESYS puts its own ScriptLib ahead of the standard library, and the
ElementTree it ships there is the xmllib-era one that parses in pure Python.
Measured on a real project: 25 POUs took 6.8s, of which 6.4s was parsing and
0.3s was drawing the diagrams. The layout code was never the problem.

IronPython runs on .NET, so System.Xml is right there and native. This picks
it when it is available and falls back to ElementTree otherwise, which is
what CPython uses when running the tests.

The two backends must agree exactly, because the golden files are generated
under CPython and consumed by CODESYS. test_xmlbackend.py compares them
element for element wherever both are available - which is the IronPython CI
job, the only place that can.

Only the small slice of the ElementTree API this project actually uses is
implemented: a tag, attributes, leading text, iteration over child elements,
and a recursive walk.
"""

import xml.etree.ElementTree as ET

ELEMENT_TREE = "ElementTree"
SYSTEM_XML = "System.Xml"

try:
    import clr

    clr.AddReference("System.Xml")
    from System import Array, Byte
    from System.IO import MemoryStream
    from System.Xml import XmlDocument, XmlNodeType

    _SYSTEM_XML_AVAILABLE = True
except Exception:  # pragma: no cover - only reachable off IronPython
    _SYSTEM_XML_AVAILABLE = False


class _DotNetElement(object):
    """The slice of the ElementTree element API this project uses."""

    __slots__ = ("_node", "_children")

    def __init__(self, node):
        self._node = node
        self._children = None

    @property
    def tag(self):
        # LocalName drops the namespace, which is what plcopen.tag() would
        # have stripped anyway.
        return self._node.LocalName

    def get(self, name, default=None):
        attributes = self._node.Attributes
        if attributes is None:
            return default
        found = attributes.GetNamedItem(name)
        # An absent attribute must be None rather than "": callers use
        # "is None" to tell "not written" from "written empty".
        return found.Value if found is not None else default

    @property
    def text(self):
        """Text before the first child element, as ElementTree defines it.

        Not InnerText, which would flatten descendants and make the two
        backends disagree on mixed content.
        """
        parts = []
        for child in self._node.ChildNodes:
            node_type = child.NodeType
            if node_type == XmlNodeType.Element:
                break
            if node_type in (
                XmlNodeType.Text,
                XmlNodeType.CDATA,
                XmlNodeType.Whitespace,
                XmlNodeType.SignificantWhitespace,
            ):
                parts.append(child.Value)
        if not parts:
            return None
        text = "".join(parts)
        # XML requires a parser to normalise line endings to \n, and
        # ElementTree does. XmlDocument does too - except for the whitespace
        # nodes PreserveWhitespace keeps, which come back with CR intact. Real
        # CODESYS exports are CRLF throughout, so this is not a corner case.
        if "\r" in text:
            text = text.replace("\r\n", "\n").replace("\r", "\n")
        return text

    def __iter__(self):
        # Wrapped once and kept. The parsers call find_child several times on
        # the same element - a block asks for inputVariables, inOutVariables
        # and outputVariables in turn - and re-wrapping every child on each
        # call was most of what this backend spent its time doing.
        if self._children is None:
            self._children = [
                _DotNetElement(child) for child in self._node.ChildNodes if child.NodeType == XmlNodeType.Element
            ]
        return iter(self._children)

    def iter(self):
        """Pre-order walk, as ElementTree does it.

        An explicit stack rather than recursive generators: delegating a yield
        up through every level of a deep document costs more than the walk.
        """
        stack = [self]
        while stack:
            node = stack.pop()
            yield node
            children = list(node)
            for index in range(len(children) - 1, -1, -1):
                stack.append(children[index])


def _parse_dotnet(data):
    document = XmlDocument()
    # XmlDocument drops insignificant whitespace by default, so an element
    # whose only content is a newline and some indentation would report no
    # text at all where ElementTree reports "\n    ". Harmless for every
    # current caller, since they all strip - but the backends have to agree
    # about what the document says, not merely about what today's callers
    # make of it.
    document.PreserveWhitespace = True
    # Never fetch an external DTD: a POU export should not be able to make
    # CODESYS reach out to the network while someone clicks Export.
    document.XmlResolver = None
    stream = MemoryStream(Array[Byte](bytearray(data)))
    try:
        document.Load(stream)
    finally:
        stream.Close()
    return _DotNetElement(document.DocumentElement)


def _parse_element_tree(data):
    return ET.fromstring(data)


def available():
    """Backend names this host can use, fastest first."""
    names = []
    if _SYSTEM_XML_AVAILABLE:
        names.append(SYSTEM_XML)
    names.append(ELEMENT_TREE)
    return names


_PARSERS = {SYSTEM_XML: _parse_dotnet, ELEMENT_TREE: _parse_element_tree}

_active = available()[0]


def use(name):
    """Force a backend. Returns the previous one, so tests can restore it."""
    global _active
    if name not in _PARSERS:
        raise ValueError("unknown xml backend %r" % (name,))
    if name == SYSTEM_XML and not _SYSTEM_XML_AVAILABLE:
        raise ValueError("System.Xml is not available on this host")
    previous, _active = _active, name
    return previous


def active():
    return _active


def parse(data, backend=None):
    """Parse document bytes and return the root element."""
    return _PARSERS[backend or _active](data)
