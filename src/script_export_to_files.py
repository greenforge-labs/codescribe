# REMEMBER: this is python 2.7
from __future__ import print_function

import os
import shutil

import scriptengine  # type: ignore

from entrypoint import find_application, get_device_entrypoints, get_src_folder
from import_export import OBJECT_TYPE_TO_EXPORT_FUNCTION
from object_type import get_object_type
from util import *


def export_application_child(child_obj, parent_obj, parent_folder_path):
    child_obj_type = get_object_type(child_obj)
    export_fn = OBJECT_TYPE_TO_EXPORT_FUNCTION.get(child_obj_type)
    if export_fn is not None:
        export_fn(child_obj, parent_obj, parent_folder_path, export_application_child)


print_python_version()
assert_project_open()

src_folder = get_src_folder(scriptengine.projects.primary)
print("Writing to: " + src_folder)

if os.path.exists(src_folder):
    shutil.rmtree(src_folder)
os.mkdir(src_folder)

for device_obj in get_device_entrypoints(scriptengine.projects.primary):
    device_folder = os.path.join(src_folder, device_obj.get_name())
    os.mkdir(device_folder)

    application = find_application(device_obj)

    for child_obj in application.get_children():
        export_application_child(child_obj, application, device_folder)

print("Done!")
