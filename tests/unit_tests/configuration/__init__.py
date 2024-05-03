import unittest

from unit_tests.configuration.yaml_conf_file import yamlConfFileSuite
from unit_tests.configuration.logging_conf import logConfSuite
from unit_tests.configuration.postgresql_conf import pgConfSuite

configurationSuite = unittest.TestSuite()
configurationSuite.addTest(yamlConfFileSuite)
configurationSuite.addTest(logConfSuite)
configurationSuite.addTest(pgConfSuite)


__all__ = 'configurationSuite'
