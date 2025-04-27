#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
"""The main GUI file"""
from typing import Optional

from PySide6.QtWidgets import QApplication, QMessageBox, QDialog

from hatch_pyside import config
from hatch_pyside.gui.mainwindow import MainWindow
from hatch_pyside.gui.ui_project_chooser_dlg import Ui_ProjectChooser


def main():
    """Starts the Qt application"""
    app = QApplication()
    try:
        name, projects = config.get_project_folders()
    except OSError:
        QMessageBox(
            QMessageBox.Icon.Critical,
            "Fatal",
            "No pyproject.toml file found",
            informativeText="The current working directory must "
            "contain a pyproject.toml file",
        ).exec()
        return 2
    except KeyError:
        QMessageBox(
            QMessageBox.Icon.Critical,
            "Fatal",
            "pyproject.toml has no project name",
            informativeText="The pyproject.toml file must "
            "at least contain [project] name=...",
        ).exec()
        return 2
    if projects is None or len(projects) == 0:
        QMessageBox(
            QMessageBox.Icon.Critical,
            "Fatal",
            "No hatch-pyside configuration found",
            informativeText="hatch-pyside plugin must be configured in "
            "pyproject.toml or hatch.toml",
        ).exec()
        return 1

    folder = choose_project(projects)
    if folder is None:  # User pressed the cancel button
        return 0

    main_wnd = MainWindow(projects, folder, name)
    main_wnd.show()

    return app.exec()


def choose_project(projects: list[str]) -> Optional[str]:
    """
    Returns a Qt project folder.

    projects should not be empty. If it contains more than one file,
    displays a QDialog to allow the user to choose one of them.

    Args:
        projects: the list of the configured folders for the plugin

    Returns:
        the project if there is only one, or the chosen project
    """
    if len(projects) == 1:
        return projects[0]
    dlg = DialogChooser(projects)
    if dlg.exec() == 0:
        return None
    return dlg.projectList.selectedItems()[0].text()


class DialogChooser(QDialog, Ui_ProjectChooser):
    """A QDialog to choose a project folder from"""

    def __init__(self, projects):
        super().__init__()
        self.setupUi(self)
        self.projectList.addItems(projects)
        self.projectList.setCurrentRow(0)


# not really useful here, but required by pyside6-project
if __name__ == "__main__":
    main()
