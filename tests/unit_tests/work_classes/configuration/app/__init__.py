import unittest

from unit_tests.work_classes.configuration.app.app_conf_tests import TestAppConf
from unit_tests.work_classes.configuration.app.telegram_bot import workClassesConfigurationAppTgBotSuite


workClassesConfigurationAppSuite = unittest.TestSuite()
workClassesConfigurationAppSuite.addTest(unittest.makeSuite(TestAppConf))
workClassesConfigurationAppSuite.addTest(workClassesConfigurationAppTgBotSuite)


__all__ = 'workClassesConfigurationAppSuite'
