import unittest

from unit_tests.configuration.minio_conf.minio_configuration_tests import TestMinioConf


minioConfSuite = unittest.TestSuite()
minioConfSuite.addTest(unittest.makeSuite(TestMinioConf))


__all__ = 'minioConfSuite'