# REMEMBER: this is python 2.7
import os

from object_type import ObjectType, get_object_type
from util import *

IMPLEMENTATION_DELIMITER_SPLIT = "// --- BEGIN IMPLEMENTATION ---"
IMPLEMENTATION_DELIMITER_INSERT = "\n" + IMPLEMENTATION_DELIMITER_SPLIT + "\n\n"


def write_st_with_impl(obj, f):
    f.write(obj.textual_declaration.text)
    f.write(IMPLEMENTATION_DELIMITER_INSERT)
    f.write(obj.textual_implementation.text)


def import_st_with_impl(f, obj):
    f.seek(0)
    content = str(f.read())
    declaration, implementation = content.split(IMPLEMENTATION_DELIMITER_SPLIT)
    obj.textual_declaration.replace(declaration.strip() + "\n")
    obj.textual_implementation.replace(implementation.strip() + "\n")


def export_folder(child_obj, parent_obj, parent_folder_path, export_child_fn):
    child_obj_folder = os.path.join(parent_folder_path, child_obj.get_name())
    os.mkdir(child_obj_folder)
    for c in child_obj.get_children():
        export_child_fn(c, child_obj, child_obj_folder)


def import_folder(child, dir_path, dir_parent_obj, import_dir_fn):
    dir_parent_obj.create_folder(child)
    folder_obj = first_of_type_or_error(
        dir_parent_obj.find(child),
        ObjectType.FOLDER,
        "Folder of name " + child + " should have been created, but cannot be found",
    )
    import_dir_fn(os.path.join(dir_path, child), folder_obj)


def export_pou(child_obj, parent_obj, parent_folder_path, export_child_fn):
    if child_obj.has_textual_implementation:
        with open(os.path.join(parent_folder_path, child_obj.get_name() + ".st"), "w") as f:
            write_st_with_impl(child_obj, f)
    else:
        export_native(child_obj, parent_obj, parent_folder_path, export_child_fn)

    for c in child_obj.get_children():
        export_child_fn(c, child_obj, parent_folder_path)


def import_pou_st(child, dir_path, dir_parent_obj, import_dir_fn):
    filename, _ = os.path.splitext(child)
    pou_obj = dir_parent_obj.create_pou(filename)
    with open(os.path.join(dir_path, child), "r") as f:
        import_st_with_impl(f, pou_obj)


def export_native(child_obj, parent_obj, parent_folder_path, export_child_fn):
    child_obj.export_native(os.path.join(parent_folder_path, child_obj.get_name() + ".xml"), recursive=False)


def export_native_recursive(child_obj, parent_obj, parent_folder_path, export_child_fn):
    child_obj.export_native(os.path.join(parent_folder_path, child_obj.get_name() + ".xml"), recursive=True)


def import_native(child, dir_path, dir_parent_obj, import_dir_fn):
    dir_parent_obj.import_native(os.path.join(dir_path, child))


def export_dut(child_obj, parent_obj, parent_folder_path, export_child_fn):
    with open(os.path.join(parent_folder_path, child_obj.get_name() + ".st"), "w") as f:
        f.write(child_obj.textual_declaration.text)


def import_dut(child, dir_path, dir_parent_obj, import_dir_fn):
    filename, _ = os.path.splitext(child)
    dut_obj = dir_parent_obj.create_dut(filename)
    with open(os.path.join(dir_path, child), "r") as f:
        f.seek(0)
        dut_obj.textual_declaration.replace(str(f.read()))


def export_method(child_obj, parent_obj, parent_folder_path, export_child_fn):
    if child_obj.has_textual_implementation:
        with open(
            os.path.join(parent_folder_path, parent_obj.get_name() + "." + child_obj.get_name() + ".st"), "w"
        ) as f:
            write_st_with_impl(child_obj, f)
    else:
        child_obj.export_native(
            os.path.join(parent_folder_path, parent_obj.get_name() + "." + child_obj.get_name() + ".xml"),
            recursive=False,
        )


def import_method_st(child, dir_path, dir_parent_obj, import_dir_fn):
    full_path = os.path.join(dir_path, child)
    filename, _ = os.path.splitext(child)
    parent_name, method_name = filename.split(".")
    parent_obj = first_of_type_or_error(
        dir_parent_obj.find(parent_name),
        ObjectType.POU,
        parent_name + " should have been created, but cannot be found",
    )

    method_obj = parent_obj.create_method(method_name)
    with open(full_path, "r") as f:
        import_st_with_impl(f, method_obj)


def export_sub_pou(child_obj, parent_obj, parent_folder_path, export_child_fn):
    child_obj.export_native(
        os.path.join(parent_folder_path, parent_obj.get_name() + "." + child_obj.get_name() + ".xml"), recursive=True
    )


def import_sub_pou(child, dir_path, dir_parent_obj, import_dir_fn):
    full_path = os.path.join(dir_path, child)
    filename, _ = os.path.splitext(child)
    parent_name = filename.split(".")[0]
    parent_obj = first_of_type_or_error(
        dir_parent_obj.find(parent_name),
        ObjectType.POU,
        parent_name + " should have been created, but cannot be found",
    )

    parent_obj.import_native(full_path)


OBJECT_TYPE_TO_EXPORT_FUNCTION = {
    ObjectType.FOLDER: export_folder,
    ObjectType.POU: export_pou,
    ObjectType.EVL: export_native,
    ObjectType.EVC: export_native,
    ObjectType.TASK_CONFIGURATION: export_native_recursive,
    ObjectType.DUT: export_dut,
    ObjectType.METHOD: export_method,
    ObjectType.PROPERTY: export_sub_pou,
    ObjectType.ACTION: export_sub_pou,
    ObjectType.TRANSITION: export_sub_pou,
}


def remove_tracked_objects(obj_list):
    for obj in obj_list:
        if get_object_type(obj) in OBJECT_TYPE_TO_EXPORT_FUNCTION:
            print("Removing " + obj.get_name())
            obj.remove()
