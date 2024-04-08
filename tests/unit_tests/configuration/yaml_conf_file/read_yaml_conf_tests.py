import os
import json

from pathlib import Path

from unittest import IsolatedAsyncioTestCase

from helpers.configuration.yaml_conf_file import read_yaml_conf
from helpers.work_classes import ReturnEntity


class ReadYamlConfTests(IsolatedAsyncioTestCase):
    """
    Class describing tests for helpers.configuration.yaml_conf_file.read_yaml_conf
    """

    async def test_path_not_exists(self):
        result: ReturnEntity = read_yaml_conf(Path('/configurations/hur-dur.yaml'))
        self.assertTrue(result.error)
        print(result.errorText)
        self.assertEqual('Configuration file /configurations/hur-dur.yaml is missing', result.errorText)
        self.assertEqual(None, result.entity)

    async def test_file_not_exists(self):
        os.mkdir(Path('/configurations'))
        result: ReturnEntity = read_yaml_conf(Path('/configurations/hur-dur.yaml'))
        os.rmdir(Path('/configurations'))
        self.assertTrue(result.error)
        print(result.errorText)
        self.assertEqual('Configuration file /configurations/hur-dur.yaml is missing', result.errorText)
        self.assertEqual(None, result.entity)

    async def test_read(self):
        result: ReturnEntity = read_yaml_conf()
        self.assertFalse(result.error)
        print(json.dumps(result.entity, indent=4, sort_keys=True))
        self.assertEqual(None, result.errorText)
        self.assertTrue(type(result.entity) is dict)
