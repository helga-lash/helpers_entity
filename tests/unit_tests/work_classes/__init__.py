import unittest

from unit_tests.work_classes.configuration import workClassesConfigurationSuite


workClassesSuite = unittest.TestSuite()
workClassesSuite.addTest(workClassesConfigurationSuite)


__all__ = 'workClassesSuite'
