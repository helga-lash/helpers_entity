import unittest

from unit_tests.configuration.yaml_conf_file import yamlConfFileSuite
from unit_tests.configuration.logging_conf import logConfSuite

configurationSuite = unittest.TestSuite()
configurationSuite.addTest(yamlConfFileSuite)
configurationSuite.addTest(logConfSuite)


__all__ = 'configurationSuite'
