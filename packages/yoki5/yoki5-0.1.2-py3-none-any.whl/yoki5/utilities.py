"""Utilities for yoki5."""

from __future__ import annotations

import typing as ty
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

import h5py
import numpy as np
from koyo.secret import get_short_hash
from koyo.typing import PathLike

TIME_FORMAT = "%d/%m/%Y-%H:%M:%S:%f"


def encode_str_array(array: np.ndarray | list[str], encoding: str = "utf-8") -> np.ndarray:
    """Encode array of U strings as S strings."""
    if isinstance(array, list):
        return np.asarray([v.encode(encoding) for v in array])

    if np.issubdtype(array.dtype, np.dtype("S")):
        return array
    out = [v.encode(encoding) for v in array]
    return np.asarray(out)


def decode_str_array(array: np.ndarray | list[str], encoding: str = "utf-8") -> np.ndarray:
    """Decode array of S strings to U strings."""
    if isinstance(array, list):
        return np.asarray([v.decode(encoding) for v in array])

    if np.issubdtype(array.dtype, np.dtype("U")):
        return array
    if array.ndim == 1:
        out = [v.decode(encoding) for v in array]
    else:
        out = [[v.decode(encoding) for v in row] for row in array]
    return np.asarray(out)


def resize_by_append_1d(h5: h5py.Group, key: str, array: np.ndarray) -> None:
    """Resize 2D array along specified dimension."""
    h5[key].resize(h5[key].shape[0] + array.shape[0], axis=0)
    h5[key][-array.shape[0] :] = array


def resize_by_insert_1d(h5: h5py.Group, key: str, array: np.ndarray, indices: list[int]) -> None:
    """Resize 2D array along specified dimension."""
    h5[key].resize(h5[key].shape[0] + len(indices), axis=0)
    h5[key][-array.shape[0] :] = array[indices]


def resize_by_append_2d(h5: h5py.Group, key: str, array: np.ndarray, axis: int) -> None:
    """Resize 2D array along specified dimension."""
    if axis > 1:
        raise ValueError("Cannot resize 2d array with index larger than 1.")
    h5[key].resize(h5[key].shape[axis] + array.shape[axis], axis=axis)
    if axis == 0:
        h5[key][-array.shape[axis] :, :] = array
    else:
        h5[key][:, -array.shape[axis] :] = array


def resize_by_insert_2d(h5: h5py.Group, key: str, array: np.ndarray, axis: int, indices: list[int]) -> None:
    """Resize 2D array along specified dimension."""
    h5[key].resize(h5[key].shape[axis] + len(indices), axis=axis)
    for i, _index in enumerate(indices):
        h5[key][:, -len(indices) + i] = array


def check_base_attributes(attrs: dict) -> None:
    """Check attributes for missing keys."""
    if "unique_id" not in attrs:
        attrs["unique_id"] = get_short_hash()
    if "date_created" not in attrs:
        attrs["date_created"] = datetime.now().strftime(TIME_FORMAT)
    if "date_edited" not in attrs:
        attrs["date_edited"] = datetime.now().strftime(TIME_FORMAT)


def check_data_keys(data: dict, keys: list[str]) -> bool:
    """Check whether all keys have been defined in the data."""
    for key in keys:
        if key not in data:
            return False
    return True


def prettify_names(names: list[str]) -> list[str]:
    """Prettify names by removing slashes."""
    if not isinstance(names, Iterable):
        raise ValueError("Cannot prettify list")
    return [_name.split("/")[-1] for _name in names]


def parse_from_attribute(attribute: ty.Any) -> ty.Any:
    """Parse attribute from cache."""
    if isinstance(attribute, str) and attribute == "__NONE__":
        attribute = None
    return attribute


def parse_to_attribute(attribute: ty.Any) -> ty.Any:
    """Parse attribute to cache."""
    if attribute is None:
        attribute = "__NONE__"
    return attribute


def check_read_mode(mode: str) -> None:
    """Check file opening mode."""
    if mode not in ["r", "a"]:
        raise ValueError(
            "Incorrect opening mode - Please use either `r` or `a` mode to open this file to avoid overwriting"
            " existing data."
        )


def find_case_insensitive(key: str, available_options: list[str]) -> str:
    """Find the closest match."""
    _available = [_key.lower() for _key in available_options]
    try:
        index = _available.index(key.lower())
    except IndexError:
        raise KeyError("Could not retrieve item.") from None
    return available_options[index]


