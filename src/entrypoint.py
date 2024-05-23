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


def find_application(device_obj):
    return first_or_error(
        device_obj.find("Application", recursive=True),
        "Couldn't find Application inside " + device_obj.get_name(),
    )
