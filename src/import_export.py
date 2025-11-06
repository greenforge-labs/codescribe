# REMEMBER: this is python 2.7
import os
import re

from object_type import ObjectType, get_object_type
from util import (
    first_of_type_or_error,
    get_original_entry,
    register_directory,
    register_original_name,
    resolve_original_name,
    safe_filename,
    write_file,
)

IMPLEMENTATION_DELIMITER_SPLIT = "// --- BEGIN IMPLEMENTATION ---"
IMPLEMENTATION_DELIMITER_INSERT = "\n" + IMPLEMENTATION_DELIMITER_SPLIT + "\n\n"


def _render_st(obj):
    return obj.textual_declaration.text + IMPLEMENTATION_DELIMITER_INSERT + obj.textual_implementation.text


def _render_st_decl_only(obj):
    return obj.textual_declaration.text


def write_st(obj, f):
    f.write(_render_st(obj))


def write_st_decl_only(obj, f):
    f.write(_render_st_decl_only(obj))


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


def write_native(obj, path, recursive=False, original_name=None, parent_name=None):
    obj.export_native(path, recursive=recursive)

    # using regex instead of an xml parser because it is much quicker (sorry)
    with open(path, "r+") as f:
        lines = f.read()

        # XXX: Warning! Overwriting Id's broke visualisations
        # It's probably a bad idea to overwrite Id's and UUIDs, even if it is annoying to have them show up in the diff
        # Stick to just overwriting timestamps for now

        # uuid_replaced = re.sub(
        #     r'(^.+<Single Name="(?:EventPOUGuid|ParentSVNodeGuid|ParentGuid|LmGuid|LmStructTypeGuid|LmArrayTypeGuid|IoConfigGlobalsGuid|IoConfigGLobalsMappingGuid|IoConfigVarConfigGuid|IoConfigErrorPouGuid)".+?>).+(<\/Single>$)',
        #     r"\g<1>00000000-0000-0000-0000-000000000000\g<2>",
        #     lines,
        #     flags=re.MULTILINE,
        # )

        # match any tags with Timestamp or Id and replace their contents with "0"
        # timestamp_replaced = re.sub(
        #     r'(^.+<Single Name="(?:Timestamp|Id)" Type="long">).+(<\/Single>$)',
        #     r"\g<1>0\g<2>",
        #     lines,
        #     flags=re.MULTILINE,
        # )

        timestamp_replaced = re.sub(
            r'(^.+<Single Name="(?:Timestamp)" Type="long">).+(<\/Single>$)',
            r"\g<1>0\g<2>",
            lines,
            flags=re.MULTILINE,
        )

        f.seek(0)
        f.write(timestamp_replaced)
        f.truncate()

    register_original_name(
        os.path.dirname(path),
        os.path.basename(path),
        original_name or obj.get_name(),
        parent_name=parent_name,
        kind="file",
    )


def read_native(f, obj):
    obj.import_native(f)


def export_folder(child_obj, parent_obj, parent_folder_path, export_child_fn):
    safe_child_name = safe_filename(child_obj.get_name())
    child_obj_folder = os.path.join(parent_folder_path, safe_child_name)
    os.mkdir(child_obj_folder)
    register_directory(parent_folder_path, safe_child_name, child_obj.get_name())
    for c in child_obj.get_children():
        export_child_fn(c, child_obj, child_obj_folder)


def import_folder(child, dir_path, dir_parent_obj, import_dir_fn):
    folder_name = resolve_original_name(dir_path, child, default=child)
    dir_parent_obj.create_folder(folder_name)
    folder_obj = first_of_type_or_error(
        dir_parent_obj.find(folder_name),
        ObjectType.FOLDER,
        "Folder of name " + folder_name + " should have been created, but cannot be found",
    )
    import_dir_fn(os.path.join(dir_path, child), folder_obj)


def export_pou(child_obj, parent_obj, parent_folder_path, export_child_fn):
    if child_obj.has_textual_implementation:
        safe_child_name = safe_filename(child_obj.get_name())
        out_path = os.path.join(parent_folder_path, safe_child_name + ".st")
        write_file(
            out_path,
            _render_st(child_obj),
            original_name=child_obj.get_name(),
            parent_name=parent_obj.get_name(),
        )
    else:
        export_native(child_obj, parent_obj, parent_folder_path, export_child_fn)

    for c in child_obj.get_children():
        export_child_fn(c, child_obj, parent_folder_path)


def import_pou_st(child, dir_path, dir_parent_obj, import_dir_fn):
    filename, _ = os.path.splitext(child)
    entry = get_original_entry(dir_path, child)
    pou_name = entry.get("name") if entry and entry.get("name") else filename
    pou_obj = dir_parent_obj.create_pou(pou_name)
    with open(os.path.join(dir_path, child), "r") as f:
        import_st(f, pou_obj)


def export_gvl(child_obj, parent_obj, parent_folder_path, export_child_fn):
    """
    Exports native xml and structured text representation.
    This is because we need to support EVL and NVL as well, using this function.
    """
    base_name = safe_filename(child_obj.get_name())
    write_native(
        child_obj,
        os.path.join(parent_folder_path, base_name + ".gvl.xml"),
        recursive=False,
        original_name=child_obj.get_name(),
        parent_name=parent_obj.get_name(),
    )
    write_file(
        os.path.join(parent_folder_path, base_name + ".gvl.st"),
        _render_st_decl_only(child_obj),
        original_name=child_obj.get_name(),
        parent_name=parent_obj.get_name(),
    )


