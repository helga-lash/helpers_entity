import os
import json

from unittest import IsolatedAsyncioTestCase
from datetime import time
from pathlib import Path

from helpers.configuration.app_conf.tg_bot_conf import tg_bot_conf
from helpers.work_classes import ReturnEntity
from helpers.work_classes import TgBotConf


class TgBotConfTests(IsolatedAsyncioTestCase):
    """
    Class describing tests for helpers.configuration.app_conf.tg_bot_conf.tg_bot_conf
    """

    async def asyncSetUp(self):
        self.tg_conf_dict = dict(
            token='6870929386:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K',
            recordTime=['11:30:00', '15', '18:12'],
            admins=['test-admin-1', 'test-admin-2', 'test-admin-3', 'test-admin-4', 'test-admin-5'],
            recordMonth=3,
            photoPath='/conf/photo'
        )

    async def asyncTearDown(self):
        os.environ.pop('TG_TOKEN', None)
        os.environ.pop('TG_RD_TM', None)
        os.environ.pop('TG_ADMINS', None)
        os.environ.pop('TG_RD_MT', None)
        os.environ.pop('TG_PHOTO_PATH', None)

    async def test_read_from_dict(self):
        result: ReturnEntity = tg_bot_conf(self.tg_conf_dict)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: TgBotConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('6870929386:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K', result_entity.token)
        self.assertEqual(list, type(result_entity.recordTime))
        self.assertIn(time(11, 30), result_entity.recordTime)
        self.assertIn(time(15), result_entity.recordTime)
        self.assertIn(time(18, 12), result_entity.recordTime)
        self.assertEqual(list, type(result_entity.admins))
        self.assertIn('test-admin-1', result_entity.admins)
        self.assertIn('test-admin-2', result_entity.admins)
        self.assertIn('test-admin-3', result_entity.admins)
        self.assertIn('test-admin-4', result_entity.admins)
        self.assertIn('test-admin-5', result_entity.admins)
        self.assertEqual(3, result_entity.recordMonth)
        self.assertEqual(Path('/conf/photo'), result_entity.photoPath)

    async def test_not_dict_not_env(self):
        result: ReturnEntity = tg_bot_conf()
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Telegram bot token not configured', result.errorText)

    async def test_env_var(self):
        os.environ['TG_TOKEN'] = '7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K'
        os.environ['TG_RD_TM'] = '8, 12:52, 15:21:35'
        os.environ['TG_ADMINS'] = 'test-admin-6, test-admin-7, test-admin-8'
        os.environ['TG_RD_MT'] = '5'
        os.environ['TG_PHOTO_PATH'] = '/tmp/photo'
        result: ReturnEntity = tg_bot_conf(self.tg_conf_dict)
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: TgBotConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K', result_entity.token)
        self.assertEqual(list, type(result_entity.recordTime))
        self.assertIn(time(8), result_entity.recordTime)
        self.assertIn(time(12, 52), result_entity.recordTime)
        self.assertIn(time(15, 21, 35), result_entity.recordTime)
        self.assertEqual(list, type(result_entity.admins))
        self.assertIn('test-admin-6', result_entity.admins)
        self.assertIn('test-admin-7', result_entity.admins)
        self.assertIn('test-admin-8', result_entity.admins)
        self.assertEqual(5, result_entity.recordMonth)
        self.assertEqual(Path('/tmp/photo'), result_entity.photoPath)

    async def test_not_admins(self):
        os.environ['TG_TOKEN'] = '7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K'
        os.environ['TG_RD_TM'] = '8, 12:52, 15:21:35'
        os.environ['TG_RD_MT'] = '5'
        os.environ['TG_PHOTO_PATH'] = '/tmp/photo'
        result: ReturnEntity = tg_bot_conf()
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: TgBotConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K', result_entity.token)
        self.assertEqual(list, type(result_entity.recordTime))
        self.assertIn(time(8), result_entity.recordTime)
        self.assertIn(time(12, 52), result_entity.recordTime)
        self.assertIn(time(15, 21, 35), result_entity.recordTime)
        self.assertEqual(None, result_entity.admins)
        self.assertEqual(5, result_entity.recordMonth)
        self.assertEqual(Path('/tmp/photo'), result_entity.photoPath)

    async def test_not_token(self):
        os.environ['TG_RD_TM'] = '8, 12:52, 15:21:35'
        os.environ['TG_ADMINS'] = 'test-admin-6, test-admin-7, test-admin-8'
        os.environ['TG_RD_MT'] = '5'
        os.environ['TG_PHOTO_PATH'] = '/tmp/photo'
        result: ReturnEntity = tg_bot_conf()
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('Telegram bot token not configured', result.errorText)

    async def test_not_recordTime(self):
        os.environ['TG_TOKEN'] = '7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K'
        os.environ['TG_ADMINS'] = 'test-admin-6, test-admin-7, test-admin-8'
        os.environ['TG_RD_MT'] = '5'
        os.environ['TG_PHOTO_PATH'] = '/tmp/photo'
        result: ReturnEntity = tg_bot_conf()
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertTrue(result.error)
        self.assertIn('The telegram recording time list not configured', result.errorText)

    async def test_not_recordMonth(self):
        os.environ['TG_TOKEN'] = '7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K'
        os.environ['TG_RD_TM'] = '8, 12:52, 15:21:35'
        os.environ['TG_ADMINS'] = 'test-admin-6, test-admin-7, test-admin-8'
        os.environ['TG_PHOTO_PATH'] = '/tmp/photo'
        result: ReturnEntity = tg_bot_conf()
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: TgBotConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K', result_entity.token)
        self.assertEqual(list, type(result_entity.recordTime))
        self.assertIn(time(8), result_entity.recordTime)
        self.assertIn(time(12, 52), result_entity.recordTime)
        self.assertIn(time(15, 21, 35), result_entity.recordTime)
        self.assertEqual(list, type(result_entity.admins))
        self.assertIn('test-admin-6', result_entity.admins)
        self.assertIn('test-admin-7', result_entity.admins)
        self.assertIn('test-admin-8', result_entity.admins)
        self.assertEqual(2, result_entity.recordMonth)
        self.assertEqual(Path('/tmp/photo'), result_entity.photoPath)

    async def test_not_photoPath(self):
        os.environ['TG_TOKEN'] = '7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K'
        os.environ['TG_RD_TM'] = '8, 12:52, 15:21:35'
        os.environ['TG_ADMINS'] = 'test-admin-6, test-admin-7, test-admin-8'
        os.environ['TG_RD_MT'] = '3'
        result: ReturnEntity = tg_bot_conf()
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: TgBotConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K', result_entity.token)
        self.assertEqual(list, type(result_entity.recordTime))
        self.assertIn(time(8), result_entity.recordTime)
        self.assertIn(time(12, 52), result_entity.recordTime)
        self.assertIn(time(15, 21, 35), result_entity.recordTime)
        self.assertEqual(list, type(result_entity.admins))
        self.assertIn('test-admin-6', result_entity.admins)
        self.assertIn('test-admin-7', result_entity.admins)
        self.assertIn('test-admin-8', result_entity.admins)
        self.assertEqual(3, result_entity.recordMonth)
        self.assertEqual(Path('/tmp'), result_entity.photoPath)

    async def test_negative_recordMonth(self):
        os.environ['TG_TOKEN'] = '7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K'
        os.environ['TG_RD_TM'] = '8, 12:52, 15:21:35'
        os.environ['TG_ADMINS'] = 'test-admin-6, test-admin-7, test-admin-8'
        os.environ['TG_RD_MT'] = '-5'
        os.environ['TG_PHOTO_PATH'] = '/tmp/photo'
        result: ReturnEntity = tg_bot_conf()
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: TgBotConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K', result_entity.token)
        self.assertEqual(list, type(result_entity.recordTime))
        self.assertIn(time(8), result_entity.recordTime)
        self.assertIn(time(12, 52), result_entity.recordTime)
        self.assertIn(time(15, 21, 35), result_entity.recordTime)
        self.assertEqual(list, type(result_entity.admins))
        self.assertIn('test-admin-6', result_entity.admins)
        self.assertIn('test-admin-7', result_entity.admins)
        self.assertIn('test-admin-8', result_entity.admins)
        self.assertEqual(2, result_entity.recordMonth)
        self.assertEqual(Path('/tmp/photo'), result_entity.photoPath)

    async def test_bool_recordMonth(self):
        os.environ['TG_TOKEN'] = '7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K'
        os.environ['TG_RD_TM'] = '8, 12:52, 15:21:35'
        os.environ['TG_ADMINS'] = 'test-admin-6, test-admin-7, test-admin-8'
        os.environ['TG_RD_MT'] = 'true'
        os.environ['TG_PHOTO_PATH'] = '/tmp/photo'
        result: ReturnEntity = tg_bot_conf()
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        self.assertFalse(result.error)
        result_entity: TgBotConf = result.entity
        print(json.dumps(result_entity.to_dict(), indent=4, sort_keys=True))
        self.assertEqual('7981030497:AAGccloydrBobPuFvzjrMWYKkLpMRSzxy3K', result_entity.token)
        self.assertEqual(list, type(result_entity.recordTime))
        self.assertIn(time(8), result_entity.recordTime)
        self.assertIn(time(12, 52), result_entity.recordTime)
        self.assertIn(time(15, 21, 35), result_entity.recordTime)
        self.assertEqual(list, type(result_entity.admins))
        self.assertIn('test-admin-6', result_entity.admins)
        self.assertIn('test-admin-7', result_entity.admins)
        self.assertIn('test-admin-8', result_entity.admins)
        self.assertEqual(2, result_entity.recordMonth)
        self.assertEqual(Path('/tmp/photo'), result_entity.photoPath)
