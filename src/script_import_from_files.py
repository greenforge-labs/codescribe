# REMEMBER: this is python 2.7
from __future__ import print_function

import os

import scriptengine  # type: ignore

from entrypoint import find_application, get_device_entrypoints, get_src_folder
from import_export import *
from util import *


def first_word_of_line_iter(f):
    for line in f.readlines():
        words = line.strip().split()
        if len(words) > 0:
            yield words[0]


def import_directory(dir_path, dir_parent_obj):
    children = os.listdir(dir_path)
    # this is a naughty way to ensure parent POU's are created before their children
    for child in sorted(children, key=lambda x: x.count(".")):
        import_directory_child(child, dir_path, dir_parent_obj)


def import_directory_child(child, dir_path, dir_parent_obj):
    full_path = os.path.join(dir_path, child)
    filename, ext = os.path.splitext(child)

    if os.path.isdir(full_path):
        import_folder(child, dir_path, dir_parent_obj, import_directory)

    if "." in filename:
        # . means some sort of sub POU
        if ext == ".xml":
            import_sub_pou(child, dir_path, dir_parent_obj, import_directory)
        if ext == ".st":
            # currently only methods are exported as ST if possible
            import_method_st(child, dir_path, dir_parent_obj, import_directory)
    else:
        if ext == ".xml":
            import_native(child, dir_path, dir_parent_obj, import_directory)
        if ext == ".st":
            # Have to check for keywords to determine if POU or DUT
            with open(full_path, "r") as f:
                for word in first_word_of_line_iter(f):
                    if word == "TYPE":
                        import_dut(child, dir_path, dir_parent_obj, import_directory)

                    if word in ["PROGRAM", "FUNCTION_BLOCK", "FUNCTION"]:
                        import_pou_st(child, dir_path, dir_parent_obj, import_directory)


print_python_version()
assert_project_open()

src_folder = get_src_folder(scriptengine.projects.primary)
print("Reading from: " + src_folder)
assert_path_exists(src_folder)

for device_obj in get_device_entrypoints(scriptengine.projects.primary):
    device_folder = os.path.join(src_folder, device_obj.get_name())
    assert_path_exists(device_folder)

    application = find_application(device_obj)
    remove_tracked_objects(application.get_children())

    import_directory(device_folder, application)

print("Done!")
