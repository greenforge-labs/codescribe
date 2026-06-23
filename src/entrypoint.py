# REMEMBER: this is python 2.7
from object_type import ObjectType, get_object_type
from util import *


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


def _subtree_contains_type(root_obj, object_type):
    stack = [root_obj]
    while len(stack) > 0:
        current = stack.pop()
        if get_object_type(current) == object_type:
            return True
        for child in current.get_children():
            stack.append(child)
    return False


def find_application(device_obj):
    # Backward-compatible fast path for the classic default name.
    by_name = first_or_none(device_obj.find("Application", recursive=True))
    if by_name is not None:
        return by_name

    # Some projects rename the node (e.g. RAM3). Detect the application by the
    # stable object graph marker: it owns a Task Configuration in its subtree.
    candidates = []
    for child in device_obj.get_children():
        if _subtree_contains_type(child, ObjectType.TASK_CONFIGURATION):
            candidates.append(child)

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:
        names = ", ".join([c.get_name() for c in candidates])
        raise ValueError(
            "Found multiple application candidates inside "
            + device_obj.get_name()
            + ": "
            + names
            + ". Keep one entrypoint per device."
        )

    raise ValueError("Couldn't find Application inside " + device_obj.get_name())


def find_communication(device_obj):
    # Not every device has a Communication object - depends on the device package.
    # Callers must treat None as "skip the communication step".
    return first_or_none(device_obj.find("Communication", recursive=True))