def get_unique_id(path: PathLike) -> str:
    """Get unique ID from path."""
    import h5py

    with h5py.File(path, mode="r", rdcc_nbytes=1024 * 1024 * 4) as f_ptr:
        unique_id = f_ptr.attrs.get("unique_id") or get_short_hash()
    return unique_id


def display_name_contains(
    klass, filelist: ty.Iterable[PathLike], contains: str, get_first: bool = False
) -> Path | list[Path]:
    """Return list or item which has specified display name."""
    assert hasattr(klass, "display_name"), "Class object is missing 'display_name' attribute."
    _filelist = []
    for file in filelist:
        obj = klass(file)
        if get_first:
            if contains == obj.display_name:
                _filelist.append(file)
        else:
            if contains in obj.display_name:
                _filelist.append(file)
    if get_first and _filelist:
        return _filelist[0]
    return _filelist


def name_contains(
    filelist: ty.Iterable[PathLike],
    contains: str,
    get_first: bool = False,
    base_dir: PathLike | None = None,
    filename_only: bool = False,
    exact_match: bool = False,
) -> Path | list[Path]:
    """Return list of items which contain specified string."""
    from pathlib import Path

    if contains is None:
        contains = ""
    contains = str(contains)

    # check if contains is a wildcard
    if "*" in contains and base_dir:
        # make sure contains has HDF5 extension
        if not contains.endswith(".h5"):
            end = "*.h5"
            if contains.endswith("*"):
                end = end[0:-1]
            contains += end

        # this will match ANY files in the directory, even if it is not directly in the folder but in the general path
        filelist = list(Path(base_dir).glob(contains))
        if get_first and filelist:
            return filelist[0]
        return filelist

    # check if contains is a file
    if Path(contains).is_file() and Path(contains).exists():
        path = Path(contains)
        if get_first:
            return path
        return [path]

    filelist_ = []
    contains = contains.lower()
    if not exact_match:
        for file in [Path(p) for p in filelist]:
            if contains in str(file.name if filename_only else file).lower():
                filelist_.append(file)
    else:
        has_h5 = contains.endswith(".h5")
        for file in [Path(p) for p in filelist]:
            if contains == str((file.name if has_h5 else file.stem) if filename_only else file).lower():
                filelist_.append(file)
    if get_first and filelist_:
        return filelist_[0]
    return filelist_


def get_object_path(path_or_tag: PathLike, func: ty.Callable, kind: str) -> Path:
    """Return path or check whether path with tag exists."""
    if isinstance(path_or_tag, list):
        raise ValueError("List of paths is not supported.")
    if path_or_tag is None or not Path(path_or_tag).exists() or not Path(path_or_tag).is_file():
        filelist: list[Path] = func(path_or_tag)
        if not filelist:
            raise ValueError(f"List of '{kind}' was empty. Input={path_or_tag}")
        elif len(filelist) > 1:
            # if by any chance the selected paths end with the specified tag, let's pick it
            for path in filelist:
                if path.stem.endswith(str(path_or_tag)):
                    return path
            filelist_str = "\n".join(map(str, filelist))
            raise ValueError(f"List of '{kind}' had more than one entry. Input={path_or_tag}. Entries=\n{filelist_str}")
        path_or_tag = filelist[0]
    path = Path(path_or_tag)
    if not path.exists():
        raise ValueError(f"The specified {kind} does not exist.")
    return path


def optimize_chunks_along_axis(
    axis: int,
    *,
    array: np.ndarray | None = None,
    shape: tuple[int, ...] | None = None,
    dtype: ty.Any = None,
    max_size: int = 1_000_000,
    auto: bool = True,
) -> tuple[int, ...] | None:
    """Optimize chunk size along specified axis."""
    if array is not None:
        dtype, shape = array.dtype, array.shape
    elif shape is None or dtype is None:
        raise ValueError("You must specify either an array or `shape` and `dtype`")
    assert len(shape) == 2, "Only supporting 2d arrays at the moment."
    assert axis <= 1, "Only supporting 2d arrays at the moment, use -1, 0 or 1 in the `axis` argument"
    assert hasattr(dtype, "itemsize"), "Data type must have the attribute 'itemsize'"
    item_size = np.dtype(dtype).itemsize

    if max_size == 0:
        return None

    n = 0
    if auto:
        max_n = shape[1] if axis == 0 else shape[0]
        while (n * item_size * shape[axis]) <= max_size and n < max_n:
            n += 1
    if n < 1:
        n = 1
    return (shape[0], n) if axis == 0 else (n, shape[1])
