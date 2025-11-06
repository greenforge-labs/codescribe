# REMEMBER: this is python 2.7
from __future__ import print_function

import os
import sys

import scriptengine  # type: ignore

from import_from_files import import_from_files
from entrypoint import get_import_source, get_project_path
from util import assert_project_open, print_python_version

try:
    print_python_version()
    assert_project_open()

    project = scriptengine.projects.primary
    project_path = get_project_path(project)
    project_name = os.path.splitext(os.path.basename(project_path))[0]
    src_dir = get_import_source(project_path, project_name, sys.argv)
    print("Importing from: " + src_dir)

    ui_continue = scriptengine.system.ui.prompt(
        "Import From Files will overwrite unexported changes in the current project!\n\nDo you want to continue?",
        choice=scriptengine.PromptChoice.YesNo,
        default_result=scriptengine.PromptResult.No,
        store_description="Don't show again",
        store_key="import_from_files_confirm",
    )

    if ui_continue == scriptengine.PromptResult.Yes:
        import_from_files(project, src_dir)
except Exception as e:
    print(e)
    print("HINT: Pass a custom source folder via argv[1] to avoid locked or missing files.")
    raise

print("Done!")
