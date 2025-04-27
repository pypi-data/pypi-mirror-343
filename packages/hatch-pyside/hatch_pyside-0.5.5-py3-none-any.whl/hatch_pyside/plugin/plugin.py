#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import os
from subprocess import CalledProcessError
from typing import Any

from hatchling.bridge.app import Application
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from ..build import build, clean

class PysideBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'pyside'

    def clean(self, _versions: list[str]) -> None:
        for f in self.config['folders']:
            try:
                self.app.display_debug(f'hatch-pyside build {f}', 1)
                cp = clean(os.path.join(self.root, f))
                self.app.display_debug(cp.stdout, 2)
            except CalledProcessError as e:
                dump(e, self.app)

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        for f in self.config['folders']:
            try:
                self.app.display_debug(f'hatch-pyside build {f}', 1)
                cp = build(os.path.join(self.root, f))
                self.app.display_debug(cp.stdout, 2)
            except CalledProcessError as e:
                dump(e, self.app)
                self.app.abort('Fatal', e.returncode)
        build_data['artifacts'].append('ui_*.py')


def dump(e: CalledProcessError, app: Application):
    app.display_error(f'Command {e.cmd} returned {e.returncode}\n'
                      f'{e.stdout}\n' f'{e.stderr}\n')
