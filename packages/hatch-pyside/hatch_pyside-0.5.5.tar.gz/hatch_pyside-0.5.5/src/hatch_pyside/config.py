#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
"""Manages the extraction of relevant parameters from a pyproject.toml file"""
from typing import Any, Optional

# a hack to cope with tomllib not present in Python 3.9
try:
    # noinspection PyUnresolvedReferences
    import tomllib
except ImportError:
    # noinspection PyUnresolvedReferences
    import tomli as tomllib


def get_values(cfg: dict[str, Any]) -> Optional[list[str]]:
    """
    Extract the cumulative config for the pyside plugin: both global and wheel
    Args:
        cfg: the content of the hatch.toml file or of
        the tool.hatch table of pyproject.toml

    Returns:
        the relevant config

    Raises:
        KeyError    if no config is present for the plugin
    """
    try:
        return cfg["build"]["targets"]["wheel"]["hooks"]["pyside"]["folders"]
    except KeyError:
        return cfg["build"]["hooks"]["pyside"]["folders"]


def get_project_folders() -> tuple[str, Optional[list[str]]]:
    """
    Extract hatch-pyside config from pyproject.toml or hatch.toml

    Returns:
        the relevant config or None

    Raises:
        KeyError    if project.name is not found in pyproject.toml
        OSError     if pyproject.toml is not found
    """
    name = None
    try:
        with open("pyproject.toml", "rb") as fd:
            json = tomllib.load(fd)
            name = json["project"]["name"]
            return name, get_values(json["tool"]["hatch"])
    except KeyError:
        if name is None:
            raise
        try:
            with open("hatch.toml", "rb") as fd:
                return name, get_values(tomllib.load(fd))
        except (OSError, KeyError):
            return name, None
