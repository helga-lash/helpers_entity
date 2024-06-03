import unittest

from unit_tests.configuration.yaml_conf_file import yamlConfFileSuite
from unit_tests.configuration.logging_conf import logConfSuite
from unit_tests.configuration.postgresql_conf import pgConfSuite
from unit_tests.configuration.app_conf import appConfSuite
from unit_tests.configuration.help_functions import helpFunctionsSuite
from unit_tests.configuration.minio_conf import minioConfSuite

configurationSuite = unittest.TestSuite()
configurationSuite.addTest(yamlConfFileSuite)
configurationSuite.addTest(logConfSuite)
configurationSuite.addTest(pgConfSuite)
configurationSuite.addTest(appConfSuite)
configurationSuite.addTest(helpFunctionsSuite)
configurationSuite.addTest(minioConfSuite)


__all__ = 'configurationSuite'
