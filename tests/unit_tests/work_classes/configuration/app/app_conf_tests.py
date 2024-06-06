from unittest import IsolatedAsyncioTestCase
from dataclasses import asdict
from datetime import time
from pathlib import PosixPath

from helpers.work_classes.configuration import AppConf, TgBotConf


class TestAppConf(IsolatedAsyncioTestCase):

    async def test_default_initialization(self):
        app_conf = AppConf()
        self.assertIsNone(app_conf.tgBot)

    async def test_initialization_with_tgBot(self):
        tg_bot_conf = TgBotConf(token="test_token", recordTime=[time(11, 15), time(18, 5)])
        app_conf = AppConf(tgBot=tg_bot_conf)
        self.assertEqual(app_conf.tgBot, tg_bot_conf)

    async def test_json_serialization(self):
        tg_bot_conf = TgBotConf(token="test_token", recordTime=[time(11, 15), time(18, 5)])
        app_conf = AppConf(tgBot=tg_bot_conf)
        json_str = app_conf.to_json()
        expected_json_str = ('{"tgBot": {"token": "test_token", "recordTime": ["11:15:00", "18:05:00"], "admins": null,'
                             ' "recordMonth": 2, "photoPath": "/tmp"}}')
        self.assertEqual(json_str, expected_json_str)

    async def test_json_deserialization(self):
        json_str = '{"tgBot": {"token": "test_token", "recordTime": ["11:15:00", "18:05:00"]}}'
        app_conf = AppConf.from_json(json_str)
        tg_bot_conf = TgBotConf(token="test_token", recordTime=[time(11, 15), time(18, 5)])
        self.assertDictEqual(app_conf.tgBot.to_dict(), tg_bot_conf.to_dict())

    async def test_asdict(self):
        tg_bot_conf = TgBotConf(token="test_token", recordTime=[time(11, 15), time(18, 5)])
        app_conf = AppConf(tgBot=tg_bot_conf)
        expected_dict = {'tgBot': {'admins': None,
                                   'photoPath': PosixPath('/tmp'),
                                   'recordMonth': 2,
                                   'recordTime': [time(11, 15), time(18, 5)],
                                   'token': 'test_token'}}
        self.assertDictEqual(asdict(app_conf), expected_dict)


__all__ = 'TestAppConf'
