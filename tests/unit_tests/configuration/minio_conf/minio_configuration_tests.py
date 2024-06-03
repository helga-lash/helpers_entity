import json
import os

from unittest import IsolatedAsyncioTestCase
from pathlib import Path
from unittest.mock import patch

from helpers.work_classes import ReturnEntity
from helpers.configuration import minio_conf
from helpers.work_classes.configuration import MinioClientConf


class TestMinioConf(IsolatedAsyncioTestCase):
    """
    Test class for the minio_conf function.
    """

    async def asyncSetUp(self):
        self.path = Path('/conf/example.yaml')

    async def asyncTearDown(self):
        """
        Async method to clean up environment variables after each test case.
        """
        os.environ.pop('MN_HOST', None)
        os.environ.pop('MN_PORT', None)
        os.environ.pop('MN_SECURE', None)
        os.environ.pop('MN_ACCESS_KEY', None)
        os.environ.pop('MN_SECRET_KEY', None)

    @patch('helpers.configuration.minio_conf.minio_configuration.read_yaml_conf')
    async def test_minio_conf_valid_yaml(self, mock_read_yaml_conf):
        # Mock the read_yaml_conf function to return a valid configuration
        mock_read_yaml_conf.return_value = ReturnEntity(False, None, {
            'minio': {'host': 'example.com', 'port': '9000', 'secure': 'True', 'accessKey': 'minio',
                      'secretKey': 'minio123'}})

        # Call the minio_conf function with a valid path
        result = minio_conf(Path('path/to/config.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        else:
            print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        # Assert that the function returns the expected result
        self.assertFalse(result.error)
        self.assertIsInstance(result.entity, MinioClientConf)
        self.assertEqual(result.entity.host, 'example.com')
        self.assertEqual(result.entity.port, 9000)
        self.assertTrue(result.entity.secure)
        self.assertEqual(result.entity.accessKey, 'minio')
        self.assertEqual(result.entity.secretKey, 'minio123')

    @patch('helpers.configuration.minio_conf.minio_configuration.read_yaml_conf')
    async def test_minio_conf_invalid_yaml(self, mock_read_yaml_conf):
        # Mock the read_yaml_conf function to return an invalid configuration
        mock_read_yaml_conf.return_value = ReturnEntity(True, 'Error reading YAML configuration', {})

        # Call the minio_conf function with a valid path
        result = minio_conf(Path('path/to/config.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        else:
            print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        # Assert that the function returns the expected result
        self.assertTrue(result.error)
        self.assertIn('Error reading YAML configuration', result.errorText)
        self.assertEqual(result.entity, {})

    @patch('helpers.configuration.minio_conf.minio_configuration.read_yaml_conf')
    async def test_minio_conf_environment_variables(self, mock_read_yaml_conf):
        # Mock the read_yaml_conf function to return an empty configuration
        mock_read_yaml_conf.return_value = (ReturnEntity(False, None, {}))

        # Set environment variables
        os.environ['MN_HOST'] = 'example.com'
        os.environ['MN_PORT'] = '9000'
        os.environ['MN_SECURE'] = 'True'
        os.environ['MN_ACCESS_KEY'] = 'minio'
        os.environ['MN_SECRET_KEY'] = 'minio123'

        # Call the minio_conf function without a path
        result = minio_conf()
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        else:
            print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        # Assert that the function returns the expected result
        self.assertFalse(result.error)
        self.assertIsInstance(result.entity, MinioClientConf)
        self.assertEqual(result.entity.host, 'example.com')
        self.assertEqual(result.entity.port, 9000)
        self.assertTrue(result.entity.secure)
        self.assertEqual(result.entity.accessKey, 'minio')
        self.assertEqual(result.entity.secretKey, 'minio123')

    @patch('helpers.configuration.minio_conf.minio_configuration.read_yaml_conf')
    async def test_minio_conf_missing_port_config(self, mock_read_yaml_conf):
        # Mock the read_yaml_conf function to return a configuration with missing required fields
        mock_read_yaml_conf.return_value = ReturnEntity(False, None, {
            'minio': {'host': 'example.com', 'secure': 'True', 'accessKey': 'minio', 'secretKey': 'minio123'}})

        # Call the minio_conf function with a valid path
        result = minio_conf(Path('path/to/config.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        else:
            print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        # Assert that the function returns the expected result
        self.assertFalse(result.error)
        self.assertIsInstance(result.entity, MinioClientConf)
        self.assertEqual(result.entity.host, 'example.com')
        self.assertEqual(result.entity.port, 443)
        self.assertTrue(result.entity.secure)
        self.assertEqual(result.entity.accessKey, 'minio')
        self.assertEqual(result.entity.secretKey, 'minio123')

    @patch('helpers.configuration.minio_conf.minio_configuration.read_yaml_conf')
    async def test_minio_conf_invalid_port(self, mock_read_yaml_conf):
        # Mock the read_yaml_conf function to return a configuration with an invalid port number
        mock_read_yaml_conf.return_value = ReturnEntity(False, None, {
            'minio': {'host': 'example.com', 'port': 'abc', 'secure': 'True', 'accessKey': 'minio',
                      'secretKey': 'minio123'}})

        # Call the minio_conf function with a valid path
        result = minio_conf(Path('path/to/config.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        else:
            print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        # Assert that the function returns the expected result
        self.assertTrue(result.error)
        self.assertEqual(result.errorText, 'The minio port must be a positive integer')
        self.assertDictEqual(result.entity, {'host': 'example.com', 'port': 'abc', 'secure': 'True',
                                             'accessKey': 'minio', 'secretKey': 'minio123'})

    @patch('helpers.configuration.minio_conf.minio_configuration.read_yaml_conf')
    async def test_minio_conf_not_host(self, mock_read_yaml_conf):
        # Mock the read_yaml_conf function to return a configuration with an invalid port number
        mock_read_yaml_conf.return_value = ReturnEntity(False, None, {
            'minio': {'port': '9000', 'secure': 'True', 'accessKey': 'minio',
                      'secretKey': 'minio123'}})

        # Call the minio_conf function with a valid path
        result = minio_conf(Path('path/to/config.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        else:
            print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        # Assert that the function returns the expected result
        self.assertTrue(result.error)
        self.assertEqual(result.errorText, 'Minio host not configured')

    @patch('helpers.configuration.minio_conf.minio_configuration.read_yaml_conf')
    async def test_minio_conf_not_accessKey(self, mock_read_yaml_conf):
        # Mock the read_yaml_conf function to return a configuration with an invalid port number
        mock_read_yaml_conf.return_value = ReturnEntity(False, None, {
            'minio': {'host': 'example.com', 'port': '9000', 'secure': 'True',
                      'secretKey': 'minio123'}})

        # Call the minio_conf function with a valid path
        result = minio_conf(Path('path/to/config.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        else:
            print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        # Assert that the function returns the expected result
        self.assertTrue(result.error)
        self.assertEqual(result.errorText, 'Minio access key not configured')

    @patch('helpers.configuration.minio_conf.minio_configuration.read_yaml_conf')
    async def test_minio_conf_not_secretKey(self, mock_read_yaml_conf):
        # Mock the read_yaml_conf function to return a configuration with an invalid port number
        mock_read_yaml_conf.return_value = ReturnEntity(False, None, {
            'minio': {'host': 'example.com', 'port': '9000', 'secure': 'True', 'accessKey': 'minio'}})

        # Call the minio_conf function with a valid path
        result = minio_conf(Path('path/to/config.yaml'))
        if result.error:
            for error in result.errorText.split('|'):
                print(error)
        else:
            print(json.dumps(result.entity.to_dict(), indent=4, sort_keys=True))
        # Assert that the function returns the expected result
        self.assertTrue(result.error)
        self.assertEqual(result.errorText, 'Minio secret key not configured')
