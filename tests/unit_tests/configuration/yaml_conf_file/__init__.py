import unittest

from unit_tests.configuration.yaml_conf_file.read_yaml_conf_tests import ReadYamlConfTests


yamlConfFileSuite = unittest.TestSuite()
yamlConfFileSuite.addTest(unittest.makeSuite(ReadYamlConfTests))


__all__ = 'yamlConfFileSuite'
