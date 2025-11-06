# REMEMBER: this is python 2.7
import os
import sys

from object_type import ObjectType, get_object_type
from util import first_or_error


def get_project_path(project):
    """
    Return the on-disk path to the current project.

    Older ScriptProject objects expose `.path` instead of `.get_path()`, so we
    try the method first and fall back to the attribute for compatibility.
    """
    path_getter = getattr(project, "get_path", None)
    if callable(path_getter):
        return path_getter()
    if hasattr(project, "path"):
        return project.path
    raise AttributeError("ScriptProject does not expose get_path() or path.")


def get_export_target(project_path, project_name, argv=None):
    """
    Determine export destination.
    """
    argv = argv or sys.argv
    if len(argv) > 1 and argv[1]:
        return os.path.abspath(argv[1])
    parent = os.path.dirname(project_path)
    return os.path.join(parent, project_name + "ST")


def get_import_source(project_path, project_name, argv=None):
    """
    Determine import source directory.
    """
    argv = argv or sys.argv
    if len(argv) > 1 and argv[1]:
        return os.path.abspath(argv[1])
    parent = os.path.dirname(project_path)
    return os.path.join(parent, project_name + "ST")


def get_src_folder(project):
    working_dir = os.path.dirname(project.path)
    project_name, project_extension = os.path.splitext(os.path.basename(project.path))
    src_folder = os.path.join(working_dir, project_name)

    return src_folder


def get_device_entrypoints(project):
    children = project.get_children()
    for child in children:
        if len(child.get_children()) < 1:
            continue

        if get_object_type(child) != ObjectType.DEVICE:
            continue

        yield child


def find_application(device_obj):
    return first_or_error(
        device_obj.find("Application", recursive=True),
        "Couldn't find Application inside " + device_obj.get_name(),
    )


def find_communication(device_obj):
    return first_or_error(
        device_obj.find("Communication", recursive=True),
        "Couldn't find Communication inside " + device_obj.get_name(),
    )
