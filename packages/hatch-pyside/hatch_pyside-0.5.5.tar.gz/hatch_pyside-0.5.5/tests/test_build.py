#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.old_dir = os.getcwd()
        os.chdir(self.tempdir.name)
        self.data_path = pathlib.Path(__file__).parent / 'data'

    def tearDown(self):
        os.chdir(self.old_dir)
        self.tempdir.cleanup()

    def test_build(self):
        shutil.copy(self.data_path / 'pyproject.toml', '.')
        shutil.copytree(self.data_path / 'src', 'src')
        os.mkdir('dist')
        cr = subprocess.run(['pip', 'wheel', '-w', 'dist', self.data_path.parent.parent],
                            capture_output=True)
        self.assertEqual(0, cr.returncode)
        cr = subprocess.run(['pip', 'install', '.', '-f', 'dist'])
        self.assertEqual(0, cr.returncode)
        try:
            import foo.ui_MainWindow
        finally:
            subprocess.run(['pip', 'uninstall', '-y', 'foo'])


if __name__ == "__main__":
    unittest.main()
