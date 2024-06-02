import json

from unittest import IsolatedAsyncioTestCase

from helpers.work_classes.configuration import MinioClientConf


class TestMinioClientConf(IsolatedAsyncioTestCase):
    async def test_minio_client_with_special_characters(self):
        # Test with special characters in host, access_key, and secret_key
        host = 'minio-server.example.com'
        access_key = 'special@key'
        secret_key = 'special#key'
        port = 9000
        region = 'us-west-2'
        secure = True

        minio_client = MinioClientConf(host, access_key, secret_key, port, region, secure)
        print(json.dumps(minio_client.to_dict(), indent=4, sort_keys=True))

        self.assertEqual(minio_client.host, host)
        self.assertEqual(minio_client.accessKey, access_key)
        self.assertEqual(minio_client.secretKey, secret_key)
        self.assertEqual(minio_client.port, port)
        self.assertEqual(minio_client.region, region)
        self.assertEqual(minio_client.secure, secure)

    async def test_minio_client_with_default_values(self):
        # Test with default values
        host = 'localhost'
        access_key = 'accessKey123'
        secret_key = 'secretKey123'

        minio_client = MinioClientConf(host, access_key, secret_key)
        print(json.dumps(minio_client.to_dict(), indent=4, sort_keys=True))

        self.assertEqual(minio_client.host, host)
        self.assertEqual(minio_client.accessKey, access_key)
        self.assertEqual(minio_client.secretKey, secret_key)
        self.assertIsNone(minio_client.port)
        self.assertEqual(minio_client.region, 'us-east-1')
        self.assertFalse(minio_client.secure)

    async def test_minio_client_with_empty_host(self):
        # Test with empty host
        with self.assertRaises(TypeError) as error:
            MinioClientConf(
                accessKey='accessKey123',
                secretKey='secretKey123'
            )
        print(error.exception)

    async def test_minio_client_with_empty_access_key(self):
        # Test with empty accessKey
        with self.assertRaises(TypeError) as error:
            MinioClientConf(
                host='localhost',
                secretKey='secretKey123'
            )
        print(error.exception)

    async def test_minio_client_with_empty_secret_key(self):
        # Test with empty secretKey
        with self.assertRaises(TypeError) as error:
            MinioClientConf(
                host='localhost',
                accessKey='accessKey123'
            )
        print(error.exception)
