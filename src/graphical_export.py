# REMEMBER: this is python 2.7
"""Write a human-readable rendering of a graphical POU alongside its native xml.

Graphical POUs (LD, FBD, SFC, CFC) have no textual implementation, so they
export as CODESYS native xml, which git can store but nobody can review. This
adds a derived ".txt" next to it: the declaration, and a diagram per network.

An equivalent-ST rendering of the same networks exists in st_render, and it
says things a single-wire diagram cannot - a block read through two of its
output pins is one call. The export does not write one; tools/ladder/write_st.py
does, on demand, and its docstring says how to put it back on this path.

The ".txt" is READ-ONLY as far as CODESCRIBE is concerned. The native xml
stays the only thing Import From Files reads, so the round trip is unaffected
and editing the ".txt" achieves nothing. import_from_files dispatches on
".xml" and ".st", so a ".txt" is ignored by construction.

The rendering goes through PLCopen xml rather than the native format, because
PLCopen has a published schema for graphical bodies while the native format
does not.
"""

import os
import tempfile
import time

import fbd_render
import ld_render
import native_networks
import parse_fbd
import parse_ld
import plcopen
from util import open_utf8

# Suffixes for the derived files. Deliberately not .st: these are not
# importable and must never be mistaken for source. import_from_files
# dispatches on ".xml" and ".st", and os.path.splitext sees ".txt" for both of
# these, so both are ignored by construction.
RENDERED_SUFFIX = ".txt"

# Said in the file itself when the editor's numbering could not be recovered.
# Numbering silently adrift from the editor is how an off-by-one review
# happens; a reviewer has to be able to see the doubt in the file they read.
ALIGNMENT_WARNING = (
    "(* WARNING: could not line these networks up with the native export;"
    " the numbering may not match the CODESYS editor *)"
)

# Rendering adds a second CODESYS-side export per graphical POU, so the cost
# is worth reporting rather than leaving people to wonder why the export got
# slower. Split so it is obvious whether CODESYS or this code is the cost.
EMPTY_STATS = {
    "rendered": 0,
    "skipped": 0,
    "export_xml_seconds": 0.0,
    "parse_seconds": 0.0,
    "draw_seconds": 0.0,
    "verbatim_declarations": 0,
    "fallback_declarations": 0,
    "members_missing": 0,
    "alignment_failures": 0,
}

STATS = dict(EMPTY_STATS)

# Names behind STATS["skipped"], so the summary can say *what* was skipped.
# A bare count reads like something went missing; a name plus the reason
# (SFC/CFC have no renderer) answers the question before it is asked.
SKIPPED_POUS = []


def reset_stats():
    STATS.update(EMPTY_STATS)
    del SKIPPED_POUS[:]


def summary():
    """One line describing what rendering cost, or None if it did nothing.

    Split three ways because the first measurement overturned the guess: the
    CODESYS-side export turned out to be a rounding error next to this code,
    and "rendering" as a single figure does not say whether that is the XML
    parser or the layout.
    """
    if not STATS["rendered"] and not STATS["skipped"]:
        return None
    total = STATS["export_xml_seconds"] + STATS["parse_seconds"] + STATS["draw_seconds"]
    line = (
        "Rendered %d graphical POUs in %.1fs"
        " (%.1fs CODESYS export_xml, %.1fs parsing, %.1fs drawing); skipped %d"
        % (
            STATS["rendered"],
            total,
            STATS["export_xml_seconds"],
            STATS["parse_seconds"],
            STATS["draw_seconds"],
            STATS["skipped"],
        )
    )
    if SKIPPED_POUS:
        shown = SKIPPED_POUS[:6]
        names = ", ".join(shown)
        if len(SKIPPED_POUS) > len(shown):
            names += ", +%d more" % (len(SKIPPED_POUS) - len(shown))
        line += " (no renderable body - SFC/CFC: %s)" % names
    # Falling back to the rebuilt declaration is silent otherwise, and it
    # costs every comment, pragma and attribute in the file. Say so.
    if STATS["fallback_declarations"]:
        line += "\n         NOTE: %d POU declaration(s) were rebuilt from structured XML; comments," % STATS[
            "fallback_declarations"
        ]
        line += " pragmas and attributes may be missing from those declarations."
    # No file at all for a member is deliberate, but it is still a POU with no
    # rendering beside its xml, so it has to be said rather than inferred.
    if STATS["members_missing"]:
        line += "\n         NOTE: %d action/transition/method export(s) did not carry the" % STATS[
            "members_missing"
        ]
        line += " member's own body; nothing was written for those - review their native xml."
    if STATS["alignment_failures"]:
        line += "\n         NOTE: %d POU(s) could not be lined up with their native export;" % STATS[
            "alignment_failures"
        ]
        line += " those are numbered in export order and say so at the top."
    return line


