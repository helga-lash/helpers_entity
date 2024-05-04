import unittest

from unit_tests.configuration.app_conf.app_configuration_tests import AppConfTests
from unit_tests.configuration.app_conf.tg_bot_conf import tgBotConfSuite


appConfSuite = unittest.TestSuite()
appConfSuite.addTest(unittest.makeSuite(AppConfTests))
appConfSuite.addTest(tgBotConfSuite)


__all__ = 'appConfSuite'
