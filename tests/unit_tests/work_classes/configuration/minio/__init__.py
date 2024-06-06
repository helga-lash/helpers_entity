import unittest

from unit_tests.work_classes.configuration.minio.minio_conf_tests import TestMinioClientConf


minioConfSuite = unittest.TestSuite()
minioConfSuite.addTest(unittest.makeSuite(TestMinioClientConf))


__all__ = 'minioConfSuite'
