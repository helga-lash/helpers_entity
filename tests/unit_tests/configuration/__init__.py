import unittest

from unit_tests.configuration.yaml_conf_file import yamlConfFileSuite
from unit_tests.configuration.logging_conf import logConfSuite
from unit_tests.configuration.postgresql_conf import pgConfSuite
from unit_tests.configuration.app_conf import appConfSuite

configurationSuite = unittest.TestSuite()
configurationSuite.addTest(yamlConfFileSuite)
configurationSuite.addTest(logConfSuite)
configurationSuite.addTest(pgConfSuite)
configurationSuite.addTest(appConfSuite)


__all__ = 'configurationSuite'
