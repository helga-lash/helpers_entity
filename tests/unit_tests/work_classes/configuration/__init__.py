import unittest

from unit_tests.work_classes.configuration.minio import minioConfSuite
from unit_tests.work_classes.configuration.app import workClassesConfigurationAppSuite


workClassesConfigurationSuite = unittest.TestSuite()
workClassesConfigurationSuite.addTest(minioConfSuite)
workClassesConfigurationSuite.addTest(workClassesConfigurationAppSuite)


__all__ = 'workClassesConfigurationSuite'
