import unittest

from unit_tests.configuration.yaml_conf_file import yamlConfFileSuite

configurationSuite = unittest.TestSuite()
configurationSuite.addTest(yamlConfFileSuite)


__all__ = 'configurationSuite'