def import_gvl(child, dir_path, dir_parent_obj, import_dir_fn):
    """
    Import the native xml and then overwrite the textual definition with the structured text.
    """
    name_safe, ext = os.path.splitext(child)

    if ".gvl" not in name_safe:
        raise ValueError(".gvl not in file name!")

    base_safe = name_safe.replace(".gvl", "")
    entry = get_original_entry(dir_path, child)
    object_name = entry.get("name") if entry and entry.get("name") else base_safe

    if ext != ".st":
        raise ValueError("Expected GVL st file!")

    gvl_xml_path = os.path.join(dir_path, base_safe + ".gvl.xml")
    if not os.path.exists(gvl_xml_path):
        raise ValueError("Expected GVL xml file at " + gvl_xml_path)

    import_native(gvl_xml_path, dir_path, dir_parent_obj, import_dir_fn)
    with open(os.path.join(dir_path, child), "r") as f:
        imported_obj = first_of_type_or_error(
            dir_parent_obj.find(object_name),
            ObjectType.GVL,
            object_name + " GVL should have been created, but cannot be found",
        )
        import_st_decl_only(f, imported_obj)


def export_native(child_obj, parent_obj, parent_folder_path, export_child_fn):
    safe_child_name = safe_filename(child_obj.get_name())
    write_native(
        child_obj,
        os.path.join(parent_folder_path, safe_child_name + ".xml"),
        recursive=False,
        original_name=child_obj.get_name(),
        parent_name=parent_obj.get_name(),
    )


def export_native_recursive(child_obj, parent_obj, parent_folder_path, export_child_fn):
    safe_child_name = safe_filename(child_obj.get_name())
    write_native(
        child_obj,
        os.path.join(parent_folder_path, safe_child_name + ".xml"),
        recursive=True,
        original_name=child_obj.get_name(),
        parent_name=parent_obj.get_name(),
    )


def import_native(child, dir_path, dir_parent_obj, import_dir_fn):
    read_native(os.path.join(dir_path, child), dir_parent_obj)


def export_dut(child_obj, parent_obj, parent_folder_path, export_child_fn):
    write_file(
        os.path.join(parent_folder_path, safe_filename(child_obj.get_name()) + ".st"),
        child_obj.textual_declaration.text,
        original_name=child_obj.get_name(),
        parent_name=parent_obj.get_name(),
    )


def import_dut(child, dir_path, dir_parent_obj, import_dir_fn):
    filename, _ = os.path.splitext(child)
    entry = get_original_entry(dir_path, child)
    dut_name = entry.get("name") if entry and entry.get("name") else filename
    dut_obj = dir_parent_obj.create_dut(dut_name)
    with open(os.path.join(dir_path, child), "r") as f:
        f.seek(0)
        dut_obj.textual_declaration.replace(str(f.read()))


def export_method(child_obj, parent_obj, parent_folder_path, export_child_fn):
    if child_obj.has_textual_implementation:
        parent_name = safe_filename(parent_obj.get_name())
        method_name = safe_filename(child_obj.get_name())
        out_path = os.path.join(parent_folder_path, parent_name + "." + method_name + ".st")
        write_file(
            out_path,
            _render_st(child_obj),
            original_name=child_obj.get_name(),
            parent_name=parent_obj.get_name(),
        )
    else:
        parent_name = safe_filename(parent_obj.get_name())
        method_name = safe_filename(child_obj.get_name())
        write_native(
            child_obj,
            os.path.join(parent_folder_path, parent_name + "." + method_name + ".xml"),
            recursive=False,
            original_name=child_obj.get_name(),
            parent_name=parent_obj.get_name(),
        )


def import_method_st(child, dir_path, dir_parent_obj, import_dir_fn):
    full_path = os.path.join(dir_path, child)
    filename, _ = os.path.splitext(child)
    parts = filename.split(".")
    parent_safe = parts[0]
    method_safe = parts[1] if len(parts) > 1 else parts[0]
    entry = get_original_entry(dir_path, child)
    parent_name = entry.get("parent") if entry and entry.get("parent") else parent_safe
    method_name = entry.get("name") if entry and entry.get("name") else method_safe
    parent_obj = first_of_type_or_error(
        dir_parent_obj.find(parent_name),
        ObjectType.POU,
        parent_name + " should have been created, but cannot be found",
    )

    method_obj = parent_obj.create_method(method_name)
    with open(full_path, "r") as f:
        import_st(f, method_obj)


def export_sub_pou(child_obj, parent_obj, parent_folder_path, export_child_fn):
    parent_name = safe_filename(parent_obj.get_name())
    child_name = safe_filename(child_obj.get_name())
    write_native(
        child_obj,
        os.path.join(parent_folder_path, parent_name + "." + child_name + ".xml"),
        recursive=True,
    )


def import_sub_pou(child, dir_path, dir_parent_obj, import_dir_fn):
    full_path = os.path.join(dir_path, child)
    filename, _ = os.path.splitext(child)
    parts = filename.split(".")
    parent_safe = parts[0]
    entry = get_original_entry(dir_path, child)
    parent_name = entry.get("parent") if entry and entry.get("parent") else parent_safe
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


def export_child(child_obj, parent_obj, parent_folder_path):
    child_obj_type = get_object_type(child_obj)
    export_fn = OBJECT_TYPE_TO_EXPORT_FUNCTION.get(child_obj_type)
    if export_fn is not None:
        export_fn(child_obj, parent_obj, parent_folder_path, export_child)


def remove_tracked_objects(obj_list):
    for obj in obj_list:
        if get_object_type(obj) in OBJECT_TYPE_TO_EXPORT_FUNCTION:
            print("Removing " + obj.get_name())
            obj.remove()
