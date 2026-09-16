# REMEMBER: this must stay valid under IronPython 2.7 as well as Python 3.
"""Render the graphical POUs in a PLCopen XML file.

    python tools/ladder/render.py [options] <file.xml> [...]

    --format art|st|both    art  diagrams, as the export writes them (default)
                            st   equivalent Structured Text
                            both the ST followed by the diagram

    --charset unicode|ascii box-drawing characters (the default), or plain
                            ASCII for terminals and diff viewers that mangle
                            them

Output is written as UTF-8 regardless of the console encoding.

Ladder and Function Block Diagram are supported; SFC bodies are skipped.
"""

from __future__ import print_function, unicode_literals

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# The renderers live in src/, alongside the CODESYS export scripts.
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))

import charset  # noqa: E402
import fbd_render  # noqa: E402
import ld_render  # noqa: E402
import parse_fbd  # noqa: E402
import parse_ld  # noqa: E402
import st_render  # noqa: E402

FORMATS = ("art", "st", "both")


def _pous(path):
    """Every graphical POU in the file, paired with its art renderer."""
    found = []
    for pou in parse_ld.parse_pous(path):
        found.append((pou, ld_render))
    for pou in parse_fbd.parse_pous(path):
        found.append((pou, fbd_render))
    return found


def render_file(path, output_format="art"):
    lines = []
    for pou, art_renderer in _pous(path):
        if output_format in ("st", "both"):
            lines.extend(st_render.render_pou(pou))
            lines.append("")
        if output_format in ("art", "both"):
            rendered = art_renderer.render_pou(pou)
            if output_format == "both":
                # The diagram repeats the declaration, which is noise the
                # second time around.
                rendered = rendered[len(ld_render.render_declaration(pou)) :]
            lines.extend(rendered)
            lines.append("")
    return [line.rstrip() for line in lines]


def write(lines, stream=None):
    """Write as UTF-8 bytes.

    A Windows console defaults to a codepage that cannot encode box drawing,
    so going through print() would raise UnicodeEncodeError on exactly the
    output this tool exists to produce.
    """
    if stream is None:
        stream = sys.stdout
    buffer = getattr(stream, "buffer", stream)
    for line in lines:
        buffer.write((line + "\n").encode("utf-8"))
    buffer.flush()


def main(argv):
    output_format = "art"
    paths = []
    index = 0
    while index < len(argv):
        argument = argv[index]
        if argument == "--format":
            index += 1
            if index >= len(argv) or argv[index] not in FORMATS:
                print("--format must be one of: " + ", ".join(FORMATS))
                return 2
            output_format = argv[index]
        elif argument == "--charset":
            index += 1
            if index >= len(argv) or argv[index] not in charset.SETS:
                print("--charset must be one of: " + ", ".join(sorted(charset.SETS)))
                return 2
            charset.use(argv[index])
        else:
            paths.append(argument)
        index += 1

    if not paths:
        print(__doc__)
        return 2

    for path in paths:
        write(render_file(path, output_format))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
