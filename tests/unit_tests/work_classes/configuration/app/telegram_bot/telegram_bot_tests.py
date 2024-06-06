from unittest import IsolatedAsyncioTestCase
from pathlib import Path
from datetime import time

from helpers.work_classes import TgBotConf


class TestTgBotConf(IsolatedAsyncioTestCase):

    async def test_tg_bot_conf_record_time_correctly_encoded(self):
        record_time_list = [time(10, 0), time(15, 30)]
        tg_bot_conf = TgBotConf(token="test_token", recordTime=record_time_list)
        self.assertEqual(tg_bot_conf.to_json(), '{"token": "test_token", "recordTime": ["10:00:00", "15:30:00"],'
                                                ' "admins": null, "recordMonth": 2, "photoPath": "/tmp"}')

    async def test_tg_bot_conf_record_time_when_admins(self):
        # Test case 4: Check that recordTime is correctly encoded when admins are provided
        record_time_list = [time(10, 0), time(15, 30)]
        tg_bot_conf = TgBotConf(token="test_token", recordTime=record_time_list, admins=["admin1", "admin2"])
        self.assertEqual(tg_bot_conf.to_json(), '{"token": "test_token", "recordTime": ["10:00:00", "15:30:00"],'
                                                ' "admins": ["admin1", "admin2"], "recordMonth": 2, '
                                                '"photoPath": "/tmp"}')

    async def test_tg_bot_conf_record_time_when_photoPath(self):
        # Test case 5: Check that recordTime is correctly encoded when photoPath is provided
        record_time_list = [time(10, 0), time(15, 30)]
        tg_bot_conf = TgBotConf(token="test_token", recordTime=record_time_list, photoPath=Path("/custom/path"))
        self.assertEqual(tg_bot_conf.to_json(), '{"token": "test_token", "recordTime": ["10:00:00", "15:30:00"],'
                                                ' "admins": null, "recordMonth": 2, "photoPath": "/custom/path"}')


__all__ = 'TestTgBotConf'
