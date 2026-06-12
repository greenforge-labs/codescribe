# REMEMBER: this is python 2.7 - runs under IronPython, the engine CODESYS embeds.
"""Compile every file in src/ with the real IronPython 2.7 compiler.

This catches Python 2 syntax errors the way CODESYS ScriptEngine would,
which py_compile under Python 3 cannot.

Note: IronPython's compile() of an in-memory string does NOT enforce PEP 263
(verified empirically; only the file-based execute/import paths do). Encoding
violations are covered by check_ascii.py, and by import_smoke.py for the
library modules, so this script owns the syntax class only.
"""
from __future__ import print_function

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src")

failures = []
for name in sorted(os.listdir(SRC)):
    if not name.endswith(".py"):
        continue
    path = os.path.join(SRC, name)
    f = open(path, "rU")
    try:
        source = f.read()
    finally:
        f.close()

    try:
        compile(source, path, "exec")
        print("OK      " + name)
    except SyntaxError as e:
        failures.append(name)
        print("FAIL    %s: %s" % (name, e))

sys.exit(1 if failures else 0)
