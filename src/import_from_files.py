import os

from communication_import_export import import_communication
from entrypoint import find_application, find_communication, get_device_entrypoints, get_src_folder
from import_export import *
from util import assert_path_exists, find_safe_name, safe_filename


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

    if filename.endswith(".gvl"):
        if ext == ".xml":
            # this is just here to point out that the xml is imported alongside the st file
            pass
        if ext == ".st":
            import_gvl(child, dir_path, dir_parent_obj, import_directory)
    elif "." in filename:
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


def import_from_files(project, src_folder=None):
    if src_folder is None:
        src_folder = get_src_folder(project)
    print("Reading from: " + src_folder)
    assert_path_exists(src_folder)

    for device_obj in get_device_entrypoints(project):
        safe_device_name = find_safe_name(src_folder, device_obj.get_name(), kind="dir") or safe_filename(
            device_obj.get_name()
        )
        device_folder = os.path.join(src_folder, safe_device_name)
        assert_path_exists(device_folder)

        application = find_application(device_obj)
        application_safe = find_safe_name(device_folder, application.get_name(), kind="dir") or "application"
        application_folder = os.path.join(device_folder, application_safe)
        assert_path_exists(application_folder)
        remove_tracked_objects(application.get_children())
        import_directory(application_folder, application)

        communication = find_communication(device_obj)
        import_communication(communication, device_folder)
