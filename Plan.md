CODESCRIBE – implementation brief for Codex
Goals

UTF-8 safe exports/imports under Python 2.7 (CODESYS ScriptEngine) — no more 'ascii' codec errors on smart punctuation.

Stable filenames derived from object names (no illegal chars, no Unicode surprises).

Configurable export target (CLI arg + safe default) to avoid file locks when the project is open.

Actionable errors & logs for typical failures (locked files, path issues).

Zero regressions on existing behavior for users who don’t pass args.

Constraints

Runtime is Python 2.7.7 (CODESYS ScriptEngine 3.5.10.30).

Do not require external packages.

Maintain compatibility with existing project structure and scripts.

Acceptance criteria

A project containing Unicode (en/em dashes, smart quotes, NBSP) exports without error.

Resulting files are UTF-8 encoded.

Object names with odd chars produce safe filenames (ASCII-only, filesystem-safe).

Export To Files works while the .project is open by exporting to a separate path (when provided).

Import path can be overridden similarly.

Clear console messages when:

destination exists and can’t be removed,

path isn’t writable,

a file is locked,

config/args are invalid.

File-by-file work
1) src/util.py (ADD Unicode + file helpers)

Replace with / extend to include:

# -*- coding: utf-8 -*-
# Python 2.7 compatible

import os, io, re, sys
try:
    import unicodedata
except Exception:
    unicodedata = None

import scriptengine  # type: ignore
from object_type import get_object_type

# ---- existing helpers kept (print_python_version, assert_*, first_* ) ----
# keep your current functions here; append the following:

SMART_MAP = {
    u'\u2013': u'-',  # en dash
    u'\u2014': u'-',  # em dash
    u'\u2018': u"'",  # left single quote
    u'\u2019': u"'",  # right single quote
    u'\u201c': u'"',  # left double quote
    u'\u201d': u'"',  # right double quote
    u'\xa0' : u' ',   # non-breaking space
}

def _to_u(s):
    try:
        return s if isinstance(s, unicode) else unicode(s, 'utf-8', 'ignore')
    except NameError:
        return s

def sanitize_text(s):
    u = _to_u(s)
    for k, v in SMART_MAP.items():
        u = u.replace(k, v)
    return u

def safe_filename(name):
    u = sanitize_text(name)
    if unicodedata:
        u = unicodedata.normalize('NFKD', u)
    try:
        u = u.encode('ascii', 'ignore').decode('ascii')
    except Exception:
        pass
    u = re.sub(r'[^\w\-. ]+', '_', u)
    u = u.strip().rstrip('.')
    return u or 'unnamed'

def ensure_dir(d):
    if d and not os.path.isdir(d):
        os.makedirs(d)

def write_file(path, text):
    """UTF-8 writer with newline normalization + sanitization."""
    ensure_dir(os.path.dirname(path))
    with io.open(path, 'w', encoding='utf-8', newline=u'\n') as f:
        f.write(sanitize_text(_to_u(text)))

2) src/import_export.py (USE write_file + safe_filename)

At top: from util import write_file, safe_filename

Wherever you build output paths from object names, wrap with safe_filename(name).

Replace any open(out_path, 'w') blocks with write_file(out_path, text).

Example change:

# BEFORE
out_path = os.path.join(parent_dir, child.get_name() + '.st')
with open(out_path, 'w') as f:
    f.write(text)

# AFTER
out_path = os.path.join(parent_dir, safe_filename(child.get_name()) + '.st')
write_file(out_path, text)

3) src/communication_import_export.py (same treatment)

from util import write_file, safe_filename

Wrap names with safe_filename(...)

Replace file writes with write_file(...).

4) src/entrypoint.py (ADD helpers for destination override)

Add two helpers (non-breaking for existing callers):

import os, sys

def get_export_target(project_path, project_name, argv=None):
    """
    If argv[1] provided, use it as the export root (absolute or relative).
    Else, default to sibling '<ProjectName>ST' beside project.
    """
    argv = argv or sys.argv
    if len(argv) > 1 and argv[1]:
        return os.path.abspath(argv[1])
    parent = os.path.dirname(project_path)
    return os.path.join(parent, project_name + "ST")

def get_import_source(project_path, project_name, argv=None):
    """
    If argv[1] provided, use it as the import source folder.
    Else, default to sibling '<ProjectName>ST'.
    """
    argv = argv or sys.argv
    if len(argv) > 1 and argv[1]:
        return os.path.abspath(argv[1])
    parent = os.path.dirname(project_path)
    return os.path.join(parent, project_name + "ST")


(Keep existing find_application, find_communication, get_device_entrypoints, get_src_folder (if used elsewhere), but migrate scripts to new helpers.)

