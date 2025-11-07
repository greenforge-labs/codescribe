# REMEMBER: this is python 2.7
import os
import sys

import scriptengine  # type: ignore

from object_type import get_object_type

IS_PY2 = sys.version_info[0] == 2
try:
    TEXT_TYPE = unicode  # type: ignore[name-defined]
except NameError:
    TEXT_TYPE = str


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


def ensure_utf8_bytes(value):
    if IS_PY2 and isinstance(value, TEXT_TYPE):
        return value.encode("utf-8")
    return value


def prompt_for_directory(initial_path, description):
    """
    Show a folder picker seeded with ``initial_path`` and return the selected directory.
    If the picker is not available (e.g. running outside IronPython), fall back to ``initial_path``.
    """
    initial_path = ensure_utf8_bytes(initial_path)

    try:
        import clr  # type: ignore

        clr.AddReference("System.Windows.Forms")
    except Exception as e:  # pragma: no cover - depends on host environment
        print("Folder picker unavailable ({}); using default path.".format(e))
        return initial_path

    from System.Windows.Forms import DialogResult, FolderBrowserDialog  # type: ignore

    dialog = FolderBrowserDialog()
    dialog.Description = description
    if initial_path and os.path.isdir(initial_path):
        dialog.SelectedPath = initial_path

    result = dialog.ShowDialog()
    if result == DialogResult.OK and dialog.SelectedPath:
        selected_path = TEXT_TYPE(dialog.SelectedPath)
        return ensure_utf8_bytes(selected_path)

    return None
