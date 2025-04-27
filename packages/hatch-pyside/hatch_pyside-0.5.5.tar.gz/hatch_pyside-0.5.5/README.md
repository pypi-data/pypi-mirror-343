# hatch-pyside

[![PyPI - Version](https://img.shields.io/pypi/v/hatch-pyside.svg)](https://pypi.org/project/hatch-pyside)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-pyside.svg)](https://pypi.org/project/hatch-pyside)

-----

## Table Of Contents
  * [Goal](#goal)
  * [Status](#status)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Plugin](#plugin)
    * [GUI](#gui)
    * [Developer](#developer)
  * [Compatibility](#compatibility)
  * [Contributing](#contributing)
  * [License](#license)
## Goal

This is a hatch plugin able to automatically build the required Python files
from their associated Qt source file. For example, it will build a
`ui_MainWindow.py` file from a `MainWindow.ui` one.

Additionally, it installs `pyside-build`, a GUI tool to manage the
`proj_name.pyproject` file
that is used by `pyside6-project` (which is internally called by
`hatch-pyside`).

## Status

The plugin and the GUI are currently beta quality. They still lack real world
tests and a decent documentation.

Starting with the 0.5.4 version, the plugin provides explanatory messages if 
the underlying `pyside6-project` command fails.

## Installation

The installation only makes sense if you want to use the GUI script. For a 
simple plugin usage, the `hatchling` build backend will automatically install
the plugin.

```console
pip install hatch-pyside
```

## Usage

### Plugin

You only have to declare the plugin as a build dependency, and configure it
to declare the directories that contain the Qt source files to compile.

If they contain a configured `.pyproject` file you are done:

```toml
[build-system]
requires = ["hatchling", "hatch-pyside"]
build-backend = "hatchling.build"
#...
# Declare the source folder(s) to the pyside plugin
[tool.hatch.build.targets.wheel.hooks.pyside]
folders = ["src/foo"]
```

### GUI

If you install the package in your environment, you will gain access to the
`pyside-builder` GUI tool. It uses the plugin configuration to know what are the
directories of interest, and allow you to easily populate a `.pyproject` file

### Developer

If you want to modify `hatch-pyside`, you can either grab the source package
from PyPI, or better clone the GitHub repository:

```commandline
git clone https://github.com/s-ball/hatch-pyside.git
```

## Compatibility

`hatch-pyside` works fine with `PySide6` in versions 6.8.x . In the new 6.9,
`pyside6-project` has a dependency on `tomlkit` which is not correctly 
handled by the `pip` dependencies machinery. For that reason, the current 
version of `hatch-pyside` requires a version 6.8.x of `PySide6`.

## Contributing

I shall always be glad to receive issues or Pull Requests on GitHub. But as
I am the only maintainer, I cannot guarantee to react quickly to them. Please
feel free to contact me by mail if I do not answer quickly enough...

## License

`hatch-pyside` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
