# CODESYS Export Pipeline

This note walks through everything that happens after clicking **Export To Files** in the CODESYS toolbar until the plain-text files land on disk. Use it as a mental model for how CodeScribe pushes a binary CODESYS project into a Git-friendly folder structure.

## Launch Sequence

1. The toolbar button defined in `config.json` runs `src/script_export_to_files.py` inside the CODESYS ScriptEngine (Python 2.7).
2. The script verifies a project is open (`assert_project_open` in `src/util.py:104`) and collects the active project path/name via `_project_info()` (`src/script_export_to_files.py:19`).
3. `get_export_target()` (`src/entrypoint.py:23`) decides where files go:
   - `sys.argv[1]` can override the destination (useful to avoid locked folders).
   - Otherwise CodeScribe writes next to the `.project` file in `<ProjectName>ST/`.
4. If the target already exists it is deleted (`shutil.rmtree`) so the export always reflects the current project snapshot (`src/script_export_to_files.py:29`).

## Device and Application Traversal

The export is device-centric because CODESYS projects can host multiple PLCs:

- `get_device_entrypoints()` filters top-level children whose type is `DEVICE` (`src/entrypoint.py:40`).
- For each device CodeScribe creates `<export>/<device-name>/` using `safe_filename()` to keep Windows-friendly names and records the original name via `register_directory()` (metadata goes into `_names.json` so imports can restore exact names).
- Inside each device folder an `application/` subfolder hosts application logic. The script locates the `Application` object (`find_application()` in `src/entrypoint.py:55`) and walks every child with `export_child()` (`src/script_export_to_files.py:42`).

## Object-Type Export Strategy

`export_child()` (`src/import_export.py:197`) switches on the runtime type and calls the right serializer. Highlights:

- **POUs**: If they have textual implementations, CodeScribe writes `<Name>.st` using `_render_st()` so declaration and body sit in one file separated by `// --- BEGIN IMPLEMENTATION ---`. Otherwise they fall back to native XML.
- **GVLs / EVLs / NVLs**: Dual output—`<Name>.gvl.xml` (native) plus `<Name>.gvl.st` (text declaration only) (`src/import_export.py:103`).
- **Methods**: Saved as `<Parent>.<Method>.st` when textual; otherwise `<Parent>.<Method>.xml` (`src/import_export.py:138`).
- **Properties / Actions / Transitions**: Exported recursively as native XML (treated as “sub-POUs”) (`src/import_export.py:170`).
- **DUTs**: Always structured text (`src/import_export.py:126`).
- **Visualisations, EVCs, Tasks**: Exported with `export_native` (or `_recursive`) to capture the runtime XML representation.

All file writes go through `write_file()` and `write_native()`, which sanitize Unicode, normalize newlines, and register metadata (`src/util.py:60`). `write_native()` also zeroes `<Single Name="Timestamp">` fields so exports diff cleanly (`src/import_export.py:53`).

## Communication Export

After the application finishes, each device’s communication configuration is exported (`export_communication()` in `src/communication_import_export.py:12`):

- Creates `<device>/communication/`.
- For every top-level communication device, builds a folder and exports each child device as native XML (using `write_native(..., recursive=True)`).
- Adding a `_NO_EXPORT` folder under `Communication` lets you skip this step entirely—handy if templates already carry the communication setup.

## Name Preservation and Safe Files

- `safe_filename()` (`src/util.py:31`) strips smart punctuation and non-ASCII characters so every filesystem entry is valid cross-platform.
- The original name, parent, and kind (file vs dir) are stored in `_names.json` within each folder (`register_original_name()` / `register_directory()`). Import scripts read this metadata to reverse the sanitisation, so you can round-trip names like “MÄIN Pump ➜ Valve” without collisions.

## Resulting Folder Layout

```
<ProjectName>ST/
  _names.json
  Sprc_PLC/                # device
    _names.json
    application/
      MAIN.st
      Motion/_names.json
      Motion/PickAndPlace.st
      AlarmManager.gvl.xml
      AlarmManager.gvl.st
    communication/
      EtherCAT_Master/
        EK1100.xml
        EL1809.xml
```

Every directory shown above holds its own `_names.json` so imports understand the true object graph.

## Full Flow Recap

1. Script launches, validates context, and chooses/cleans the export destination.
2. Devices are enumerated; each gets a folder plus an `application/` subtree.
3. The application graph is walked depth-first, exporting every CODESYS object according to its type.
4. Communication devices export into native XML under `communication/` unless `_NO_EXPORT` short-circuits the step.
5. Safe names and metadata are emitted alongside `*.st` and `*.xml` files so the import scripts can perfectly rebuild the project later.

With this pipeline in mind you can confidently trace any exported file back to the object (and serialization path) that produced it, which makes debugging or extending the export feature far easier.