# Body language -> (parser, diagram renderer). SFC and CFC are absent, so they
# fall through and no file is written for them.
RENDERERS = {
    parse_ld.LANGUAGE: (parse_ld, ld_render),
    parse_fbd.LANGUAGE: (parse_fbd, fbd_render),
}


def _write_lines(path, lines):
    """Write one rendering, newline-terminated, as UTF-8."""
    with open_utf8(path, "w") as f:
        f.write(u"\n".join(lines))
        f.write(u"\n")


def _render_pous(plcopen_path, member_name=None):
    """(pou, art_renderer) for every POU in the file we know how to draw.

    One pass over the document. Asking each language parser in turn would
    re-read and re-parse the whole file once per language, which is pure waste
    on a project with hundreds of POUs.

    With a member_name, only that member's own body qualifies. The exported
    file also carries the parent POU's body, and rendering that instead is
    exactly the foreign-dump defect this parameter exists to prevent.
    """
    found = []
    if member_name is None:
        bodies = plcopen.iter_bodies(plcopen_path)
    else:
        bodies = plcopen.iter_member_bodies(plcopen_path, member_name)
    for pou_elem, language, body in bodies:
        entry = RENDERERS.get(language)
        if entry is None:
            continue
        parser, art_renderer = entry
        pou = parser.pou_from_body(pou_elem, body)
        if member_name is not None:
            lowered = pou.name.lower()
            if lowered != member_name.lower() and not lowered.endswith("." + member_name.lower()):
                # The body came from a member nested in the parent pou, whose
                # name the parser picked up. Title the rendering for what it
                # actually shows - and flag it, because the declaration in
                # the export is the parent's and the rendering should say so.
                pou.name = pou.name + "." + member_name
                pou.member_of_parent = True
        found.append((pou, art_renderer))
    return found


def _joined(blocks):
    """One POU rendering after another, with the blank lines tidied up."""
    lines = []
    for block in blocks:
        lines.extend(block)
        lines.append(u"")
    while lines and lines[-1] == u"":
        lines.pop()
    return lines


def render_plcopen(plcopen_path, declaration_text=None, member_name=None, native_path=None):
    """The diagram lines for a PLCopen file, or [] if none apply.

    The declaration and a diagram per network. An equivalent-ST rendering is
    written by st_render and reachable from tools/ladder/render.py, but the
    export does not write one: it was tried in the same file, which was worse
    than either notation alone, and then in a file of its own, which is not
    what is wanted for now.

    ``member_name`` restricts the rendering to that sub-POU member's own
    body; see _render_pous. ``native_path`` is the native export written
    beside the rendering, read back for the editor's own network list; see
    native_networks.
    """
    started = time.time()
    pous = _render_pous(plcopen_path, member_name)
    if declaration_text is not None and pous:
        pous[0][0].declaration_text = declaration_text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
    STATS["parse_seconds"] += time.time() - started

    # The editor's own network list, where one is available. It belongs to one
    # POU and carries nothing to say which, so a file holding more than one
    # renderable POU cannot use it - and that counts as a failure to line them
    # up rather than as a reason to say nothing.
    warnings = []
    native = native_networks.read_networks(native_path) if native_path is not None else None
    if native and pous:
        # No POU means nothing to number - a member export that carried no
        # renderable body of its own, say. Running the alignment on it counted
        # a spurious failure and printed a "could not line up" note for a POU
        # that was never drawn.
        aligned = native_networks.align(native, pous[0][0].networks) if len(pous) == 1 else None
        if aligned is None:
            STATS["alignment_failures"] += 1
            warnings.append(ALIGNMENT_WARNING)
        else:
            pous[0][0].networks = aligned

    # A member's export carries the parent's declaration, not its own, so
    # both renderings have to open by saying whose declaration they show.
    notes = []
    for pou, _art_renderer in pous:
        head = list(warnings)
        # The note is true only when the rendering opens with the parent's
        # declaration. A graphical method carries its own, passed in as
        # declaration_text, so there the note would misdescribe what follows.
        if getattr(pou, "member_of_parent", False) and declaration_text is None:
            head.append(u"(* " + pou.name + u" - the declaration below is the parent POU's *)")
        notes.append(head + [u""] if head else [])

    started = time.time()
    drawn = []
    for index, entry in enumerate(pous):
        pou, art_renderer = entry
        if pou.declaration_text:
            STATS["verbatim_declarations"] += 1
        else:
            STATS["fallback_declarations"] += 1
        drawn.append(notes[index] + art_renderer.render_pou(pou))
    STATS["draw_seconds"] += time.time() - started

    return _joined(drawn)


