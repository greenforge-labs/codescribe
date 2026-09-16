# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Write the equivalent-ST rendering of a graphical POU beside its diagram.

    python tools/ladder/write_st.py <file.plcopen.xml> [...]

The export does not write these. It did for a while, as "<name>.st.txt" next
to "<name>.txt", and that is easy to turn back on - see below - but for now
the diagram is the only rendering the export produces, and this script is how
to get the ST when it is wanted.

The ST states the logic exactly where the diagram can only approximate it: a
block read through two of its output pins is one call, and no single-wire
diagram can say so. It is a rendering, not a translation - not guaranteed to
compile, and never to be fed back into CODESYS - so every file it writes
opens by saying that.

Input is PLCopen xml, which is what the renderer reads. To get some from a
project, call graphical_export._export_plcopen(obj, path) from a CODESYS
script; codesys-headless-test.md shows how to run one.

To put this back on the export path, in graphical_export.py:

  * import st_render
  * have render_plcopen return the ST lines alongside the diagram lines,
    built the same way as the diagram - notes first, then one
    st_render.render_pou(pou) per POU, joined by _joined
  * in write_rendered_text, write them to base_path + ".st.txt" with
    ST_HEADER at the top, and remove that file alongside the diagram when a
    write fails

The suffix has to stay ".st.txt" rather than ".st": import_from_files
dispatches on ".xml" and ".st", and os.path.splitext sees ".txt" for this
one, so it is ignored by construction the way the diagram is.
"""

from __future__ import print_function, unicode_literals

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))

from render import write  # noqa: E402

import parse_fbd  # noqa: E402
import parse_ld  # noqa: E402
import plcopen  # noqa: E402
import st_render  # noqa: E402

# Language -> parser. Kept here rather than imported from graphical_export,
# which needs the CODESYS scriptengine module to load at all.
PARSERS = {parse_ld.LANGUAGE: parse_ld, parse_fbd.LANGUAGE: parse_fbd}

# Stated in the file itself, not just in the docs. The ST reads like source
# and sits next to real .st exports, so the one thing a reader must not
# assume is that it can go back into CODESYS.
ST_HEADER = [
    "(* Equivalent Structured Text for a graphical POU, written by codescribe.",
    "   READ ONLY. This is a rendering of the native xml beside it, not a",
    "   translation: it is not guaranteed to compile and must never be imported",
    "   or pasted back into CODESYS. The native xml is the source. *)",
    "",
]

SUFFIX = ".st.txt"


def render(path):
    """The ST lines for every renderable POU in a PLCopen file."""
    lines = []
    for pou_elem, language, body in plcopen.iter_bodies(path):
        parser = PARSERS.get(language)
        if parser is None:
            continue
        lines.extend(st_render.render_pou(parser.pou_from_body(pou_elem, body)))
        lines.append("")
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def main(argv):
    if not argv:
        write(__doc__.strip().split("\n")[:3])
        return 2
    for path in argv:
        lines = render(path)
        if not lines:
            print("nothing renderable in " + path)
            continue
        base = path
        for ending in (".plcopen.xml", ".xml"):
            if base.endswith(ending):
                base = base[: -len(ending)]
                break
        target = base + SUFFIX
        handle = open(target, "wb")
        try:
            handle.write(("\n".join(ST_HEADER + lines) + "\n").encode("utf-8"))
        finally:
            handle.close()
        print("wrote " + target)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
