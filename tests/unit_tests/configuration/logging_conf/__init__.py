import unittest

from unit_tests.configuration.logging_conf.logging_configuration_tests import LogConfTests


logConfSuite = unittest.TestSuite()
logConfSuite.addTest(unittest.makeSuite(LogConfTests))


__all__ = 'logConfSuite'
