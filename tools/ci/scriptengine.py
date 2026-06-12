# REMEMBER: this is python 2.7
"""Stub of the CODESYS-injected scriptengine module, for CI import tests only.

The real module exists solely inside the CODESYS ScriptEngine host. The src
modules only touch it inside function bodies, so an attribute sponge is enough
to let them import. If a future change accesses scriptengine at module scope
in a way this stub cannot satisfy, the import smoke test fails - which is
exactly the kind of regression it exists to catch.
"""


class _Anything(object):
    def __getattr__(self, name):
        return _Anything()

    def __call__(self, *args, **kwargs):
        return _Anything()


projects = _Anything()
system = _Anything()
online = _Anything()
ImplementationLanguages = _Anything()
PromptChoice = _Anything()
PromptResult = _Anything()
