from unittest import IsolatedAsyncioTestCase

from helpers.configuration.help_functions import positive_int_check


class PositiveIntCheckTests(IsolatedAsyncioTestCase):
    """
    Class describing tests for helpers.configuration.help_functions.positive_int_check
    """

    async def test_positive_int(self):
        verifiable: int = 5
        result: bool = positive_int_check(verifiable)
        print(f'{verifiable} - {result}')
        self.assertTrue(result)

    async def test_positive_int_in_str(self):
        verifiable: str = '10'
        result: bool = positive_int_check(verifiable)
        print(f'{verifiable} - {result}')
        self.assertTrue(result)

    async def test_float(self):
        verifiable: float = 5.1235
        result: bool = positive_int_check(verifiable)
        print(f'{verifiable} - {result}')
        self.assertFalse(result)

    async def test_float_in_str(self):
        verifiable: str = '58.983654'
        result: bool = positive_int_check(verifiable)
        print(f'{verifiable} - {result}')
        self.assertFalse(result)

    async def test_bool_true(self):
        verifiable: bool = True
        result: bool = positive_int_check(verifiable)
        print(f'{verifiable} - {result}')
        self.assertFalse(result)

    async def test_bool_true_in_str(self):
        verifiable: str = 'true'
        result: bool = positive_int_check(verifiable)
        print(f'{verifiable} - {result}')
        self.assertFalse(result)

    async def test_bool_false(self):
        verifiable: bool = False
        result: bool = positive_int_check(verifiable)
        print(f'{verifiable} - {result}')
        self.assertFalse(result)

    async def test_bool_false_str(self):
        verifiable: str = 'False'
        result: bool = positive_int_check(verifiable)
        print(f'{verifiable} - {result}')
        self.assertFalse(result)
