# CODESCRIBE

[![CI](https://github.com/greenforge-labs/codescribe/actions/workflows/ci.yml/badge.svg)](https://github.com/greenforge-labs/codescribe/actions/workflows/ci.yml)

_/koh-DEH-skribe/_

CODESYS plaintext import and export scripts.

No python installation is required to use the scripts as CODESYS ships with its own copy of Python 2.

CODESCRIBE supplies CODESYS scripts to:

- export a project to plaintext files that can be tracked in source control, as well as edited in other editors
- import plaintext files back into a CODESYS project for uploading / debugging / etc
- generate a "template" project by making a copy of the current project and deleting all exportable objects
- update the current working project from a template by copying the template file and importing plaintext files

![toolbar](docs/toolbar.png)

Since v0.2.0, each script reports its outcome in a dialog when it finishes. Failures show the full Python traceback, so problems no longer hide in the message view.

With CODESCRIBE, a CODESYS project like this:
![example_project_codesys](docs/example_project_codesys.png)

Becomes a plaintext project like this:
![example_project_vscode](docs/example_project_vscode.png)

The following items are exported:

- Folders
- POUs
- EVLs
- EVCs
- Task Configurations
- DUTs
- Methods
- Properties
- Actions
- Transitions
- Communication Devices\*

\*see [Exporting and Importing Communication Devices](#exporting-and-importing-communication-devices)

Items are exported in formatted structured text (`.st`) where possible, and in native CODESYS xml everywhere else. The `.st` files are written as UTF-8, so non-ASCII content (Cyrillic, accented characters, smart punctuation) exports and round-trips correctly since v0.2.0.

Since v0.2.0, Actions and Transitions export as `.st` rather than native xml. The kind is encoded in the filename (`MyPou.MyAction.action.st`, `MyPou.MyTransition.transition.st`) and the file contains the implementation text only, as these objects have no textual declaration. Exports made with earlier versions (where these objects were `.xml`) still import correctly; re-exporting once after upgrading migrates the tracked files to the new format.

Visualisations export as `<name>.vis.xml`. Earlier versions wrote `<name>.xml`, which silently collided with any POU of the same name (a `Main` program plus a `Main` visualisation is common). Old plain `.xml` exports still import correctly; re-exporting once migrates the tracked files.

## Export folder locked (Windows)

`Export To Files` writes the export into a sibling folder named `<project_name>.codescribe_staging` and only swaps it into place once the export completes. Earlier versions deleted the target folder up front, so a locked folder (an open Explorer window, IDE, git client or antivirus) aborted the export immediately and a mid-export crash left the on-disk copy destroyed.

If the target folder is locked and cannot be swapped, the staged files are synced into it instead and the export still succeeds. If that also fails, the error dialog reports the staging folder path; the completed export is preserved there, so nothing is lost.

## Project Templates

The intention of CODESCRIBE is not to export a complete copy of the project, but to only export the implementation logic of the project, enabling collaboration via git and other source control methods. An empty, but configured, underlying project file should also be committed to the repo to manage any other configuration that CODESYS provides (e.g. project level configuration, device configuration). For example, `Example Project_template_v1.project`:

![example_template_file](docs/example_template_file.png)

_Note, it is recommended to not source control the actual working copy of the project (`Example Project.project`) to avoid duplication._

A template file can be generated from an existing project file by using the `Save As Template` script. This script will copy the project, give it the appropriate name and delete any objects that can be imported by CODESCRIBE. If an existing project following the template naming scheme is found, the new template will use an incremented version number.

To generate a project from a template file, you need two things: the `<project_name>_template_v<X>.project` file and a folder named `<project_name>` with the files exported by the `Export To Files` script. To generate a project, copy the template project in the same location and rename it to `<project_name>.project`. Open the copy with CODESYS and use the `Import From Files` button to import the project files.

## Exporting and Importing Communication Devices

Exporting communication devices has been hardcoded to create folders for top-level devices under `Communication`. Any devices under these top-level devices will be exported using native CODESYS xml. This is done because the top-level devices can not be removed from the CODESYS project.

**If this functionality is causing you problems, it can be disabled by adding a folder with the name `_NO_EXPORT` directly under `Communication`.** You can then still rely on your project template to carry your communication configurations.

Devices that have no `Communication` object at all are also supported since v0.2.0. The communication step is skipped for that device and no `communication` folder is created in the export; before v0.2.0 this aborted the export, import or Save As Template for the whole device.

## Status

CODESCRIBE has been tested only on CODESYS V3.5 SP11, using the project structure supplied by the IFM CR711s packages. Version 0.2.0 was validated end-to-end on V3.5 SP11 (32-bit) with an IFM CR711S compound (Standard + SIL2) project: export/import round-trip, code generation, simulation and a hardware download.

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

    - Scripts supplied by this repo are `Export To Files`, `Import From Files`, `Save As Template` and `Update From Template`

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
