#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import os
import sys
from subprocess import CalledProcessError
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

sys.path.append(os.path.dirname(__file__))
from hatch_pyside.build import build, clean
from hatch_pyside.plugin.plugin import dump


# A custom plugin to build the GUI
class CustomBuildHook(BuildHookInterface):

    def clean(self, _versions: list[str]) -> None:
        try:
            clean(os.path.join(self.root, 'src', 'hatch_pyside', 'gui'))
        except CalledProcessError as e:
            dump(e, self.app)

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        try:
            build(os.path.join(self.root, 'src', 'hatch_pyside', 'gui'))
        except CalledProcessError as e:
            dump(e, self.app)
            self.app.abort('Fatal', e.returncode)
