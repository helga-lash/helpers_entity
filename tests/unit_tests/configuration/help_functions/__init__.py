import unittest

from unit_tests.configuration.help_functions.positive_integer_func_tests import PositiveIntCheckTests


helpFunctionsSuite = unittest.TestSuite()
helpFunctionsSuite.addTest(unittest.makeSuite(PositiveIntCheckTests))


__all__ = 'helpFunctionsSuite'
