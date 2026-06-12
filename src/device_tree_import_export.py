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
    # import_native always pastes the archived object as a child of the receiving node,
    # it never replaces in place. So the only way to update a tracked device is to
    # remove it and import the xml into the PLC device. Devices fixed by the device
    # package (e.g. Local_IO and HMI on IFM hardware) cannot be removed; their
    # configuration is carried by the project template, like the fixed top-level
    # communication devices, so they are skipped with a message.
    devices_folder = os.path.join(device_folder, DEVICE_TREE_FOLDER_NAME)
    if not os.path.exists(devices_folder):
        return

    if no_export_device_tree(device_obj):
        return

    for child_name in sorted(os.listdir(devices_folder)):
        name, ext = os.path.splitext(child_name)
        if ext != ".xml":
            continue

        device_node = _find_device_tree_sibling(device_obj, name)
        if device_node is not None:
            try:
                device_node.remove()
            except Exception:
                print("Cannot remove fixed device " + name + ", skipping its import (the template carries its configuration)")
                continue
        # Missing device (fresh project from a template) and removed device both
        # import the same way: the xml recreates the device under the PLC device.
        read_native(os.path.join(devices_folder, child_name), device_obj)


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
        try:
            device_node.remove()
        except Exception:
            # Fixed package devices stay in the template; import skips them too.
            print("Cannot remove fixed device " + name + ", leaving it in the template")
