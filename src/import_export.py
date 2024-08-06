# REMEMBER: this is python 2.7
import os
import re

from object_type import ObjectType, get_object_type
from util import *

IMPLEMENTATION_DELIMITER_SPLIT = "// --- BEGIN IMPLEMENTATION ---"
IMPLEMENTATION_DELIMITER_INSERT = "\n" + IMPLEMENTATION_DELIMITER_SPLIT + "\n\n"


def write_st(obj, f):
    f.write(obj.textual_declaration.text)
    f.write(IMPLEMENTATION_DELIMITER_INSERT)
    f.write(obj.textual_implementation.text)


def write_st_decl_only(obj, f):
    f.write(obj.textual_declaration.text)


def import_st(f, obj):
    f.seek(0)
    content = str(f.read())
    declaration, implementation = content.split(IMPLEMENTATION_DELIMITER_SPLIT)
    obj.textual_declaration.replace(declaration.strip() + "\n")
    obj.textual_implementation.replace(implementation.strip() + "\n")


def import_st_decl_only(f, obj):
    f.seek(0)
    content = str(f.read())
    obj.textual_declaration.replace(content.strip() + "\n")


def write_native(obj, path, recursive=False):
    obj.export_native(path, recursive=recursive)

    # using regex instead of an xml parser because it is much quicker (sorry)
    with open(path, "r+") as f:
        lines = f.read()
        # uuid_replaced = re.sub(
        #     r'(^.+<Single Name="(?:EventPOUGuid|ParentSVNodeGuid|ParentGuid|LmGuid|LmStructTypeGuid|LmArrayTypeGuid|IoConfigGlobalsGuid|IoConfigGLobalsMappingGuid|IoConfigVarConfigGuid|IoConfigErrorPouGuid)".+?>).+(<\/Single>$)',
        #     r"\g<1>00000000-0000-0000-0000-000000000000\g<2>",
        #     lines,
        #     flags=re.MULTILINE,
        # )

        # match any tags with Timestamp or Id and replace their contents with "0"
        timestamp_replaced = re.sub(
            r'(^.+<Single Name="(?:Timestamp|Id)" Type="long">).+(<\/Single>$)',
            r"\g<1>0\g<2>",
            lines,
            flags=re.MULTILINE,
        )
        f.seek(0)
        f.write(timestamp_replaced)
        f.truncate()


def read_native(f, obj):
    obj.import_native(f)


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
            write_st(child_obj, f)
    else:
        export_native(child_obj, parent_obj, parent_folder_path, export_child_fn)

    for c in child_obj.get_children():
        export_child_fn(c, child_obj, parent_folder_path)


def import_pou_st(child, dir_path, dir_parent_obj, import_dir_fn):
    filename, _ = os.path.splitext(child)
    pou_obj = dir_parent_obj.create_pou(filename)
    with open(os.path.join(dir_path, child), "r") as f:
        import_st(f, pou_obj)


def export_gvl(child_obj, parent_obj, parent_folder_path, export_child_fn):
    """
    Exports native xml and structured text representation.
    This is because we need to support EVL and NVL as well, using this function.
    """
    write_native(child_obj, os.path.join(parent_folder_path, child_obj.get_name() + ".gvl.xml"), recursive=False)
    with open(os.path.join(parent_folder_path, child_obj.get_name() + ".gvl.st"), "w") as f:
        write_st_decl_only(child_obj, f)


def import_gvl(child, dir_path, dir_parent_obj, import_dir_fn):
    """
    Import the native xml and then overwrite the textual definition with the structured text.
    """
    name, ext = os.path.splitext(child)

    if ".gvl" not in name:
        raise ValueError(".gvl not in file name!")

    name = name.replace(".gvl", "")

    if ext != ".st":
        raise ValueError("Expected GVL st file!")

    gvl_xml_path = os.path.join(dir_path, name + ".gvl.xml")
    if not os.path.exists(gvl_xml_path):
        raise ValueError("Expected GVL xml file at " + gvl_xml_path)

    import_native(gvl_xml_path, dir_path, dir_parent_obj, import_dir_fn)
    with open(os.path.join(dir_path, child), "r") as f:
        imported_obj = first_of_type_or_error(
            dir_parent_obj.find(name), ObjectType.GVL, name + " GVL should have been created, but cannot be found"
        )
        import_st_decl_only(f, imported_obj)


def export_native(child_obj, parent_obj, parent_folder_path, export_child_fn):
    write_native(child_obj, os.path.join(parent_folder_path, child_obj.get_name() + ".xml"), recursive=False)


def export_native_recursive(child_obj, parent_obj, parent_folder_path, export_child_fn):
    write_native(child_obj, os.path.join(parent_folder_path, child_obj.get_name() + ".xml"), recursive=True)


def import_native(child, dir_path, dir_parent_obj, import_dir_fn):
    read_native(os.path.join(dir_path, child), dir_parent_obj)


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
            write_st(child_obj, f)
    else:
        write_native(
            child_obj,
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
        import_st(f, method_obj)


def export_sub_pou(child_obj, parent_obj, parent_folder_path, export_child_fn):
    write_native(
        child_obj,
        os.path.join(parent_folder_path, parent_obj.get_name() + "." + child_obj.get_name() + ".xml"),
        recursive=True,
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
    ObjectType.GVL: export_gvl,  # EVL, NVL are "special types" of GVL which show up with the same UUID
    ObjectType.EVC: export_native,
    ObjectType.VISUALISATION: export_native,
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
