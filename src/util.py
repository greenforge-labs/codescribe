# REMEMBER: this is python 2.7
import io
import os
import shutil
import sys
import traceback

import scriptengine  # type: ignore

from object_type import get_object_type

EXPORT_STAGING_SUFFIX = ".codescribe_staging"
EXPORT_BACKUP_SUFFIX = ".codescribe_backup"


class ExportFolderLockedError(EnvironmentError):
    """The target export folder could not be replaced. The completed export is
    preserved in the staging folder."""


def begin_export_folder(target_folder):
    # The export is written into a sibling staging folder and only swapped into
    # place once it completes, so a locked target folder or a mid-export crash
    # cannot destroy the existing on-disk copy.
    staging_folder = target_folder + EXPORT_STAGING_SUFFIX
    if os.path.exists(staging_folder):
        shutil.rmtree(staging_folder)
    os.mkdir(staging_folder)
    return staging_folder


def _sync_export_files(staging_folder, target_folder):
    # Overwrite sync only; files that exist in the target but not in staging are
    # left in place, because deleting them would require the same folder access
    # that already failed for the rename.
    for dir_path, dir_names, file_names in os.walk(staging_folder):
        relative = os.path.relpath(dir_path, staging_folder)
        destination = target_folder if relative == "." else os.path.join(target_folder, relative)
        if not os.path.isdir(destination):
            os.makedirs(destination)
        for file_name in file_names:
            shutil.copy2(os.path.join(dir_path, file_name), os.path.join(destination, file_name))


def finalize_export_folder(target_folder, staging_folder):
    backup_folder = target_folder + EXPORT_BACKUP_SUFFIX
    try:
        if os.path.exists(target_folder):
            if os.path.exists(backup_folder):
                shutil.rmtree(backup_folder)
            os.rename(target_folder, backup_folder)
        os.rename(staging_folder, target_folder)
    except (OSError, IOError) as rename_error:
        # On Windows these renames fail while another program holds a handle on
        # the target folder. Fall back to copying the staged files into it.
        try:
            _sync_export_files(staging_folder, target_folder)
            shutil.rmtree(staging_folder)
        except (OSError, IOError):
            raise ExportFolderLockedError(
                "Could not replace the export folder "
                + target_folder
                + ". It is likely locked by another program (an open Explorer window, IDE, git client or antivirus)."
                + " The completed export is preserved in "
                + staging_folder
                + ". Original error: "
                + str(rename_error)
            )
        print("Export folder " + target_folder + " is in use; synced the staged files into it instead of swapping folders.")
        return
    try:
        if os.path.exists(backup_folder):
            shutil.rmtree(backup_folder)
    except (OSError, IOError) as backup_error:
        # The export itself succeeded at this point; a leftover backup folder is
        # not worth failing it over.
        print("Warning: could not delete backup folder " + backup_folder + ": " + str(backup_error))


def ui_info(message):
    # Blocking dialog; the message view is easy to miss, so entry scripts report
    # their outcome through these as well.
    scriptengine.system.ui.info(message)


def ui_error_with_traceback(message):
    scriptengine.system.ui.error(message + "\n\n" + traceback.format_exc())


def open_utf8(path, mode):
    # ScriptEngine runs on Python 2.7; the builtin open() writes a byte stream and would
    # implicitly encode unicode text as ascii, crashing on Cyrillic / accented chars / smart
    # punctuation. io.open with an explicit encoding keeps everything UTF-8 round-trippable.
    return io.open(path, mode, encoding="utf-8")


def print_python_version():
    print("Python version: " + sys.version)


def assert_project_open():
    if scriptengine.projects.primary is None:
        raise ValueError("You must have a project open!")


def assert_path_exists(path):
    if not os.path.exists(path):
        raise ValueError("Path " + path + " does not exist")


def first_or_none(lst):
    return next(iter(lst), None)


def first_of_type_or_error(lst, obj_type, err):
    for obj in lst:
        if get_object_type(obj) == obj_type:
            return obj
    raise ValueError(err)


def first_of_type_or_none(lst, obj_type):
    for obj in lst:
        if get_object_type(obj) == obj_type:
            return obj
    return None


def first_or_error(lst, err):
    try:
        return next(iter(lst))
    except StopIteration:
        raise ValueError(err)
