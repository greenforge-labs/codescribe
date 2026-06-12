# REMEMBER: this is python 2.7
import os

from communication_import_export import NO_EXPORT_FOLDER_NAME
from import_export import read_native, write_native
from object_type import ObjectType, get_object_type
from util import *

DEVICE_TREE_FOLDER_NAME = "devices"


def no_export_device_tree(device_obj):
    # Only a direct FOLDER child of the PLC device disables this export. A _NO_EXPORT
    # folder nested under Communication keeps disabling the Communication export alone.
    for child in device_obj.get_children():
        if get_object_type(child) == ObjectType.FOLDER and child.get_name() == NO_EXPORT_FOLDER_NAME:
            return True
    return False


def _find_device_tree_sibling(device_obj, name):
    # Match the export scope: only direct DEVICE children of the PLC device.
    for child in device_obj.get_children():
        if get_object_type(child) == ObjectType.DEVICE and child.get_name() == name:
            return child
    return None


def export_device_tree_siblings(device_obj, device_folder, application, communication):
    """
    Export device-tree devices that sit next to Plc Logic as direct children of the PLC device
    (Ethernet, Modbus, fieldbus). Each one is written as a single native recursive xml file under
    <device_folder>/devices. Returns True when at least one device was exported.
    """
    if no_export_device_tree(device_obj):
        return False

    siblings = []
    for child in device_obj.get_children():
        if get_object_type(child) != ObjectType.DEVICE:
            continue
        if communication is not None and child == communication:
            continue
        # Skip children that carry an Application anywhere in their subtree, not just the
        # Application passed in. In compound safety projects (e.g. the IFM CR711s) the
        # SafetyPLC and StandardPLC are DEVICE children that each carry their own
        # Application and are already exported through their own device entrypoint.
        if first_or_none(child.find("Application", recursive=True)) is not None:
            continue
        siblings.append(child)

    if len(siblings) < 1:
        return False

    devices_folder = os.path.join(device_folder, DEVICE_TREE_FOLDER_NAME)
    os.mkdir(devices_folder)

    for child in siblings:
        write_native(child, os.path.join(devices_folder, child.get_name() + ".xml"), recursive=True)

    return True


def import_device_tree_siblings(device_obj, device_folder):
    devices_folder = os.path.join(device_folder, DEVICE_TREE_FOLDER_NAME)
    if not os.path.exists(devices_folder):
        return

    if no_export_device_tree(device_obj):
        return

    remove_tracked_device_tree_devices(device_obj, device_folder)

    for child_name in sorted(os.listdir(devices_folder)):
        name, ext = os.path.splitext(child_name)
        if ext != ".xml":
            continue

        device_node = _find_device_tree_sibling(device_obj, name)
        if device_node is None:
            raise ValueError("Cannot find device-tree device with name " + name)
        read_native(os.path.join(devices_folder, child_name), device_node)


def remove_tracked_device_tree_devices(device_obj, device_folder):
    devices_folder = os.path.join(device_folder, DEVICE_TREE_FOLDER_NAME)
    if not os.path.exists(devices_folder):
        return

    if no_export_device_tree(device_obj):
        return

    for child_name in os.listdir(devices_folder):
        name, ext = os.path.splitext(child_name)
        if ext != ".xml":
            continue

        device_node = _find_device_tree_sibling(device_obj, name)
        if device_node is None:
            continue
        # snapshot the children: removing while iterating the live collection skips entries
        for child in list(device_node.get_children()):
            child.remove()
