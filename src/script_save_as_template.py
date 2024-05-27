# REMEMBER: this is python 2.7
from __future__ import print_function

import os
import shutil

import scriptengine  # type: ignore

from entrypoint import find_application, get_device_entrypoints
from import_export import *
from util import *

PROJECT_EXT = ".project"


def find_template_paths(project):
    working_dir = os.path.dirname(project.path)
    project_name, _ = os.path.splitext(os.path.basename(scriptengine.projects.primary.path))

    template_name_start = project_name + "_template_v"

    for child in os.listdir(working_dir):
        name, ext = os.path.splitext(child)
        if ext == PROJECT_EXT and name.startswith(template_name_start):
            version_str = name.replace(template_name_start, "")
            try:
                version = int(version_str)
            except ValueError:
                raise ValueError("Found a template with invalid version: " + version_str)

            new_version = version + 1

            print("Found a template with version: " + str(version))
            print("New template version: " + str(new_version))

            template_path = os.path.join(working_dir, child)
            new_template_path = os.path.join(working_dir, template_name_start + str(new_version) + PROJECT_EXT)
            return template_path, new_template_path

    print("No existing template found!")
    print("New template version: 1")

    template_path = None
    new_template_path = os.path.join(working_dir, template_name_start + "1" + PROJECT_EXT)
    return template_path, new_template_path


print_python_version()
assert_project_open()

template_path, new_template_path = find_template_paths(scriptengine.projects.primary)

shutil.copyfile(scriptengine.projects.primary.path, new_template_path)
scriptengine.projects.open(new_template_path, primary=False)

template_project = scriptengine.projects.get_by_path(new_template_path)

for device_obj in get_device_entrypoints(template_project):
    application = find_application(device_obj)
    remove_tracked_objects(application.get_children())

template_project.save()

if template_path is not None:
    os.remove(template_path)

print("Done!")
