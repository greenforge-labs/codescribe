# REMEMBER: this is python 2.7
import os
import re

import scriptengine  # type: ignore

from object_type import ObjectType, get_object_type
from util import *

# unicode literals so they can be written to / split out of the UTF-8 text streams below
IMPLEMENTATION_DELIMITER_SPLIT = u"// --- BEGIN IMPLEMENTATION ---"
IMPLEMENTATION_DELIMITER_INSERT = u"\n" + IMPLEMENTATION_DELIMITER_SPLIT + u"\n\n"


def write_st(obj, f):
    f.write(obj.textual_declaration.text)
    f.write(IMPLEMENTATION_DELIMITER_INSERT)
    f.write(obj.textual_implementation.text)


def write_st_decl_only(obj, f):
    f.write(obj.textual_declaration.text)


def import_st(f, obj):
    f.seek(0)
    content = f.read()
    declaration, implementation = content.split(IMPLEMENTATION_DELIMITER_SPLIT)
    obj.textual_declaration.replace(declaration.strip() + "\n")
    obj.textual_implementation.replace(implementation.strip() + "\n")


def import_st_decl_only(f, obj):
    f.seek(0)
    content = f.read()
    obj.textual_declaration.replace(content.strip() + "\n")


def write_native(obj, path, recursive=False):
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
        with open_utf8(os.path.join(parent_folder_path, child_obj.get_name() + ".st"), "w") as f:
            write_st(child_obj, f)
    else:
        export_native(child_obj, parent_obj, parent_folder_path, export_child_fn)

    for c in child_obj.get_children():
        export_child_fn(c, child_obj, parent_folder_path)


def import_pou_st(child, dir_path, dir_parent_obj, import_dir_fn):
    filename, _ = os.path.splitext(child)
    pou_obj = dir_parent_obj.create_pou(filename)
    with open_utf8(os.path.join(dir_path, child), "r") as f:
        import_st(f, pou_obj)


def export_gvl(child_obj, parent_obj, parent_folder_path, export_child_fn):
    """
    Exports native xml and structured text representation.
    This is because we need to support EVL and NVL as well, using this function.
    """
    write_native(child_obj, os.path.join(parent_folder_path, child_obj.get_name() + ".gvl.xml"), recursive=False)
    with open_utf8(os.path.join(parent_folder_path, child_obj.get_name() + ".gvl.st"), "w") as f:
        write_st_decl_only(child_obj, f)


def find_gvl_or_error(parent_obj, name, err):
    # Persistent variable lists carry their own GUID, so a freshly imported GVL can be
    # either type.
    for gvl_type in (ObjectType.GVL, ObjectType.GVL_PERSISTENT):
        found = first_of_type_or_none(parent_obj.find(name), gvl_type)
        if found is not None:
            return found
    raise ValueError(err)


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
    if os.path.exists(gvl_xml_path):
        import_native(gvl_xml_path, dir_path, dir_parent_obj, import_dir_fn)
        imported_obj = find_gvl_or_error(
            dir_parent_obj, name, name + " GVL should have been created, but cannot be found"
        )
    else:
        imported_obj = dir_parent_obj.create_gvl(name)

    with open_utf8(os.path.join(dir_path, child), "r") as f:
        import_st_decl_only(f, imported_obj)


def export_native(child_obj, parent_obj, parent_folder_path, export_child_fn):
    write_native(child_obj, os.path.join(parent_folder_path, child_obj.get_name() + ".xml"), recursive=False)


def export_visualisation(child_obj, parent_obj, parent_folder_path, export_child_fn):
    # Visualisations regularly share a name with a POU (a Main program and a Main
    # visualisation, for example), which would collide on Main.xml.
    write_native(child_obj, os.path.join(parent_folder_path, child_obj.get_name() + ".vis.xml"), recursive=False)


def export_native_recursive(child_obj, parent_obj, parent_folder_path, export_child_fn):
    write_native(child_obj, os.path.join(parent_folder_path, child_obj.get_name() + ".xml"), recursive=True)


def import_native(child, dir_path, dir_parent_obj, import_dir_fn):
    read_native(os.path.join(dir_path, child), dir_parent_obj)


