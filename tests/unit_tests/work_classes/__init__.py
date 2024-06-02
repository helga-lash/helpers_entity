import unittest

from unit_tests.work_classes.minio import minioConfSuite


workClassesSuite = unittest.TestSuite()
workClassesSuite.addTest(minioConfSuite)


__all__ = 'workClassesSuite'
