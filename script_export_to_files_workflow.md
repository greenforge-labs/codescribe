# Script Export-to-Files Workflow

## Purpose
- Generate a file-system snapshot of every device, its application graph, and communication settings in the active ScriptEngine project.
- Guarantee that downstream tooling always starts from a clean, user-selected export directory that mirrors the project structure at export time.

## Architectural Components
- **ScriptEngine context (`scriptengine.projects.primary`)** – supplies the open project that drives every lookup.
- **Entrypoint helpers (`find_application`, `find_communication`, `get_device_entrypoints`, `get_src_folder`)** – locate the top-level objects and provide the default destination suggestion.
- **Import/export layer (`OBJECT_TYPE_TO_EXPORT_FUNCTION`, `export_communication`)** – maps object types to the correct serializer and knows how to persist communication artifacts.
- **Utility helpers (`print_python_version`, `assert_project_open`, `prompt_for_directory`)** – enforce that the integration runs inside a live, compatible environment and surface the Windows folder picker with a safe fallback.
- **Destination helpers (`prepare_export_destination`, `write_export_manifest`)** – make sure the selected path exists, delete only directories owned by CODESCRIBE, and persist a manifest for future cleanups.
- **Standard library (`os`, `shutil`, `json`)** – handles folder creation, recursive removal, and manifest serialization so exports stay deterministic.

## Core Workflow
1. **Environment verification**
   - `print_python_version()` logs the interpreter (Python 2.7 requirement).
   - `assert_project_open()` ensures ScriptEngine has an active project; the script halts otherwise.
2. **Destination selection and preparation**
   - `get_src_folder(...)` provides the default path, and `prompt_for_directory(...)` opens a `FolderBrowserDialog` seeded with that location. If the picker is unavailable (headless runs) the default is used automatically.
   - Canceling the picker returns `None`, prompting an early exit before any filesystem changes occur.
   - `prepare_export_destination(...)` validates the chosen path, creates it when missing, removes every device folder recorded in `.codescribe_export_manifest.json`, and also clears any device folders that are about to be recreated.
3. **Device iteration**
   - `get_device_entrypoints(...)` yields each device entrypoint object once; the script captures both the COM object and its name so filenames stay stable even on Python 2.
   - A dedicated directory (`<export>/<device_name>/`) is created per device with `os.makedirs` to avoid race conditions when exporting to empty or remote folders.
4. **Application export**
   - `find_application(device_obj)` returns the application node for the device.
   - An `application` subfolder stores exported components.
   - Each child of the application triggers `export_child`, which passes control to the appropriate serializer via `OBJECT_TYPE_TO_EXPORT_FUNCTION`. The serializer receives the same `export_child` callback so it can recurse into nested structures.
5. **Communication export**
   - `find_communication(device_obj)` retrieves the communication configuration.
   - `export_communication(...)` writes those assets directly under the device folder alongside the `application` directory.
6. **Completion**
   - After all devices are processed, `write_export_manifest(...)` captures the list of device directories that were created so the next run can clean them safely.
   - Success is reported with `print("Done!")`; exceptions propagate so upstream automation can react.

## Recursive Child Export (`export_child`)
- Identifies the object's type with `get_object_type(child_obj)`.
- Looks up the matching export function from `OBJECT_TYPE_TO_EXPORT_FUNCTION`.
- When found, invokes it with the child, its parent, the target folder, and the same `export_child` callback so exporters can continue descending the tree.
- If a type is missing from the map, the child is silently skipped, preventing crashes but signaling the need to extend the mapping for new object types.

```python
def export_child(child, parent, folder):
    obj_type = get_object_type(child)
    handler = OBJECT_TYPE_TO_EXPORT_FUNCTION.get(obj_type)
    if handler:
        handler(child, parent, folder, export_child)  # depth-first recursion
```

## Error Handling & Idempotency
- The top-level `try/except` logs any exception and re-raises it, ensuring both console visibility and proper failure semantics for calling processes. Canceling the folder picker raises `SystemExit`, which bypasses the trailing `Done!` message.
- Manifest-driven cleanup guarantees idempotent exports: only the device folders created by the previous run are deleted, so outputs always reflect the latest project state without risking unrelated files in the same destination.

## Extension Considerations
- **New object types** – register a serializer in `OBJECT_TYPE_TO_EXPORT_FUNCTION`; it will automatically participate in the recursive walk.
- **Partial exports** – adapt the device loop or pass filters to `get_device_entrypoints`.
- **Safety checks** – hook into `prompt_for_directory` or `prepare_export_destination` if you need additional validation before deleting user-selected content.
