#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
"""This module wraps the calls to the pyside6-project command
used to build the relevant .py file from the Qt source ones
or to remove them.

command contains the full path of the first found pyside-project command.
"""
import shutil
import subprocess
import sysconfig

__all__ = ["command", "build", "clean"]

command: list[str]


try:
    _creation_flags = subprocess.CREATE_NO_WINDOW
except AttributeError:
    _creation_flags = 0

def run(cmd, folder) -> subprocess.CompletedProcess:
    """
    Pass the subcommand cmd to pyside6-project with the folder parameter
    Args:
        cmd:    the subcommand to execute (should be clean, lupdate or build)
        folder: the folder containing the .pyproject file

    Raises:
        CalledProcessError  if the pyside6-project command returns a non 0 exit code
    """
    return subprocess.run(
        command + [cmd, folder],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=True,
        creationflags=_creation_flags,
    )


def build(folder: str) -> subprocess.CompletedProcess:
    """
    Calls run to build the dependant files
    Args:
        folder:  the folder containing the .pyproject file

    Raises:
        CalledProcessError  if the pyside6-project command returns a non 0 exit code
    """
    return run("build", folder)


def clean(folder: str) -> subprocess.CompletedProcess:
    """
    Calls run to clean the dependant files
    Args:
        folder:  the folder containing the .pyproject file

    Raises:
        CalledProcessError  if the pyside6-project command returns a non 0 exit code
    """
    return run("clean", folder)


def lupdate(folder: str) -> subprocess.CompletedProcess:
    """
    Calls run to update the translation files
    Args:
        folder:  the folder containing the .pyproject file

    Raises:
        CalledProcessError  if the pyside6-project command returns a non 0 exit code
    """
    return run("lupdate", folder)


def _build_command() -> str:
    # first search the command in the path
    prog = "pyside6-project"
    cmd = shutil.which(prog)
    if cmd is None:
        # else search it in any possible script installation folder
        visited = set()
        for d in (
            sysconfig.get_path("scripts", scheme)
            for scheme in sysconfig.get_scheme_names()
        ):
            if d in visited:  # only search once in each folder
                continue
            visited.add(d)
            cmd = shutil.which(prog)
            if cmd is not None:
                break
        else:
            raise RuntimeError(f"No installation of {prog} found")
    return cmd


# compute command at import time
command = [_build_command()]

