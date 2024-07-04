import os

from object_type import ObjectType
from util import *


def export_communication(communication_obj, device_folder):
    """
    Export communication is hardcoded to create folders for the top level devices inside the communication object, and
    then do a native recursive export for any devices under those top level devices.
    """
    if first_of_type_or_none(communication_obj.find("_NO_EXPORT"), ObjectType.FOLDER) is not None:
        return

    communication_folder = os.path.join(device_folder, "communication")
    os.mkdir(communication_folder)

    for top_level_device in communication_obj.get_children():
        top_level_device_folder = os.path.join(communication_folder, top_level_device.get_name())
        os.mkdir(top_level_device_folder)
        for child_device in top_level_device.get_children():
            child_device.export_native(
                os.path.join(top_level_device_folder, child_device.get_name() + ".xml"), recursive=True
            )


def import_communication(communication_obj, device_folder):
    communication_folder = os.path.join(device_folder, "communication")
    if not os.path.exists(communication_folder):
        return

    # remove all children from top level devices
    for top_level_device in communication_obj.get_children():
        for child in top_level_device.get_children():
            child.remove()

    # for top level folders inside the communcation folder, do a native import on the corresponding communication device
    for name in os.listdir(communication_folder):
        full_path = os.path.join(communication_folder, name)
        if not os.path.isdir(full_path):
            continue

        top_level_device = first_of_type_or_error(
            communication_obj.find(name), ObjectType.DEVICE, "Cannot find communication device with name " + name
        )
        for child_name in os.listdir(full_path):
            _, ext = os.path.splitext(child_name)
            if ext == ".xml":
                top_level_device.import_native(os.path.join(full_path, child_name))
