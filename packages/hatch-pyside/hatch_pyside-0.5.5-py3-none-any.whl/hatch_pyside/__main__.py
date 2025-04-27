#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
"""Tiny wrapper to allow the package to be used as a module"""

import sys

from hatch_pyside.gui import app

if __name__ == "__main__":
    sys.exit(app.main())
