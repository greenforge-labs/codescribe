# CODESYS Export Workflow Map

This guide cleans up and expands the quick notes on how the project exports artifacts from CODESYS. It highlights the primary scripts, explains the functions they expose, and anchors each description to the relevant line ranges so you can jump straight to the implementation when needed.

## Driver Pipeline — `src/script_export_to_files.py:16-47`
- `export_child` dispatches every application child through `OBJECT_TYPE_TO_EXPORT_FUNCTION`, guaranteeing that folders, POUs, DUTs, etc., are exported with the correct handler (`src/script_export_to_files.py:16-20`).
- The try block asserts the project is open, derives the `src` target with `get_src_folder`, wipes any existing export tree, and then iterates each device entrypoint to create `<device>/application` and `<device>/communication` scaffolding (`src/script_export_to_files.py:23-47`).
- Application children are exported depth-first via `export_child`, while communication objects are handed off to `export_communication`, keeping logic split between logic/program exports and network configuration exports.

## Entrypoint Helpers — `src/entrypoint.py:6-36`
- `get_src_folder` normalizes the export root to sit beside the `.project` file by reusing its directory and basename (`src/entrypoint.py:6-11`).
- `get_device_entrypoints` filters top-level project children so only populated `DEVICE` objects drive export runs, preventing empty hardware shells from cluttering the output (`src/entrypoint.py:14-23`).
- `find_application` and `find_communication` wrap `device_obj.find(...)` with `first_or_error`, surfacing immediate diagnostics when expected subtrees are missing, which keeps the main driver lean (`src/entrypoint.py:26-36`).

## Core Export Primitives — `src/import_export.py:12-240`
- Structured-text helpers (`write_text`, `write_st`, `write_st_decl_only`, `import_st`, `import_st_decl_only`) centralize the delimiter logic that splits declarations from implementations, so every textual export carries the `// --- BEGIN IMPLEMENTATION ---` boundary consistently (`src/import_export.py:12-38`).
- `write_native` performs native XML exports and then scrubs timestamp nodes to stabilize diffs; its counterpart `read_native` wraps `import_native` for symmetry (`src/import_export.py:40-80`).
- Directory/object exporters cover the various IEC 61131 object kinds:
  - `export_folder` recurses folder children (`src/import_export.py:82-87`).
  - `export_pou` chooses between textual `.st` snapshots and XML exports depending on whether an implementation exists, then recurses child objects (`src/import_export.py:99-108`).
  - `export_gvl` writes both `.gvl.xml` and `.gvl.st` files so EVL/NVL variations stay supported (`src/import_export.py:117-138`).
  - `export_dut`, `export_method`, and `export_sub_pou` handle declarations-only types, parent-qualified methods, and nested actions/properties/transitions respectively (`src/import_export.py:165-225`).
- `OBJECT_TYPE_TO_EXPORT_FUNCTION` is the routing table that connects each `ObjectType` enum to its exporter, and `remove_tracked_objects` inverts it to delete any tracked objects before re-importing (`src/import_export.py:228-247`).

## Communication Handlers — `src/communication_import_export.py:14-63`
- `export_communication` skips work if a `_NO_EXPORT` folder exists, then creates a `communication/` directory under each device export, mirrors every top-level communication device into its own subfolder, and uses `write_native(..., recursive=True)` so all nested devices/configurations land in the export tree (`src/communication_import_export.py:14-33`).
- `import_communication` (paired for completeness) removes previously exported children, then walks the filesystem to rehydrate communication devices via `import_native`, ensuring exports stay idempotent (`src/communication_import_export.py:34-54`).
- `remove_tracked_communication_devices` clears descendants unless `_NO_EXPORT` is present, so repeated runs always start from a clean slate (`src/communication_import_export.py:56-63`).

## Workflow at a Glance
- The driver script discovers devices (`entrypoint.py`), builds per-device folders, and hands each application child to `export_child`.
- `export_child` consults `OBJECT_TYPE_TO_EXPORT_FUNCTION`, which in turn calls the specialized exporters in `import_export.py`.
- Communication structures bypass the generic dispatcher and instead flow through `export_communication`, which writes native XML snapshots for hardware links.
- Combined, these layers keep textual logic, native XML artifacts, and communication definitions synchronized across exports without altering project code.
- Taken together, `src/script_export_to_files.py`, `src/entrypoint.py`, `src/import_export.py`, and `src/communication_import_export.py` span the entire export workflow: the toolbar script orchestrates, entrypoint helpers locate the right objects, import/export routines serialize each type, and communication handlers apply the hard-coded device export rules.

## Export Flow Snapshot
- `src/script_export_to_files.py:16-47` is the CODESYS-side script you execute; it asserts a project is open, builds the `<project>\src` directory beside the `.project`, and loops over each device yielded by `entrypoint.get_device_entrypoints`.
- For every device it walks the `Application` subtree, calling `export_child` on each object and `export_communication` for the communication branch so program logic and hardware links are exported together.
- `OBJECT_TYPE_TO_EXPORT_FUNCTION` (`src/import_export.py:228-240`) is the dispatcher that `export_child` consults, routing every supported `ObjectType` to its specialized exporter so serialization stays consistent.

## User-Selected Export Destination
- `prompt_for_directory` (`src/util.py:41-70`) opens a `System.Windows.Forms.FolderBrowserDialog`, seeds it with `get_src_folder(...)`, and falls back to the default path if the picker is unavailable. Canceling the dialog returns `None`, letting the export script bail out without touching the filesystem.
- `src/script_export_to_files.py:54-140` now calls the picker before any cleanup. When the user cancels, it prints “Export canceled” and exits before the final `Done!` message.
- `prepare_export_destination` and `write_export_manifest` (`src/script_export_to_files.py:28-75`) ensure the chosen path exists, enforce that it is a directory, and record every top-level device folder in `.codescribe_export_manifest.json`. The manifest powers selective cleanup so only the directories created by CODESCRIBE are removed on subsequent runs, keeping any unrelated files in the chosen folder intact.
- Device folders are created with `os.makedirs`, so pointing the export at an empty path (or one on a different drive) requires no manual preparation.
