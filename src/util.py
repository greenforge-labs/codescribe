# REMEMBER: this is python 2.7
import io
import os
import shutil
import sys
import traceback
import codecs

import scriptengine  # type: ignore

from object_type import get_object_type

EXPORT_STAGING_SUFFIX = ".codescribe_staging"
EXPORT_BACKUP_SUFFIX = ".codescribe_backup"


class ExportFolderLockedError(EnvironmentError):
    """The target export folder could not be replaced. The completed export is
    preserved in the staging folder."""


class NothingExportedError(EnvironmentError):
    """The export produced no files at all, so the existing export folder was
    left untouched rather than being replaced with an empty one."""


def begin_export_folder(target_folder):
    # The export is written into a sibling staging folder and only swapped into
    # place once it completes, so a locked target folder or a mid-export crash
    # cannot destroy the existing on-disk copy.
    staging_folder = target_folder + EXPORT_STAGING_SUFFIX
    if os.path.exists(staging_folder):
        shutil.rmtree(staging_folder)
    os.mkdir(staging_folder)
    return staging_folder


def _remove_stale_files(staging_folder, target_folder):
    """Delete target files this export did not write. Returns those that stay.

    The swap path replaces the folder wholesale, so anything the export did
    not produce is gone by definition. The sync path has to do the same, or a
    rendering from a previous export is left beside a new native xml and
    describes a POU that has since changed - with nothing to say so. Renaming
    a folder is what a lock stops; deleting a file inside it usually still
    works, and where it does not the file is named rather than left silent.
    """
    stale = []
    for dir_path, _dir_names, file_names in os.walk(target_folder):
        relative = os.path.relpath(dir_path, target_folder)
        source = staging_folder if relative == "." else os.path.join(staging_folder, relative)
        for file_name in file_names:
            if os.path.exists(os.path.join(source, file_name)):
                continue
            try:
                os.remove(os.path.join(dir_path, file_name))
            except (OSError, IOError):
                stale.append(os.path.join(dir_path, file_name))
    return stale


def _sync_export_files(staging_folder, target_folder):
    # Overwrite sync; anything in the target the export did not write is
    # removed afterwards by _remove_stale_files.
    for dir_path, dir_names, file_names in os.walk(staging_folder):
        relative = os.path.relpath(dir_path, staging_folder)
        destination = target_folder if relative == "." else os.path.join(target_folder, relative)
        if not os.path.isdir(destination):
            os.makedirs(destination)
        for file_name in file_names:
            shutil.copy2(os.path.join(dir_path, file_name), os.path.join(destination, file_name))


def _folder_has_files(folder):
    for _dir_path, _dir_names, file_names in os.walk(folder):
        if file_names:
            return True
    return False


def finalize_export_folder(target_folder, staging_folder):
    # An export that wrote no files must never replace the previous export:
    # swapping in an empty staging folder silently destroys it. Seen when
    # Export Lib To Files runs on a device project - its walker only exports
    # objects directly under the project root, and a device project keeps
    # everything under Devices, so the walk produces nothing.
    if not _folder_has_files(staging_folder):
        shutil.rmtree(staging_folder)
        raise NothingExportedError(
            "Nothing was exported, so the existing export folder was left untouched: "
            + target_folder
            + ". Export To Files needs a device project (objects under a Device); Export Lib To Files"
            + " needs a library project (objects directly under the project root)."
        )

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
            stale = _remove_stale_files(staging_folder, target_folder)
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
        print(
            "Export folder "
            + target_folder
            + " is in use; synced the staged files into it instead of swapping folders."
        )
        if stale:
            print(
                "WARNING: "
                + str(len(stale))
                + " file(s) this export did not write could not be removed and are now stale: "
                + ", ".join(stale[:6])
            )
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
    # punctuation. codecs.open with an explicit encoding keeps everything UTF-8 round-trippable.
    #
    # io.open(path, mode, encoding="utf-8") looks equivalent but is unreliable on the
    # IronPython 2.7 runtime CODESYS ScriptEngine uses: encoding resolution can silently
    # fall back to the OS ANSI code page instead of true UTF-8, which corrupts any
    # non ASCII character(umlauts, accented letters, smart punctuation, etc.) on export and
    # then fail to decode on the next import ("'unknown' codec can't decode byte ...").
    # codec.open is the long-standing, well-supported way to do UTF-8 text I/O on 
    # Python 2 / IronPython and does not have this problems.
    return codecs.open(path, mode, encoding="utf-8")


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
