import unittest

from unit_tests.work_classes.configuration.app.telegram_bot.telegram_bot_tests import TestTgBotConf


workClassesConfigurationAppTgBotSuite = unittest.TestSuite()
workClassesConfigurationAppTgBotSuite.addTest(unittest.makeSuite(TestTgBotConf))


__all__ = 'workClassesConfigurationAppTgBotSuite'
