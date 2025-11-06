# -*- coding: utf-8 -*-
# REMEMBER: this is python 2.7
import io
import json
import os
import re
import sys

try:
    import unicodedata
except Exception:
    unicodedata = None

import scriptengine  # type: ignore

from object_type import get_object_type

SMART_MAP = {
    u"\u2013": u"-",  # en dash
    u"\u2014": u"-",  # em dash
    u"\u2018": u"'",  # left single quote
    u"\u2019": u"'",  # right single quote
    u"\u201c": u'"',  # left double quote
    u"\u201d": u'"',  # right double quote
    u"\xa0": u" ",  # non-breaking space
}

_NAMES_FILE = "_names.json"
_NAMES_CACHE = {}


def _to_u(s):
    try:
        return s if isinstance(s, unicode) else unicode(s, "utf-8", "ignore")
    except NameError:
        return s


def sanitize_text(s):
    u = _to_u(s)
    for k, v in SMART_MAP.items():
        u = u.replace(k, v)
    return u


def safe_filename(name):
    u = sanitize_text(name)
    if unicodedata:
        u = unicodedata.normalize("NFKD", u)
    try:
        u = u.encode("ascii", "ignore").decode("ascii")
    except Exception:
        pass
    u = re.sub(r"[^\w\-. ]+", "_", u)
    u = u.strip().rstrip(".")
    return u or "unnamed"


def ensure_dir(directory):
    if directory and not os.path.isdir(directory):
        os.makedirs(directory)


def _names_meta_path(directory):
    return os.path.join(directory, _NAMES_FILE)


def _load_names(directory):
    if directory in _NAMES_CACHE:
        return _NAMES_CACHE[directory]
    meta_path = _names_meta_path(directory)
    if not directory or not os.path.exists(meta_path):
        data = {}
    else:
        try:
            with io.open(meta_path, "r", encoding="utf-8") as meta_file:
                content = meta_file.read()
                data = json.loads(content) if content else {}
        except Exception:
            data = {}
    _NAMES_CACHE[directory] = data
    return data


def register_original_name(directory, safe_key, original_name, parent_name=None, kind=None):
    if not directory or not safe_key or not original_name:
        return
    entry = {"name": original_name}
    if parent_name:
        entry["parent"] = parent_name
    if kind:
        entry["kind"] = kind
    names = _load_names(directory)
    if names.get(safe_key) == entry:
        return
    names[safe_key] = entry
    ensure_dir(directory)
    meta_path = _names_meta_path(directory)
    with io.open(meta_path, "w", encoding="utf-8") as meta_file:
        json.dump(names, meta_file, ensure_ascii=False, indent=2, sort_keys=True)
        meta_file.write(u"\n")


def get_original_entry(directory, safe_key):
    if not directory or not safe_key:
        return None
    names = _load_names(directory)
    return names.get(safe_key)


def resolve_original_name(directory, safe_key, default=None):
    entry = get_original_entry(directory, safe_key)
    if entry and entry.get("name"):
        return entry["name"]
    if default is not None:
        return default
    return safe_key


def find_safe_name(directory, original_name, kind=None, parent_name=None):
    if not directory or not original_name:
        return None
    names = _load_names(directory)
    for safe_key, entry in names.items():
        if entry.get("name") != original_name:
            continue
        if kind and entry.get("kind") != kind:
            continue
        if parent_name and entry.get("parent") != parent_name:
            continue
        return safe_key
    return None


def write_file(path, text, original_name=None, parent_name=None):
    """UTF-8 writer with newline normalization + sanitization."""
    ensure_dir(os.path.dirname(path))
    with io.open(path, "w", encoding="utf-8", newline=u"\n") as f:
        f.write(sanitize_text(_to_u(text)))
    if original_name:
        register_original_name(
            os.path.dirname(path),
            os.path.basename(path),
            original_name,
            parent_name=parent_name,
            kind="file",
        )


def register_directory(parent_directory, safe_name, original_name):
    register_original_name(parent_directory, safe_name, original_name, kind="dir")


def print_python_version():
    print("Python version: " + sys.version)


def assert_project_open():
    if scriptengine.projects.primary is None:
        raise ValueError("You must have a project open!")


def assert_path_exists(path):
    if not os.path.exists(path):
        raise ValueError("Path " + path + " does not exist")


def first_or_none(lst):
    return next(iter(lst), None)


def first_of_type_or_error(lst, obj_type, err):
    for obj in lst:
        if get_object_type(obj) == obj_type:
            return obj
    raise ValueError(err)


def first_of_type_or_none(lst, obj_type):
    for obj in lst:
        if get_object_type(obj) == obj_type:
            return obj
    return None


def first_or_error(lst, err):
    try:
        return next(iter(lst))
    except StopIteration:
        raise ValueError(err)