# Ways of asking for plaintext declarations, most likely to bind first.
# ScriptEngine methods are .NET overloads, and IronPython resolves them by
# signature: keyword arguments frequently fail to bind where the same call
# positionally succeeds. The documented overload is
# export_xml(path, recursive, export_folder_structure, declarations_as_plaintext).
_EXPORT_ATTEMPTS = (
    lambda obj, path: obj.export_xml(path, False, False, True),
    lambda obj, path: obj.export_xml(path=path, recursive=False, declarations_as_plaintext=True),
    lambda obj, path: obj.export_xml(None, path, False, False, True),
)


def _export_plcopen(obj, path):
    """Export one object as PLCopen xml, asking for plaintext declarations.

    The structured <interface> has nowhere to put a comment, a pragma or an
    attribute, so without this the declaration in the rendering silently drops
    all three. CODESYS documents the flag as lossless.

    It is a proprietary extension and an overload this ScriptEngine build may
    not have, so a TypeError - which is what IronPython raises when no
    overload matches - falls back to the plain call rather than losing the
    rendering altogether.
    """
    for attempt in _EXPORT_ATTEMPTS:
        try:
            attempt(obj, path)
            return
        except TypeError:
            # No matching overload on this build. Try the next shape.
            continue
    # Nothing with plaintext bound, so fall back to the lossy declaration
    # rather than losing the rendering.
    obj.export_xml(path=path, recursive=False)


def _remove_quietly(path):
    """Best-effort delete. Cleanup trouble is never worth failing an export."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def write_rendered_text(obj, base_path, member_name=None):
    """Export obj as PLCopen xml, render it, and write the derived files.

    Returns True if files were written. SFC and CFC bodies parse to nothing
    renderable, so they are skipped rather than producing empty files.

    ``member_name`` marks obj as a sub-POU member (action, transition,
    graphical method) whose PLCopen export wraps it in its *parent* POU.
    Only the member's own body is rendered then - never the parent's, whose
    networks under the member's filename would have a reviewer reading a
    different POU. If the export carries no such body, nothing is written at
    all: an absent rendering sends the reviewer to the native xml, a foreign
    one does not.

    A rendering failure must not fail the export: the native xml has already
    been written and is complete and correct on its own. The problem is
    reported and the export carries on. That barrier has to hold around the
    temp-file scaffolding too, not just the rendering itself - a full %TEMP%
    or an antivirus scan holding the temp file open must degrade to a warning
    exactly like a parse failure does.
    """
    # Staged outside the export folder: exports are written to a staging
    # directory that gets swapped into place wholesale, and a temp file left
    # behind by a failed cleanup would be swapped in along with it.
    try:
        handle, temp_path = tempfile.mkstemp(suffix=".plcopen.xml")
        os.close(handle)
    except Exception as error:
        print("WARNING: could not render " + obj.get_name() + ": " + repr(error))
        return False
    try:
        started = time.time()
        _export_plcopen(obj, temp_path)
        STATS["export_xml_seconds"] += time.time() - started

        # render_plcopen accounts for its own parse, draw and ST time.
        textual_declaration = getattr(getattr(obj, "textual_declaration", None), "text", None)
        lines = render_plcopen(temp_path, textual_declaration, member_name, base_path + ".xml")
        if not lines:
            if member_name is not None:
                # No file at all is the honest outcome: an absent rendering
                # sends the reviewer to the native xml, a foreign one does not.
                STATS["members_missing"] += 1
                print(
                    "WARNING: the PLCopen export of "
                    + obj.get_name()
                    + " carries no renderable body for the member itself;"
                    + " nothing written - review the native xml"
                )
            else:
                # Members announce themselves above; these are the SFC/CFC
                # bodies no renderer exists for.
                SKIPPED_POUS.append(obj.get_name())
            STATS["skipped"] += 1
            return False

        _write_lines(base_path + RENDERED_SUFFIX, lines)
        STATS["rendered"] += 1
        return True
    except Exception as error:
        print("WARNING: could not render " + obj.get_name() + ": " + repr(error))
        # Say what is actually in the file, so a failure explains itself
        # instead of needing a separate diagnostic run. The diagnostic is
        # best-effort: it must not turn a reported failure into a raised one.
        try:
            if os.path.exists(temp_path):
                for note in plcopen.describe_suspect_characters(temp_path):
                    print("         " + note)
        except Exception:
            pass
        # A write that died halfway leaves a truncated rendering that looks
        # exactly like a valid one. No file at all is the honest outcome.
        _remove_quietly(base_path + RENDERED_SUFFIX)
        return False
    finally:
        _remove_quietly(temp_path)
