import unittest

from unit_tests.configuration.postgresql_conf.pg_configuration_tests import PgConfTests


pgConfSuite = unittest.TestSuite()
pgConfSuite.addTest(unittest.makeSuite(PgConfTests))


__all__ = 'pgConfSuite'
