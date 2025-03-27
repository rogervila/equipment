import unittest
import tempfile
import os
import shutil
from codecs import open  # pylint: disable=W0622
from unittest.mock import MagicMock
from equipment.Log.NullLogger import NullLogger
from equipment.Storage.LocalStorage import LocalStorage


class TestLocalStorage(unittest.TestCase):
    def setUp(self):
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()

        # Logger
        self.logger = NullLogger()

        # Configuration for LocalStorage
        self.config = {
            'path': 'test_storage'
        }

        # Create LocalStorage instance
        self.storage = LocalStorage(self.config, self.temp_dir, self.logger)

        # Create the storage directory
        os.makedirs(os.path.join(self.temp_dir, 'test_storage'), exist_ok=True)

    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)

    def test_init(self):
        # Test initialization
        self.assertEqual(self.storage.config, self.config)
        self.assertEqual(self.storage.base_path, self.temp_dir)
        self.assertEqual(self.storage.log, self.logger)

    def test_local_storage_path(self):
        expected_path = os.path.join(self.temp_dir, 'test_storage')
        path = self.storage._local_storage_path()  # pylint: disable=W0212
        self.assertEqual(path, expected_path)

    def test_path(self):
        expected_path = os.path.join(
            self.temp_dir, 'test_storage', 'test_file.txt')
        self.assertEqual(self.storage.path('test_file.txt'), expected_path)

    def test_write_success(self):
        # Test writing a file successfully
        result = self.storage.write('test_file.txt', 'Hello, World!')

        self.assertTrue(result)
        expected_path = os.path.join(
            self.temp_dir, 'test_storage', 'test_file.txt')
        self.assertTrue(os.path.isfile(expected_path))

        with open(expected_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'Hello, World!')

    def test_write_nested_directory(self):
        # Test writing a file in a nested directory
        result = self.storage.write(
            'nested/dir/test_file.txt', 'Nested content')

        self.assertTrue(result)
        expected_path = os.path.join(
            self.temp_dir, 'test_storage', 'nested/dir/test_file.txt')
        self.assertTrue(os.path.isfile(expected_path))

        with open(expected_path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'Nested content')

    def test_write_error(self):
        # Test write error by using a mock to simulate an exception
        self.storage.path = MagicMock(side_effect=Exception("Test exception"))

        result = self.storage.write('test_file.txt', 'Hello, World!')

        self.assertFalse(result)

    def test_read_success(self):
        # Create a file to read
        file_path = os.path.join(
            self.temp_dir, 'test_storage', 'test_file.txt')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write('Test content')

        # Read the file
        content = self.storage.read('test_file.txt')

        self.assertEqual(content, 'Test content')

    def test_read_file_not_found(self):
        # Test reading a non-existent file
        with self.assertRaises(FileNotFoundError):
            self.storage.read('non_existent_file.txt')

    def test_exists_true(self):
        # Create a file
        file_path = os.path.join(
            self.temp_dir, 'test_storage', 'test_file.txt')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write('Test content')

        # Check if file exists
        self.assertTrue(self.storage.exists('test_file.txt'))

    def test_exists_false(self):
        # Check if non-existent file exists
        self.assertFalse(self.storage.exists('non_existent_file.txt'))

    def test_remove_success(self):
        # Create a file to remove
        file_path = os.path.join(
            self.temp_dir, 'test_storage', 'test_file.txt')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write('Test content')

        # Remove the file
        result = self.storage.remove('test_file.txt')

        self.assertTrue(result)
        self.assertFalse(os.path.exists(file_path))

    def test_remove_error(self):
        # Test remove error with non-existent file
        result = self.storage.remove('non_existent_file.txt')

        self.assertFalse(result)

    def test_move_success(self):
        # Create a file to move
        source_path = os.path.join(self.temp_dir, 'test_storage', 'source.txt')
        destination_path = os.path.join(
            self.temp_dir, 'test_storage', 'destination.txt')
        os.makedirs(os.path.dirname(source_path), exist_ok=True)

        with open(source_path, 'w') as f:
            f.write('Test content')

        # Move the file
        result = self.storage.move('source.txt', 'destination.txt')

        self.assertTrue(result)
        self.assertFalse(os.path.exists(source_path))
        self.assertTrue(os.path.exists(destination_path))

    def test_move_error(self):
        # Test move error with non-existent source file
        result = self.storage.move('non_existent_file.txt', 'destination.txt')

        self.assertFalse(result)

    def test_list_success(self):
        # Create test files
        dir_path = os.path.join(self.temp_dir, 'test_storage', 'test_dir')
        os.makedirs(dir_path, exist_ok=True)

        with open(os.path.join(dir_path, 'file1.txt'), 'w') as f:
            f.write('File 1')

        with open(os.path.join(dir_path, 'file2.txt'), 'w') as f:
            f.write('File 2')

        # Create a subdirectory (should not be in results)
        os.makedirs(os.path.join(dir_path, 'subdir'), exist_ok=True)

        # List files
        files = self.storage.list('test_dir')

        self.assertIn('file1.txt', files)
        self.assertIn('file2.txt', files)
        self.assertEqual(len(files), 2)  # Only files, not directories

    def test_list_directory_not_found(self):
        # Test listing a non-existent directory
        with self.assertRaises(NotADirectoryError):
            self.storage.list('non_existent_dir')


if __name__ == '__main__':
    unittest.main()
