# REMEMBER: this is python 2.7
from __future__ import print_function

import os

import scriptengine  # type: ignore

from communication_import_export import export_communication
from device_tree_import_export import export_device_tree_siblings
from entrypoint import find_application, find_communication, get_device_entrypoints, get_src_folder
from import_export import OBJECT_TYPE_TO_EXPORT_FUNCTION, write_native
from object_type import ObjectType, get_object_type
from util import *


def export_child(child_obj, parent_obj, parent_folder_path):
    child_obj_type = get_object_type(child_obj)
    export_fn = OBJECT_TYPE_TO_EXPORT_FUNCTION.get(child_obj_type)
    if export_fn is not None:
        export_fn(child_obj, parent_obj, parent_folder_path, export_child)
        return

    if child_obj_type == ObjectType.UNKNOWN:
        # An unmapped GUID would otherwise be dropped from the export without a trace
        # (seen with diagram objects such as an LD nested inside a CFC). Fall back to a
        # native export and keep walking the children.
        try:
            write_native(child_obj, os.path.join(parent_folder_path, child_obj.get_name() + ".xml"), recursive=False)
        except Exception as fallback_error:
            print(
                "Warning: failed to export '"
                + child_obj.get_name()
                + "' (unmapped type GUID "
                + str(child_obj.type)
                + "): "
                + str(fallback_error)
            )
        for c in child_obj.get_children():
            export_child(c, child_obj, parent_folder_path)


try:
    print_python_version()
    assert_project_open()

    src_folder = get_src_folder(scriptengine.projects.primary)
    print("Writing to: " + src_folder)

    staging_folder = begin_export_folder(src_folder)

    for device_obj in get_device_entrypoints(scriptengine.projects.primary):
        device_folder = os.path.join(staging_folder, device_obj.get_name())
        os.mkdir(device_folder)

        application = find_application(device_obj)
        application_folder = os.path.join(device_folder, "application")
        os.mkdir(application_folder)

        for child_obj in application.get_children():
            export_child(child_obj, application, application_folder)

        communication = find_communication(device_obj)
        if communication is not None:
            export_communication(communication, device_folder)

        export_device_tree_siblings(device_obj, device_folder, application, communication)

    finalize_export_folder(src_folder, staging_folder)
except Exception as e:
    print(e)
    ui_error_with_traceback("Export To Files failed!")
    raise e

print("Done!")
ui_info("Export To Files complete.\n\nWrote: " + src_folder)
