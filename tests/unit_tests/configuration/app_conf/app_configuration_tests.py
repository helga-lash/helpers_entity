import os
import json

from pathlib import Path

from unittest import IsolatedAsyncioTestCase
from datetime import time

from helpers.configuration.app_conf import app_conf
from helpers.work_classes import ReturnEntity
from helpers.work_classes import AppConf


class AppConfTests(IsolatedAsyncioTestCase):
    """
    Class describing tests for helpers.configuration.app_conf.app_conf
    """

    async def asyncSetUp(self):
        self.conf_path = Path('/conf/app-conf-test.yaml')
        with open(self.conf_path, 'w') as file:
            file.write('app:\n'
                       '  tgBot:\n'
                       '    token: 6870929386:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K\n'
                       '    recordTime:\n'
                       '      - "11:30:00"\n'
                       '      - "15"\n'
                       '      - "18:00"\n'
                       '    admins:\n'
                       '      - test-admin-1\n'
                       '      - test-admin-2\n'
                       '      - test-admin-3\n'
                       '      - test-admin-4\n'
                       '      - test-admin-5\n')

    async def asyncTearDown(self):
        os.remove(self.conf_path)

    async def test_read_from_file(self):
        result: ReturnEntity = app_conf(self.conf_path)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: AppConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('6870929386:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K', result_entity.tgBot.token)
        self.assertEqual(list, type(result_entity.tgBot.recordTime))
        self.assertIn(time(11, 30, 00), result_entity.tgBot.recordTime)
        self.assertIn(time(15), result_entity.tgBot.recordTime)
        self.assertIn(time(18, 00), result_entity.tgBot.recordTime)
        self.assertEqual(list, type(result_entity.tgBot.admins))
        self.assertIn('test-admin-1', result_entity.tgBot.admins)
        self.assertIn('test-admin-2', result_entity.tgBot.admins)
        self.assertIn('test-admin-3', result_entity.tgBot.admins)
        self.assertIn('test-admin-4', result_entity.tgBot.admins)
        self.assertIn('test-admin-5', result_entity.tgBot.admins)

    async def test_not_conf_file_not_env(self):
        result: ReturnEntity = app_conf(Path('/conf/app-conf.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Configuration file /conf/app-conf.yaml is missing', result.errorText)
        self.assertIn('Telegram bot token not configured', result.errorText)
