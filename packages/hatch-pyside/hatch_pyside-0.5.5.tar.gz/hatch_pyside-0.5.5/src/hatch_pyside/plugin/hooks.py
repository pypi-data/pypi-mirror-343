#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT

from hatchling.plugin import hookimpl

from .plugin import PysideBuildHook


@hookimpl
def hatch_register_build_hook():
    return PysideBuildHook