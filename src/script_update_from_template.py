# REMEMBER: this is python 2.7
from __future__ import print_function

import os
import shutil

import scriptengine  # type: ignore

from import_from_files import import_from_files
from project_template import find_template_paths_and_versions
from util import *


def get_newest_template_path(template_paths, template_versions):
    newest_version = max(template_versions)
    newest_idx = template_versions.index(newest_version)
    newest_path = template_paths[newest_idx]
    print("Found template version " + str(newest_version) + " at " + newest_path)
    return newest_path


try:
    print_python_version()
    assert_project_open()

    template_paths, template_versions = find_template_paths_and_versions(scriptengine.projects.primary)
    newest_template_path = get_newest_template_path(template_paths, template_versions)

    ui_continue = scriptengine.system.ui.prompt(
        "Update From Template will overwrite unexported changes in the current project!\n\nDo you want to continue?",
        choice=scriptengine.PromptChoice.YesNo,
        default_result=scriptengine.PromptResult.No,
        store_description="Don't show again",
        store_key="update_from_template_confirm",
    )

    if ui_continue == scriptengine.PromptResult.Yes:
        project_path = scriptengine.projects.primary.path

        scriptengine.projects.primary.close()
        shutil.copyfile(newest_template_path, project_path)
        scriptengine.projects.open(project_path)

        import_from_files(scriptengine.projects.primary)

        scriptengine.projects.primary.save()
except Exception as e:
    print(e)
    raise e

print("Done!")
