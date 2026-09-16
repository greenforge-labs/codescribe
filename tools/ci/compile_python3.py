"""Compile src/*.py with the host Python 3 interpreter."""
import os
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "src")

failures = []
for name in sorted(os.listdir(SRC)):
    if not name.endswith(".py"):
        continue
    path = os.path.join(SRC, name)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            source = handle.read()
        compile(source, path, "exec")
        print("OK      " + name)
    except (OSError, SyntaxError) as error:
        failures.append(name)
        print("FAIL    %s: %s" % (name, error))

sys.exit(1 if failures else 0)
