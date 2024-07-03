# REMEMBER: this is python 2.7
import os

import scriptengine  # type: ignore

PROJECT_EXT = ".project"
TEMPLATE_FILEPART = "_template_v"


def find_template_paths_and_versions(project):
    working_dir = os.path.dirname(project.path)
    project_name, _ = os.path.splitext(os.path.basename(scriptengine.projects.primary.path))

    template_name_start = project_name + TEMPLATE_FILEPART

    template_paths = []
    template_versions = []

    for child in os.listdir(working_dir):
        name, ext = os.path.splitext(child)
        if ext == PROJECT_EXT and name.startswith(template_name_start):
            version_str = name.replace(template_name_start, "")
            try:
                version = int(version_str)
            except ValueError:
                raise ValueError("Found a template with invalid version: " + version_str)

            template_paths.append(os.path.join(working_dir, child))
            template_versions.append(version)

    return template_paths, template_versions


def generate_template_path(project, version_number):
    working_dir = os.path.dirname(project.path)
    project_name, _ = os.path.splitext(os.path.basename(scriptengine.projects.primary.path))

    template_name_start = project_name + TEMPLATE_FILEPART

    return os.path.join(working_dir, template_name_start + str(version_number) + PROJECT_EXT)
