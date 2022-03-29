from datetime import datetime
import os
import unittest
from uuid import uuid4
from equipment.framework.Storage.AbstractStorage import AbstractStorage
from equipment.framework.Storage.LocalStorage import LocalStorage
from equipment.framework.tests.TestCase import TestCase


class LocalStorageTest(TestCase):
    def setUp(self):
        super().setUp()

        self.app.config().set('STORAGE_LOCAL', 'path', 'storage/test')

        self.app.storage.override(LocalStorage(
            config=self.app.config(),
            log=self.app.log()
        ))

    def test_extends_from_abstract_storage(self):
        self.assertTrue(
            isinstance(self.app.storage(), AbstractStorage)
        )

    def test_file_lifecycle(self):
        path = str(uuid4())
        file = path + os.path.sep + str(uuid4()) + '.txt'
        content = str(uuid4())

        self.assertFalse(self.app.storage().exists(file))
        self.assertTrue(self.app.storage().write(file, content))

        self.assertTrue(self.app.storage().exists(file))
        self.assertEqual(self.app.storage().read(file), content)

        new_file = os.path.splitext(file)[0] + datetime.now().strftime('.%Y-%m-%d_%H_%M_%S') + '.txt'   # nopep8

        self.assertFalse(self.app.storage().exists(new_file))
        self.assertTrue(self.app.storage().move(file, new_file))
        self.assertTrue(self.app.storage().exists(new_file))
        self.assertTrue(self.app.storage().remove(new_file))
        self.assertFalse(self.app.storage().exists(new_file))

        os.rmdir(self.app.storage().path(path))

    def test_list_files_in_directory(self):
        path = str(uuid4())
        number_of_files = 10
        files = [path + os.path.sep + str(uuid4()) + '.txt' for _ in range(number_of_files)]    # nopep8
        content = str(uuid4())

        for file in files:
            self.app.storage().write(file, content)

        self.assertIsInstance(self.app.storage().list(path), list)
        self.assertEqual(len(self.app.storage().list(path)), number_of_files)

        for file in files:
            self.app.storage().remove(file)

        os.rmdir(self.app.storage().path(path))


if __name__ == '__main__':
    unittest.main()
