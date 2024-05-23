"""
Needs to be run as administrator!
Use install.bat: Right click -> "Run as administrator"
"""

import json
from pathlib import Path
import shutil

from typing import TypeVar


class TerminalColours:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_fail(msg: str):
    print(msg, end="\n\n")
    # print(TerminalColours.FAIL + msg + TerminalColours.ENDC)


def print_warning(msg: str):
    print(msg, end="\n\n")
    # print(TerminalColours.WARNING + msg + TerminalColours.ENDC)


def print_ok(msg: str):
    print(msg, end="\n\n")
    # print(TerminalColours.OKBLUE + msg + TerminalColours.ENDC)


T = TypeVar("T")


def select_option(options: list[T], *, none_msg: str, one_msg: str, many_msg: str) -> T:
    if len(options) < 1:
        print_fail(none_msg)
        exit(0)
    elif len(options) == 1:
        print_ok(one_msg.format(single_option=options[0]))
        return options[0]
    else:
        while True:
            print_ok(many_msg.format(num_options=len(options)))
            for i, option in enumerate(options):
                print(f"({i+1}) {str(option)}")
            selection = input("Selection: ")
            try:
                selection = int(selection) - 1
                if selection < 0:
                    raise ValueError()
                return options[selection]
            except (ValueError, IndexError):
                print_fail("Unknown selection!\n")


def find_repo_config_json() -> Path:
    repo_path = Path(__file__).parent
    config_json = repo_path / "config.json"
    if not config_json.exists():
        print_fail(f"ERROR: expecting to find config.json at {config_json}")
        exit(0)

    return config_json


def get_config_path_remappings(config_path: Path) -> dict[str, str]:
    with open(config_path, "r") as f:
        config = json.load(f)

    remappings = {}
    success = True
    src_path = config_path.parent / "src"
    icons_path = config_path.parent / "icons"
    for script in config:
        script_path = src_path / str(script["Path"])
        if script_path.exists():
            remappings[str(script["Path"])] = str(script_path).replace("\\", "\\\\")
        else:
            print_fail(f"ERROR: expecting script at {script_path}")
            success = False

        icon_path = icons_path / str(script["Icon"])
        if icon_path.exists():
            remappings[str(script["Icon"])] = str(icon_path).replace("\\", "\\\\")
        else:
            print_fail(f"ERROR: expecting icon at {icon_path}")
            success = False

    if not success:
        exit(0)

    return remappings


def find_codesys_install_paths() -> list[Path]:
    program_files = Path("C:/Program Files")
    program_files_x86 = Path("C:/Program Files (x86)")

    found_paths = []

    for prg_files_path in [program_files, program_files_x86]:
        for child in prg_files_path.iterdir():
            if child.is_dir() and "CODESYS" in child.name:
                found_paths.append(child)

    return found_paths


def get_or_create_script_path(codesys_install_path: Path) -> Path:
    codesys_path = codesys_install_path / "CODESYS"
    if not codesys_path.exists() or not codesys_path.is_dir():
        print_fail(f"ERROR: expected directory to exist: {codesys_path}")
        exit(0)

    script_path = codesys_path / "Script Commands"
    if not script_path.exists():
        print_ok(f"Creating directory: {script_path}")
        script_path.mkdir()

    if not script_path.is_dir():
        print_fail(f"ERROR: expected to be a directory: {script_path}")
        exit(0)

    return script_path


def rename_or_get_config_json_destination(script_path: Path) -> Path:
    config_json = script_path / "config.json"
    if config_json.exists():
        print_warning(f"WARNING: existing config found, renaming to config.backup.json: {config_json}")
        try:
            backup_path = config_json.parent / "config.backup.json"
            config_json.rename(backup_path)
        except FileExistsError:
            print_fail(f"ERROR: file already exists: {backup_path}")
            exit(0)

    return config_json


def copy_config_json_and_remap_paths(repo_config: Path, config_destination: Path, path_remappings: dict[str, str]):
    shutil.copy(repo_config, config_destination)

    with open(config_destination, "r") as f:
        contents = f.read()

    for find, replace in path_remappings.items():
        contents = contents.replace(find, replace)

    with open(config_destination, "w") as f:
        f.write(contents)

    print_ok(f"SUCCESS: config written to {config_destination}")


if __name__ == "__main__":
    try:
        print()
        repo_config_json = find_repo_config_json()
        config_path_remappings = get_config_path_remappings(repo_config_json)

        install_paths = find_codesys_install_paths()
        install_path = select_option(
            install_paths,
            none_msg="No CODESYS install paths found!",
            one_msg="CODESYS install path found: {single_option}",
            many_msg="{num_options} CODESYS install paths found:",
        )

        script_path = get_or_create_script_path(install_path)
        config_json_destination = rename_or_get_config_json_destination(script_path)

        copy_config_json_and_remap_paths(repo_config_json, config_json_destination, config_path_remappings)
    except PermissionError:
        print_fail(f"Permission error! Are you running as administrator?")
        exit(0)
