import os
import unittest
from uuid import uuid4
from equipment.framework.Storage.AbstractStorage import AbstractStorage
from equipment.framework.Storage.LocalStorage import LocalStorage
from equipment.framework.tests.BaseTest import BaseTest


class test_LocalStorage(BaseTest):
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
        self.assertTrue(self.app.storage().remove(file))
        self.assertFalse(self.app.storage().exists(file))

        os.rmdir(self.app.storage().path(path))


if __name__ == '__main__':
    unittest.main()
