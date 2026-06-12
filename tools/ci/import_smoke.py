# REMEMBER: this is python 2.7 - runs under IronPython, the engine CODESYS embeds.
"""Import every library module in src/ with a stubbed scriptengine.

Compilation alone misses module-scope mistakes (bad names in dispatch tables,
broken imports between modules). Importing executes module-level code, which
is as close as CI can get to CODESYS loading the scripts.

The script_*.py entry scripts are excluded: they execute their main logic at
import time and require a live CODESYS project.
"""
from __future__ import print_function

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "src"))
sys.path.insert(0, HERE)  # provides the scriptengine stub

MODULES = [
    "object_type",
    "util",
    "entrypoint",
    "import_export",
    "communication_import_export",
    "import_from_files",
    "project_template",
]

failures = []
for module in MODULES:
    try:
        __import__(module)
        print("OK      import " + module)
    except Exception as e:
        failures.append(module)
        print("FAIL    import %s: %r" % (module, e))

sys.exit(1 if failures else 0)
