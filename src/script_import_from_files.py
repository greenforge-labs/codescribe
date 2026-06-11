# REMEMBER: this is python 2.7
from __future__ import print_function

import scriptengine  # type: ignore

from import_from_files import import_from_files
from util import *

try:
    print_python_version()
    assert_project_open()

    ui_continue = scriptengine.system.ui.prompt(
        "Import From Files will overwrite unexported changes in the current project!\n\nDo you want to continue?",
        choice=scriptengine.PromptChoice.YesNo,
        default_result=scriptengine.PromptResult.No,
        store_description="Don't show again",
        store_key="import_from_files_confirm",
    )

    if ui_continue == scriptengine.PromptResult.Yes:
        import_from_files(scriptengine.projects.primary)
        ui_info("Import From Files complete.")
    else:
        print("Import cancelled.")
except Exception as e:
    print(e)
    ui_error_with_traceback("Import From Files failed!")
    raise e

print("Done!")
