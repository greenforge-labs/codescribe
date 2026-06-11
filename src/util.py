# REMEMBER: this is python 2.7
import io
import os
import sys
import traceback

import scriptengine  # type: ignore

from object_type import get_object_type


def ui_info(message):
    # Blocking dialog; the message view is easy to miss, so entry scripts report
    # their outcome through these as well.
    scriptengine.system.ui.info(message)


def ui_error_with_traceback(message):
    scriptengine.system.ui.error(message + "\n\n" + traceback.format_exc())


def open_utf8(path, mode):
    # ScriptEngine runs on Python 2.7; the builtin open() writes a byte stream and would
    # implicitly encode unicode text as ascii, crashing on Cyrillic / accented chars / smart
    # punctuation. io.open with an explicit encoding keeps everything UTF-8 round-trippable.
    return io.open(path, mode, encoding="utf-8")


def print_python_version():
    print("Python version: " + sys.version)


def assert_project_open():
    if scriptengine.projects.primary is None:
        raise ValueError("You must have a project open!")


def assert_path_exists(path):
    if not os.path.exists(path):
        raise ValueError("Path " + path + " does not exist")


def first_or_none(lst):
    return next(iter(lst), None)


def first_of_type_or_error(lst, obj_type, err):
    for obj in lst:
        if get_object_type(obj) == obj_type:
            return obj
    raise ValueError(err)


def first_of_type_or_none(lst, obj_type):
    for obj in lst:
        if get_object_type(obj) == obj_type:
            return obj
    return None


def first_or_error(lst, err):
    try:
        return next(iter(lst))
    except StopIteration:
        raise ValueError(err)