def export_dut(child_obj, parent_obj, parent_folder_path, export_child_fn):
    with open_utf8(os.path.join(parent_folder_path, child_obj.get_name() + ".st"), "w") as f:
        f.write(child_obj.textual_declaration.text)


def import_dut(child, dir_path, dir_parent_obj, import_dir_fn):
    filename, _ = os.path.splitext(child)
    dut_obj = dir_parent_obj.create_dut(filename)
    with open_utf8(os.path.join(dir_path, child), "r") as f:
        f.seek(0)
        # Normalize trailing whitespace the same way import_st does, so that
        # export -> import -> export round-trips are byte-identical.
        dut_obj.textual_declaration.replace(f.read().strip() + u"\n")


def export_method(child_obj, parent_obj, parent_folder_path, export_child_fn):
    if child_obj.has_textual_implementation:
        with open_utf8(
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
    with open_utf8(full_path, "r") as f:
        import_st(f, method_obj)


def _export_member_st_or_xml(child_obj, parent_obj, parent_folder_path, st_suffix):
    # Actions and Transitions have no textual declaration - the on-disk format is the
    # implementation text alone, with the kind encoded in the filename (.action.st / .transition.st)
    # so import dispatch is deterministic.
    base = os.path.join(parent_folder_path, parent_obj.get_name() + "." + child_obj.get_name())
    if child_obj.has_textual_implementation:
        with open_utf8(base + st_suffix + ".st", "w") as f:
            f.write(child_obj.textual_implementation.text)
    else:
        write_native(child_obj, base + ".xml", recursive=False)


def export_action(child_obj, parent_obj, parent_folder_path, export_child_fn):
    _export_member_st_or_xml(child_obj, parent_obj, parent_folder_path, ".action")


def export_transition(child_obj, parent_obj, parent_folder_path, export_child_fn):
    _export_member_st_or_xml(child_obj, parent_obj, parent_folder_path, ".transition")


def _import_member_st(child, dir_path, dir_parent_obj, st_suffix, create_fn):
    full_path = os.path.join(dir_path, child)
    filename, _ = os.path.splitext(child)
    filename = filename[: -len(st_suffix)]
    parent_name, child_name = filename.split(".")
    parent_obj = first_of_type_or_error(
        dir_parent_obj.find(parent_name),
        ObjectType.POU,
        parent_name + " should have been created, but cannot be found",
    )

    new_obj = create_fn(parent_obj, child_name)
    with open_utf8(full_path, "r") as f:
        new_obj.textual_implementation.replace(f.read().strip() + u"\n")


def import_action_st(child, dir_path, dir_parent_obj, import_dir_fn):
    # Pass the ST language explicitly: unlike methods, actions have no declaration line
    # for CODESYS to infer the language from.
    _import_member_st(
        child,
        dir_path,
        dir_parent_obj,
        ".action",
        lambda parent, name: parent.create_action(name, scriptengine.ImplementationLanguages.st),
    )


def import_transition_st(child, dir_path, dir_parent_obj, import_dir_fn):
    _import_member_st(
        child,
        dir_path,
        dir_parent_obj,
        ".transition",
        lambda parent, name: parent.create_transition(name, scriptengine.ImplementationLanguages.st),
    )


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
    ObjectType.GVL_PERSISTENT: export_gvl,  # persistent variable lists have their own GUID
    ObjectType.EVC: export_native,
    ObjectType.VISUALISATION: export_visualisation,
    ObjectType.TASK_CONFIGURATION: export_native_recursive,
    ObjectType.DUT: export_dut,
    ObjectType.METHOD: export_method,
    ObjectType.METHOD_NORET: export_method,  # methods without a return type have their own GUID
    ObjectType.PROPERTY: export_sub_pou,
    ObjectType.ACTION: export_action,
    ObjectType.TRANSITION: export_transition,
}


def remove_tracked_objects(obj_list):
    for obj in obj_list:
        if get_object_type(obj) in OBJECT_TYPE_TO_EXPORT_FUNCTION:
            print("Removing " + obj.get_name())
            obj.remove()
