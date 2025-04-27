#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import os
import pathlib
import shutil
import tempfile

try:
    # noinspection PyUnresolvedReferences
    import tomllib
    patch_str = 'tomllib.load'
except ImportError:
    # noinspection PyUnresolvedReferences
    import tomli as tomllib
    patch_str = 'tomli.load'
import unittest
from unittest.mock import patch

from hatch_pyside import config


class ConfigMockTest(unittest.TestCase):
    @patch('builtins.open')
    def test_no_project(self, op):
        """If pyproject.toml is not found: OSError"""
        op.side_effect = OSError
        with self.assertRaises(OSError):
            config.get_project_folders()

    @patch(patch_str)
    @patch('builtins.open')
    def test_no_config(self, _op, load):
        load.return_value = {'project': {'name': 'foo'}}
        _, lst = config.get_project_folders()
        self.assertIsNone(lst)

    @patch(patch_str)
    @patch('builtins.open')
    def test_hatch_global(self, _op, load):
        lst = ['src/foo']
        load.side_effect = [
            {'project': {'name': 'foo'}},
            {'build': {'hooks': {'pyside': {'folders': lst}}},
                     'project': {'name': 'foo'}}]
        self.assertIs(lst, config.get_project_folders()[1])

    @patch(patch_str)
    @patch('builtins.open')
    def test_hatch_wheel(self, _op, load):
        lst = ['src/foo']
        load.side_effect = [
            {'project': {'name': 'foo'}},
            {'build':
                 {'targets': {'wheel': {'hooks':{'pyside': {'folders': lst}}}}},
             'project': {'name': 'foo'}}
        ]
        self.assertIs(lst, config.get_project_folders()[1])


class ConfigTempTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.old_dir = os.getcwd()
        os.chdir(self.tempdir.name)
        self.data_path = pathlib.Path(__file__).parent / 'data'

    def tearDown(self):
        os.chdir(self.old_dir)
        self.tempdir.cleanup()

    def test_hatch(self):
        shutil.copy(self.data_path / 'pyproject.empty', 'pyproject.toml')
        shutil.copy(self.data_path / 'hatch.wheel', 'hatch.toml')
        self.assertEqual([ 'src/bar'], config.get_project_folders()[1])

    def test_pyproj(self):
        shutil.copy(self.data_path / 'pyproject.toml', 'pyproject.toml')
        self.assertEqual(['src/foo'], config.get_project_folders()[1])

    def test_no_proj(self):
        with self.assertRaises(OSError):
            config.get_project_folders()

    def test_no_config(self):
        shutil.copy(self.data_path / 'pyproject.empty', 'pyproject.toml')
        self.assertIsNone(config.get_project_folders()[1])

if __name__ == '__main__':
    unittest.main()
