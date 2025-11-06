# REMEMBER: this is python 2.7
from __future__ import print_function

import os
import shutil
import sys

import scriptengine  # type: ignore

from communication_import_export import export_communication
from entrypoint import (
    find_application,
    find_communication,
    get_device_entrypoints,
    get_export_target,
    get_project_path,
)
from import_export import export_child
from util import assert_project_open, print_python_version, register_directory, safe_filename


def _project_info():
    project = scriptengine.projects.primary
    project_path = get_project_path(project)
    project_name = os.path.splitext(os.path.basename(project_path))[0]
    return project_path, project_name


try:
    print_python_version()
    assert_project_open()

    project_path, project_name = _project_info()
    out_dir = get_export_target(project_path, project_name, sys.argv)
    print("Writing to: " + out_dir)

    if os.path.exists(out_dir):
        print("Removing existing: " + out_dir)
        try:
            shutil.rmtree(out_dir)
        except Exception as ex:
            print("WARN: could not remove existing dir '{}': {}".format(out_dir, ex))
            raise
    os.makedirs(out_dir)

    for device_obj in get_device_entrypoints(scriptengine.projects.primary):
        device_folder = os.path.join(out_dir, safe_filename(device_obj.get_name()))
        os.mkdir(device_folder)
        register_directory(out_dir, os.path.basename(device_folder), device_obj.get_name())

        application = find_application(device_obj)
        application_folder = os.path.join(device_folder, "application")
        os.mkdir(application_folder)
        register_directory(device_folder, "application", application.get_name())

        for child_obj in application.get_children():
            export_child(child_obj, application, application_folder)

        communication = find_communication(device_obj)
        export_communication(communication, device_folder)

except Exception as e:
    print(e)
    print(
        "HINT: If you see [Errno 13] access denied, close editors/Explorer/OneDrive locking the export folder or export to a different path via argv."
    )
    raise

print("Done!")
