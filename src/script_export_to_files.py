# REMEMBER: this is python 2.7
from __future__ import print_function

import json
import os
import shutil

import scriptengine  # type: ignore

from communication_import_export import export_communication
from entrypoint import find_application, find_communication, get_device_entrypoints, get_src_folder
from import_export import OBJECT_TYPE_TO_EXPORT_FUNCTION
from object_type import get_object_type
from util import *


EXPORT_MANIFEST_FILENAME = ".codescribe_export_manifest.json"


def export_child(child_obj, parent_obj, parent_folder_path):
    child_obj_type = get_object_type(child_obj)
    export_fn = OBJECT_TYPE_TO_EXPORT_FUNCTION.get(child_obj_type)
    if export_fn is not None:
        export_fn(child_obj, parent_obj, parent_folder_path, export_child)


def _remove_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)


def prepare_export_destination(export_root, device_names):
    if not os.path.exists(export_root):
        os.makedirs(export_root)
    elif not os.path.isdir(export_root):
        raise ValueError("Selected export destination is not a directory: " + export_root)

    manifest_path = os.path.join(export_root, EXPORT_MANIFEST_FILENAME)
    previous_entries = []

    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r") as manifest_file:
                previous_entries = json.load(manifest_file) or []
        except Exception as e:
            print("Warning: unable to read previous export manifest ({}).".format(e))
            previous_entries = []

    for relative_path in previous_entries:
        target = os.path.join(export_root, relative_path)
        if os.path.exists(target):
            _remove_path(target)

    seen = set()
    for device_name in device_names:
        if device_name in seen:
            continue
        target = os.path.join(export_root, device_name)
        if os.path.exists(target):
            _remove_path(target)
        seen.add(device_name)

    return manifest_path


def write_export_manifest(manifest_path, device_names):
    try:
        with open(manifest_path, "w") as manifest_file:
            json.dump(device_names, manifest_file)
    except Exception as e:
        print("Warning: unable to write export manifest ({}).".format(e))


try:
    print_python_version()
    assert_project_open()

    project = scriptengine.projects.primary
    device_entrypoints = list(get_device_entrypoints(project))
    device_metadata = [
        (device_obj, ensure_utf8_bytes(device_obj.get_name())) for device_obj in device_entrypoints
    ]
    device_names = [name for (_, name) in device_metadata]

    default_folder = get_src_folder(project)
    export_folder = prompt_for_directory(
        default_folder,
        "Select a folder where CODESCRIBE should export project files.",
    )

    if export_folder is None:
        print("Export canceled by user; no files were written.")
        raise SystemExit

    manifest_path = prepare_export_destination(export_folder, device_names)
    print("Writing to: " + export_folder)

    for (device_obj, device_name) in device_metadata:
        device_folder = os.path.join(export_folder, device_name)
        if not os.path.exists(device_folder):
            os.makedirs(device_folder)

        application = find_application(device_obj)
        application_folder = os.path.join(device_folder, "application")
        if not os.path.exists(application_folder):
            os.makedirs(application_folder)

        for child_obj in application.get_children():
            export_child(child_obj, application, application_folder)

        communication = find_communication(device_obj)
        export_communication(communication, device_folder)

    write_export_manifest(manifest_path, device_names)
except Exception as e:
    print(e)
    raise e

print("Done!")