5) src/script_export_to_files.py (SUPPORT dest arg + robust errors)

At top: import io, sys, shutil, os

Import new helpers: from entrypoint import find_application, find_communication, get_device_entrypoints, get_export_target

Replace get_src_folder(...) usage with get_export_target(project_path, project_name, sys.argv)

Before deleting an existing folder, print a clear message; add --force behavior if desired.

Proposed body:

# REMEMBER: python 2.7
from __future__ import print_function
import os, sys, shutil
import scriptengine  # type: ignore

from communication_import_export import export_communication
from entrypoint import find_application, find_communication, get_device_entrypoints, get_export_target
from util import print_python_version, assert_project_open

def _project_info():
    p = scriptengine.projects.primary
    project_path = p.get_path()
    project_name = os.path.splitext(os.path.basename(project_path))[0]
    return project_path, project_name

try:
    print_python_version()
    assert_project_open()

    project_path, project_name = _project_info()
    out_dir = get_export_target(project_path, project_name, sys.argv)
    print("Writing to: " + out_dir)

    if os.path.exists(out_dir):
        try:
            shutil.rmtree(out_dir)
        except Exception as ex:
            print("WARN: could not remove existing dir '{}': {}".format(out_dir, ex))
            raise
    os.makedirs(out_dir)

    for device_obj in get_device_entrypoints(scriptengine.projects.primary):
        device_folder = os.path.join(out_dir, device_obj.get_name())
        os.mkdir(device_folder)

        application = find_application(device_obj)
        application_folder = os.path.join(device_folder, "application")
        os.mkdir(application_folder)

        for child_obj in application.get_children():
            # export_child comes from import_export module (kept as-is),
            # ensure it relies on util.write_file + util.safe_filename internally.
            from import_export import export_child
            export_child(child_obj, application, application_folder)

        communication = find_communication(device_obj)
        export_communication(communication, device_folder)

except Exception as e:
    # Show actionable hint for common Windows lock
    print(e)
    print("HINT: If you see [Errno 13] access denied, close editors/Explorer/OneDrive locking the export folder or export to a different path via argv.")
    raise

print("Done!")


Note: move export_child definition to import_export.py (it already conceptually belongs there), or import it where it currently lives.

6) src/script_import_from_files.py (SUPPORT source arg)

Import get_import_source, accept sys.argv[1] as import root; otherwise default to sibling <ProjectName>ST.

Print source path; errors should mention how to pass a different folder.

Sketch:

from __future__ import print_function
import os, sys
import scriptengine  # type: ignore
from entrypoint import get_import_source
from util import print_python_version, assert_project_open

try:
    print_python_version()
    assert_project_open()

    p = scriptengine.projects.primary
    project_path = p.get_path()
    project_name = os.path.splitext(os.path.basename(project_path))[0]
    src_dir = get_import_source(project_path, project_name, sys.argv)
    print("Importing from: " + src_dir)

    # existing import logic continues, reading files from src_dir
except Exception as e:
    print(e)
    raise

7) (Optional) README.md updates

Add usage examples for ScriptEngine console:

# Export to a custom folder (avoid file locks)
Tools → Scripting → Scripting Console:

import sys
sys.argv = [r"C:\codescribe\src\script_export_to_files.py",
            r"C:\_exports\IceMachine_Run1"]
execfile(r"C:\codescribe\src\script_export_to_files.py")

# Import from a custom folder
sys.argv = [r"C:\codescribe\src\script_import_from_files.py",
            r"C:\_exports\IceMachine_Run1"]
execfile(r"C:\codescribe\src\script_import_from_files.py")


Mention UTF-8 and filename sanitation.

Manual test plan

Unicode project content

Insert comments/names containing: – — “ ” ‘ ’ (NBSP) in POUs/Methods/Devices.

Run Export To Files (toolbar or console with custom path) → ✅ no ASCII errors; files appear.

Filename safety

Create POUs with names like Seal—Bar / Closed? → output filenames should be sane, e.g., Seal-Bar _ Closed_.st.

Custom export path

With the project open on Desktop, export to C:\_exports\Run_1 via console arg → ✅ succeeds, no [Errno 13].

Import round-trip

Edit an exported .st, run Import From Files with the same custom path → changes appear in CODESYS.

Lock handling

Open the export folder in Explorer with Preview Pane on; attempt export to the same folder → should either succeed (clean rmtree) or emit a clear warning and stop; then succeed to a new path.

Notes to Codex

Keep changes Python 2.7 compatible (no f-strings, no pathlib).

Don’t add third-party deps.

Minimize surface area: centralize writing/filenaming in util.py and ensure all export code paths call those helpers.

If any module performs its own open(..., 'w'), convert to write_file(...).

That’s everything needed.