# REMEMBER: this is python 2.7
from __future__ import print_function

import os

import scriptengine  # type: ignore

from entrypoint import get_src_folder
import graphical_export
from import_export import OBJECT_TYPE_TO_EXPORT_FUNCTION, SERVICE_EXPORT_FUNCTIONS, write_native
from object_type import ObjectType, get_object_type
from util import *

# Service objects that are not source. The manager objects carry GUIDs that are not in
# GUID_TYPE_MAPPING, so without this list the UNKNOWN fallback below would export them
# as native xml noise.
SKIP_NAMES = [
    "Library Manager",
    "Project Information",
    "Project Settings",
    "Task Configuration",
    "Symbol Configuration",
    "Visualization Manager",
    "Alarm Configuration",
    "Recipe Manager",
    "__VisualizationStyle",  # auto-created in every project; native export of it fails
]


def export_child(child_obj, parent_obj, parent_folder_path):
    # Keep this consistent with export_child in script_export_to_files.py. Entry
    # scripts execute at import time, so it cannot be imported from there.
    child_obj_type = get_object_type(child_obj)
    export_fn = OBJECT_TYPE_TO_EXPORT_FUNCTION.get(child_obj_type)
    if export_fn is not None:
        export_fn(child_obj, parent_obj, parent_folder_path, export_child)
        return

    # Read-only informational exports (library list, visualisation manager).
    # In library projects these managers usually carry unmapped GUIDs and are
    # filtered by SKIP_NAMES above instead; the branch is here for consistency
    # with script_export_to_files.py.
    service_fn = SERVICE_EXPORT_FUNCTIONS.get(child_obj_type)
    if service_fn is not None:
        service_fn(child_obj, parent_obj, parent_folder_path, export_child)
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
    graphical_export.reset_stats()

    src_folder = get_src_folder(scriptengine.projects.primary)
    print("Writing to: " + src_folder)

    # A device project keeps its objects under Devices, which this walker never
    # enters - the "export" would be empty. Refuse up front with a pointer to
    # the right button instead of touching anything on disk.
    for child_obj in scriptengine.projects.primary.get_children():
        if get_object_type(child_obj) == ObjectType.DEVICE:
            raise ValueError(
                "This project has a device ('"
                + child_obj.get_name()
                + "'), so it is not a library project. Use Export To Files instead;"
                + " Export Lib To Files only exports objects directly under the project root."
            )

    staging_folder = begin_export_folder(src_folder)

    for child_obj in scriptengine.projects.primary.get_children():
        if child_obj.get_name() in SKIP_NAMES:
            continue

        child_obj_type = get_object_type(child_obj)
        if child_obj_type != ObjectType.UNKNOWN and child_obj_type not in OBJECT_TYPE_TO_EXPORT_FUNCTION:
            continue

        # Passing None as parent_obj is safe at the top level: the export functions
        # that use parent_obj.get_name() (METHOD, PROPERTY, ACTION, TRANSITION) only
        # apply to children of POUs, and export_pou passes the POU as the parent when
        # recursing into them.
        export_child(child_obj, None, staging_folder)

    finalize_export_folder(src_folder, staging_folder)

    rendering_summary = graphical_export.summary()
    if rendering_summary is not None:
        print(rendering_summary)
except Exception as e:
    print(e)
    ui_error_with_traceback("Export Lib To Files failed.")
    raise e

print("Done!")
ui_info("Export Lib To Files complete.\n\nWrote: " + src_folder)
