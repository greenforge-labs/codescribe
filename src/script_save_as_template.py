# REMEMBER: this is python 2.7
from __future__ import print_function

import os
import shutil

import scriptengine  # type: ignore

from entrypoint import find_application, get_device_entrypoints
from import_export import *
from project_template import find_template_paths_and_versions, generate_template_path
from util import *

PROJECT_EXT = ".project"


def get_new_template_version(template_versions):
    if len(template_versions) < 1:
        print("No existing template found!")
        print("New template version: 1")
        return 1

    current_version = max(template_versions)
    new_version = current_version + 1
    print("Found a template with version: " + str(current_version))
    print("New template version: " + str(new_version))
    return new_version


def delete_old_templates(template_paths):
    print("Deleting " + str(len(template_paths)) + " old template(s):")
    for path in template_paths:
        print(path)
        os.remove(path)


print_python_version()
assert_project_open()

template_paths, template_versions = find_template_paths_and_versions(scriptengine.projects.primary)
new_template_version = get_new_template_version(template_versions)
new_template_path = generate_template_path(scriptengine.projects.primary, new_template_version)

shutil.copyfile(scriptengine.projects.primary.path, new_template_path)
scriptengine.projects.open(new_template_path, primary=False)

template_project = scriptengine.projects.get_by_path(new_template_path)

for device_obj in get_device_entrypoints(template_project):
    application = find_application(device_obj)
    remove_tracked_objects(application.get_children())

template_project.save()

if len(template_paths) > 0:
    delete_old_templates(template_paths)

print("Done!")
