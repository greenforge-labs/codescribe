import os

from import_export import write_native
from object_type import ObjectType, get_object_type
from util import first_of_type_or_error, first_of_type_or_none, register_directory, resolve_original_name, safe_filename

NO_EXPORT_FOLDER_NAME = "_NO_EXPORT"


def no_export_folder_exists(communication_obj):
    return first_of_type_or_none(communication_obj.find(NO_EXPORT_FOLDER_NAME), ObjectType.FOLDER) is not None


def export_communication(communication_obj, device_folder):
    """
    Export communication is hardcoded to create folders for the top level devices inside the communication object, and
    then do a native recursive export for any devices under those top level devices.
    """
    if no_export_folder_exists(communication_obj):
        return

    communication_folder_name = "communication"
    communication_folder = os.path.join(device_folder, communication_folder_name)
    os.mkdir(communication_folder)
    register_directory(device_folder, communication_folder_name, communication_obj.get_name())

    for top_level_device in communication_obj.get_children():
        safe_device_name = safe_filename(top_level_device.get_name())
        top_level_device_folder = os.path.join(communication_folder, safe_device_name)
        os.mkdir(top_level_device_folder)
        register_directory(communication_folder, safe_device_name, top_level_device.get_name())
        for child_device in top_level_device.get_children():
            child_safe_name = safe_filename(child_device.get_name())
            write_native(
                child_device,
                os.path.join(top_level_device_folder, child_safe_name + ".xml"),
                recursive=True,
                original_name=child_device.get_name(),
                parent_name=top_level_device.get_name(),
            )


def import_communication(communication_obj, device_folder):
    communication_folder = os.path.join(device_folder, "communication")
    if not os.path.exists(communication_folder):
        return

    remove_tracked_communication_devices(communication_obj)

    # for top level folders inside the communication folder, do a native import on the corresponding communication device
    for name in os.listdir(communication_folder):
        full_path = os.path.join(communication_folder, name)
        if not os.path.isdir(full_path):
            continue

        original_name = resolve_original_name(communication_folder, name, default=name)
        top_level_device = _find_top_level_device(communication_obj, original_name, safe_name=name)
        for child_name in os.listdir(full_path):
            _, ext = os.path.splitext(child_name)
            if ext == ".xml":
                top_level_device.import_native(os.path.join(full_path, child_name))


def remove_tracked_communication_devices(communication_obj):
    if no_export_folder_exists(communication_obj):
        return

    # remove all children from top level devices
    for top_level_device in communication_obj.get_children():
        for child in top_level_device.get_children():
            child.remove()


def _find_top_level_device(communication_obj, export_name, safe_name=None):
    err = "Cannot find communication device with name " + export_name
    try:
        return first_of_type_or_error(communication_obj.find(export_name), ObjectType.DEVICE, err)
    except ValueError:
        target_safe = safe_name or safe_filename(export_name)
        for candidate in communication_obj.get_children():
            if get_object_type(candidate) != ObjectType.DEVICE:
                continue
            if safe_filename(candidate.get_name()) == target_safe:
                return candidate
        raise ValueError(err)
