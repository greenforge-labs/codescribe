"""Fail if any file in src/ contains a non-ASCII byte.

CODESYS ScriptEngine is IronPython 2.7, which enforces PEP 263: source files
must be pure ASCII unless an encoding is declared. A stray em-dash or smart
quote in a comment makes CODESYS refuse to load the file at all. Python 3
py_compile cannot catch this because Python 3 source defaults to UTF-8.

Runs under Python 3 (CI) or Python 2 - byte scanning only, no imports.
"""

import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src")

failures = []
for name in sorted(os.listdir(SRC)):
    if not name.endswith(".py"):
        continue
    path = os.path.join(SRC, name)
    with open(path, "rb") as f:
        data = f.read()
    line = 1
    for i in range(len(data)):
        b = data[i] if isinstance(data[i], int) else ord(data[i])
        if b == 0x0A:
            line += 1
        elif b > 0x7F:
            failures.append("%s:%d: non-ASCII byte 0x%02X" % (name, line, b))

for failure in failures:
    print("FAIL    " + failure)
if not failures:
    print("OK      all src/*.py files are pure ASCII")
sys.exit(1 if failures else 0)
