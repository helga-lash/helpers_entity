import unittest

from unit_tests.configuration.app_conf.tg_bot_conf.tg_bot_configuration_tests import TgBotConfTests


tgBotConfSuite = unittest.TestSuite()
tgBotConfSuite.addTest(unittest.makeSuite(TgBotConfTests))


__all__ = 'tgBotConfSuite'
