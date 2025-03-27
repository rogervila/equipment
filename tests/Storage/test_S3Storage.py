import unittest
from unittest.mock import MagicMock
import boto3
import botocore
import botocore.exceptions
from moto import mock_aws
from equipment.Storage.S3Storage import S3Storage


class TestS3Storage(unittest.TestCase):
    def setUp(self):
        # Start the moto S3 mock
        self.mock_s3 = mock_aws()
        self.mock_s3.start()

        # Create a mock logger
        self.mock_logger = MagicMock()

        # Create test config
        self.config = {
            'endpoint': None,  # Use default AWS endpoint for moto
            'access_key': 'test_access_key',
            'secret_key': 'test_secret_key',
            'region': 'us-east-1',
            'bucket': 'test-bucket',
            'prefix': 'test-prefix'
        }

        # Create the S3 bucket
        self.s3_client = boto3.client(
            's3',
            region_name=self.config['region'],
            aws_access_key_id=self.config['access_key'],
            aws_secret_access_key=self.config['secret_key']
        )
        self.s3_client.create_bucket(Bucket=self.config['bucket'])

        # Create S3Storage instance
        self.storage = S3Storage(self.config, self.mock_logger)
        self.storage.s3 = self.s3_client

    def tearDown(self):
        # Stop the moto mock
        self.mock_s3.stop()

    def test_path(self):
        # Test path generation without trailing slash in prefix
        self.assertEqual(self.storage.path('test.txt'), 'test-prefix/test.txt')

        # Test path generation with trailing slash in prefix
        self.storage.config['prefix'] = 'test-prefix/'
        self.assertEqual(self.storage.path('test.txt'), 'test-prefix/test.txt')

        # Test with empty prefix
        self.storage.config['prefix'] = ''
        self.assertEqual(self.storage.path('test.txt'), 'test.txt')

        # Test with None prefix
        self.storage.config['prefix'] = None
        self.assertEqual(self.storage.path('test.txt'), 'test.txt')

    def test_write(self):
        # Test writing a file
        result = self.storage.write('test.txt', 'test content')
        self.assertTrue(result)

        # Verify file was written
        response = self.s3_client.get_object(
            Bucket=self.config['bucket'],
            Key='test-prefix/test.txt'
        )
        content = response['Body'].read().decode('utf-8')
        self.assertEqual(content, 'test content')

        # Test write with exception
        self.storage.client = MagicMock(
            side_effect=Exception("Test exception"))
        result = self.storage.write('fail.txt', 'test content')
        self.assertFalse(result)
        self.mock_logger.error.assert_called()

    def test_read(self):
        # Create a test file
        self.s3_client.put_object(
            Bucket=self.config['bucket'],
            Key='test-prefix/test.txt',
            Body='test content'
        )

        # Test reading a file
        content = self.storage.read('test.txt')
        self.assertEqual(content, 'test content')

        # Test reading non-existent file
        with self.assertRaises(FileNotFoundError):
            self.storage.read('nonexistent.txt')

        # Test read with exception
        self.storage.client = MagicMock()
        self.storage.exists = MagicMock(return_value=True)
        self.storage.client.return_value.get_object.side_effect = Exception(
            "Test exception")
        with self.assertRaises(Exception):
            self.storage.read('error.txt')
        self.mock_logger.error.assert_called()

    def test_exists(self):
        # Create a test file
        self.s3_client.put_object(
            Bucket=self.config['bucket'],
            Key='test-prefix/test.txt',
            Body='test content'
        )

        # Test file exists
        self.assertTrue(self.storage.exists('test.txt'))

        # Test file does not exist
        self.assertFalse(self.storage.exists('nonexistent.txt'))

        # Test with client error (not 404)
        original_client = self.storage.client
        self.storage.client = MagicMock()
        error_response = {'Error': {'Code': '403'}}
        self.storage.client.return_value.head_object.side_effect = botocore.exceptions.ClientError(
            error_response, 'HeadObject')
        self.assertFalse(self.storage.exists('error.txt'))
        self.mock_logger.error.assert_called()

        # Test with generic exception
        self.storage.client.return_value.head_object.side_effect = Exception(
            "Test exception")
        self.assertFalse(self.storage.exists('error2.txt'))
        self.mock_logger.error.assert_called()

        # Restore original client
        self.storage.client = original_client

    def test_remove(self):
        # Create a test file
        self.s3_client.put_object(
            Bucket=self.config['bucket'],
            Key='test-prefix/test.txt',
            Body='test content'
        )

        # Test removing a file
        result = self.storage.remove('test.txt')
        self.assertTrue(result)

        # Verify file was removed
        self.assertFalse(self.storage.exists('test.txt'))

        # Test remove with exception
        self.storage.client = MagicMock()
        self.storage.client.return_value.delete_object.side_effect = Exception(
            "Test exception")
        result = self.storage.remove('error.txt')
        self.assertFalse(result)
        self.mock_logger.error.assert_called()

    def test_move(self):
        # Create a test file
        self.s3_client.put_object(
            Bucket=self.config['bucket'],
            Key='test-prefix/source.txt',
            Body='test content'
        )

        # Test moving a file
        result = self.storage.move('source.txt', 'destination.txt')
        self.assertTrue(result)

        # Verify source file was removed
        self.assertFalse(self.storage.exists('source.txt'))

        # Verify destination file exists with correct content
        self.assertTrue(self.storage.exists('destination.txt'))
        content = self.storage.read('destination.txt')
        self.assertEqual(content, 'test content')

        # Test move with exception
        self.storage.client = MagicMock()
        self.storage.client.return_value.copy_object.side_effect = Exception(
            "Test exception")
        result = self.storage.move('source.txt', 'error.txt')
        self.assertFalse(result)
        self.mock_logger.error.assert_called()

    def test_list(self):
        # Create test files
        self.s3_client.put_object(
            Bucket=self.config['bucket'],
            Key='test-prefix/folder/file1.txt',
            Body='content1'
        )
        self.s3_client.put_object(
            Bucket=self.config['bucket'],
            Key='test-prefix/folder/file2.txt',
            Body='content2'
        )
        self.s3_client.put_object(
            Bucket=self.config['bucket'],
            Key='test-prefix/folder/subfolder/',
            Body=''
        )

        # Test listing files in a directory
        files = self.storage.list('folder')
        self.assertIn('file1.txt', files)
        self.assertIn('file2.txt', files)
        self.assertEqual(len(files), 2)  # Should not include subdirectories

        # Test list with exception
        self.storage.client = MagicMock()
        self.storage.client.return_value.list_objects_v2.side_effect = Exception(
            "Test exception")
        with self.assertRaises(Exception):
            self.storage.list('error')
        self.mock_logger.error.assert_called()

    def test_client(self):
        # Test client initialization
        client = self.storage.client()
        self.assertIsNotNone(client)

        # Test caching behavior
        same_client = self.storage.client()
        self.assertIs(client, same_client)

        # Test with different config
        storage2 = S3Storage({
            'endpoint': 'http://localhost:4566',
            'access_key': 'different_key',
            'secret_key': 'different_secret',
            'region': 'eu-west-1',
            'bucket': 'another-bucket',
        }, self.mock_logger)

        # The client should be initialized with the specified config
        client2 = storage2.client()
        self.assertIsNotNone(client2)


if __name__ == '__main__':
    unittest.main()
