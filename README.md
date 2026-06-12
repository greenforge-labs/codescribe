# CODESCRIBE

[![CI](https://github.com/greenforge-labs/codescribe/actions/workflows/ci.yml/badge.svg)](https://github.com/greenforge-labs/codescribe/actions/workflows/ci.yml)

_/koh-DEH-skribe/_

Allows you to use version control for CODESYS projects.

## The problem

A CODESYS project is a single `.project` file in a proprietary binary format. Git can store it, but it cannot diff it, merge it, or review it since every change is an all-or-nothing binary blob. That rules out meaningful code review, parallel development and a usable change history.

CODESCRIBE exports the logic of a CODESYS project to plaintext files that git handles like any other source code, and imports those files back into CODESYS. A CODESYS project like this:

![example_project_codesys](docs/example_project_codesys.png)

becomes a plaintext project like this:

![example_project_vscode](docs/example_project_vscode.png)

## How it works

CODESCRIBE supplies five scripts that run inside the CODESYS ScriptEngine and appear as toolbar buttons. No Python installation is required to use them as CODESYS ships with its own copy of Python 2.

![toolbar](docs/toolbar.png)

- `Export To Files` exports the project to plaintext files that can be tracked in source control, as well as edited in other editors
- `Import From Files` imports plaintext files back into a CODESYS project for uploading / debugging / etc
- `Save As Template` generates a "template" project by making a copy of the current project and deleting all exportable objects
- `Update From Template` updates the current working project by copying the template file and importing the plaintext files
- `Export Lib To Files` exports a library project, which keeps its objects directly under the project root rather than under a Device (see [Export Lib To Files](#export-lib-to-files))

A typical workflow:

1. Make changes in CODESYS, then click `Export To Files`.
2. Commit the exported files. Diff, review and merge them in git like any other code.
3. Pull a teammate's changes, or edit the `.st` files directly in another editor.
4. Click `Import From Files` to bring the changes back into CODESYS.

Each script reports its outcome in a dialog when it finishes. Failures show the full Python traceback, so problems do not hide in the message view.

## What gets exported

- Folders
- POUs
- GVLs (including persistent variable lists)
- EVLs
- EVCs
- Task Configurations
- DUTs
- Methods
- Properties
- Actions
- Transitions
- Communication Devices\*
- Device-tree devices\*

\*see [Exporting and Importing Communication Devices](#exporting-and-importing-communication-devices)

Items are exported in formatted structured text (`.st`) where possible, and in native CODESYS xml everywhere else. The `.st` files are written as UTF-8, so non-ASCII content (Cyrillic, accented characters, smart punctuation) exports and round-trips correctly.

Actions and Transitions export as `.st` with the kind encoded in the filename (`MyPou.MyAction.action.st`, `MyPou.MyTransition.transition.st`). The file contains the implementation text only, as these objects have no textual declaration.

Visualisations export as `<name>.vis.xml`, so a `Main` visualisation cannot collide with a `Main` POU.

Exports made with older versions of CODESCRIBE use different filenames for some of these objects; they still import correctly, and re-exporting once migrates the tracked files. See [CHANGELOG.md](CHANGELOG.md) for the details.

## Export Lib To Files

Library projects keep their POUs, DUTs, GVLs and folders directly under the project root rather than under a Device, so `Export To Files` (which walks device entrypoints) exports nothing for them. `Export Lib To Files` walks the project root instead and writes the same on-disk format as `Export To Files`, without the device and application folder levels. Service objects (Library Manager, Project Information, Project Settings, and the Task/Symbol/Visualization/Alarm/Recipe manager objects) are skipped.

Importing a library export back into a project is not yet supported.

## Project Templates

CODESCRIBE exports the implementation logic of the project, not a complete copy. An empty, but configured, underlying project file should also be committed to the repo to manage any other configuration that CODESYS provides (e.g. project level configuration, device configuration). For example, `Example Project_template_v1.project`:

![example_template_file](docs/example_template_file.png)

_Note, it is recommended to not source control the actual working copy of the project (`Example Project.project`) to avoid duplication._

A template file can be generated from an existing project file by using the `Save As Template` script. This script will copy the project, give it the appropriate name and delete any objects that can be imported by CODESCRIBE. If an existing project following the template naming scheme is found, the new template will use an incremented version number.

To generate a project from a template file, you need two things: the `<project_name>_template_v<X>.project` file and a folder named `<project_name>` with the files exported by the `Export To Files` script. To generate a project, copy the template project in the same location and rename it to `<project_name>.project`. Open the copy with CODESYS and use the `Import From Files` button to import the project files.

## Exporting and Importing Communication Devices

Exporting communication devices has been hardcoded to create folders for top-level devices under `Communication`. Any devices under these top-level devices will be exported using native CODESYS xml. This is done because the top-level devices can not be removed from the CODESYS project.

**If this functionality is causing you problems, it can be disabled by adding a folder with the name `_NO_EXPORT` directly under `Communication`.** You can then still rely on your project template to carry your communication configurations.

Devices that have no `Communication` object at all are also supported. The communication step is skipped for that device and no `communication` folder is created in the export.

A second layout is also supported: on standard CODESYS hardware, Ethernet, Modbus and fieldbus devices often sit in the device tree as direct children of the PLC device, next to `Plc Logic`, rather than under a `Communication` node. These device-tree siblings are exported to `<device>/devices/<name>.xml` using a native recursive export, one file per top-level device. Children that contain an `Application` (for example the SafetyPLC and StandardPLC of a compound safety project) are excluded, as they are already exported through their own device entrypoint.

On import, each tracked device is removed and recreated from its exported xml. Devices fixed by the device package (for example `Local_IO` and `HMI` on IFM hardware) cannot be removed; they are skipped with a message and their configuration is carried by the project template instead.

**To disable the device-tree export, add a folder with the name `_NO_EXPORT` as a direct child of the PLC device.** The existing `_NO_EXPORT` folder under `Communication` continues to disable only the `Communication` export.

## Export folder locked (Windows)

`Export To Files` writes the export into a sibling folder named `<project_name>.codescribe_staging` and only swaps it into place once the export completes, so a mid-export failure cannot destroy the existing on-disk copy.

If the target folder is locked (an open Explorer window, IDE, git client or antivirus) and cannot be swapped, the staged files are synced into it instead and the export still succeeds. If that also fails, the error dialog reports the staging folder path; the completed export is preserved there, so nothing is lost.

## Status

CODESCRIBE has been tested only on CODESYS V3.5 SP11, using the project structure supplied by the IFM CR711s packages. Version 0.2.0 was validated end-to-end on V3.5 SP11 (32-bit) with an IFM CR711S compound (Standard + SIL2) project: export/import round-trip, code generation, simulation and a hardware download.

See [CHANGELOG.md](CHANGELOG.md) for version history and upgrade notes.

## Installing

### Using the install script

Using the install script requires Python 3 to be installed on your system (https://www.python.org/downloads/).

Once the repo is cloned, run `install.bat` as administrator. This will in turn run `install.py`.

Once installed, proceed to [Adding the Script Toolbar to CODESYS](#adding-the-script-toolbar-to-codesys).

### Installing manually

Copy `config.json` to `C:\<CODESYS INSTALL LOCATION>\CODESYS\Script Commands`. The `Script Commands` folder may need to be created.

Open the copy of `config.json` and edit the `"Icon"` and `"Path"` fields to point to their respective locations in cloned repo (under `src` and `icons`). For example, this config:

```json
"Icon": "export_to_files.ico",
"Path": "script_export_to_files.py",
```

Should be changed to:

```json
"Icon": "<PATH TO REPO>\\icons\\export_to_files.ico",
"Path": "<PATH TO REPO>\\src\\script_export_to_files.py",
```

_NOTE: the escaped backslashes (`\\`) are required for windows paths in json_

Once installed, proceed to [Adding the Script Toolbar to CODESYS](#adding-the-script-toolbar-to-codesys).

## Adding the Script Toolbar to CODESYS

1. Select Tools -> Customize

    ![Step 1](docs/step_1.png)

2. Select Toolbars

    ![Step 2](docs/step_2.png)

3. Select the blank toolbar at the bottom of the list and click "Add toolbar". Call it `Scripts`.

    ![Step 3](docs/step_3.png)

4. Expand `Scripts`, select the blank spot and click "Add command"

    ![Step 4](docs/step_4.png)

5. Under Categories, scroll down, select ScriptEngine Commands and pick the script you want to add

    - Scripts supplied by this repo are `Export To Files`, `Export Lib To Files`, `Import From Files`, `Save As Template` and `Update From Template`

    ![Step 5](docs/step_5.png)

6. Repeat the process to add the other scripts

    ![Step 6](docs/step_6.png)

7. Click OK to save changes

    ![Step 7](docs/step_7.png)

8. You should now have new icons available in your toolbar

    ![Step 8](docs/step_8.png)

## Development

The scripts run inside the CODESYS ScriptEngine, which embeds IronPython 2.7:

- All code in `src/` must be Python 2.7 compatible.
- Source files must be pure ASCII. IronPython enforces PEP 263 (ASCII source unless an encoding is declared), and a single stray em-dash or smart quote in a comment will make CODESYS refuse to load the file.
- `main` is protected: changes go through a pull request and the CI checks must pass.
- Changes that alter the export format or behaviour should be noted in [CHANGELOG.md](CHANGELOG.md).

CI runs two jobs on every pull request (see `.github/workflows/ci.yml` and `tools/ci/`):

- `ascii-check`: fails on any non-ASCII byte in `src/*.py`.
- `ironpython`: compiles every src file with real IronPython 2.7.12 (catches Python 2 syntax errors) and imports the library modules against a stubbed `scriptengine` (catches module-scope errors).

Note that `python -m py_compile` under Python 3 is not a sufficient local check; it misses both failure classes above.

## CODESYS Scripting Docs

- https://help.codesys.com/webapp/idx-scriptingengine;product=ScriptEngine;version=3.5.10.0 (dead link)
- `C:\<CODESYS INSTALL LOCATION>\CODESYS\Online Help\en\ScriptEngine.chm`
- [ScriptEngine V3.5 SP11 API Reference (converted from CHM)](docs/references/codesys_scriptengine_v3.5_sp11_api_reference.md)

## Similar Projects

- https://github.com/18thCentury/CodeSys
