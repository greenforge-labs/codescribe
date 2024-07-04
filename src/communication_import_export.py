import os

from object_type import ObjectType
from util import *


def export_communication(communication_obj, communication_folder_path):
    """
    Export communication is hardcoded to create folders for the top level devices inside the communication object, and
    then do a native recursive export for any devices under those top level devices.
    """
    if first_of_type_or_none(communication_obj.find("_NO_EXPORT"), ObjectType.FOLDER) is not None:
        return

    for top_level_device in communication_obj.get_children():
        top_level_device_folder = os.path.join(communication_folder_path, top_level_device.get_name())
        os.mkdir(top_level_device_folder)
        for child_device in top_level_device.get_children():
            child_device.export_native(
                os.path.join(top_level_device_folder, child_device.get_name() + ".xml"), recursive=True
            )
