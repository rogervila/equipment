import unittest
from os import sep
from uuid import uuid4
import boto3
from moto import mock_s3
from equipment.framework.tests.TestCase import TestCase
from equipment.framework.Storage.AbstractStorage import AbstractStorage
from equipment.framework.Storage.S3Storage import S3Storage


class S3StorageTest(TestCase):
    def setUp(self):
        super().setUp()

        self.app.storage.override(S3Storage(
            config=self.app.config(),
            log=self.app.log()
        ))

    def test_extends_from_abstract_storage(self):
        self.assertTrue(
            isinstance(self.app.storage(), AbstractStorage)
        )

    @mock_s3
    def test_file_lifecycle(self):
        self.app.storage().client = boto3.client('s3', region_name='us-east-1')

        # We need to create the bucket since this is all in Moto's 'virtual' AWS account
        self.app.storage().client.create_bucket(
            Bucket=self.app.config().get('STORAGE_S3', 'aws_bucket')
        )

        path = str(uuid4())
        file = path + sep + str(uuid4()) + '.txt'
        content = str(uuid4())

        self.assertFalse(self.app.storage().exists(file))

        self.assertTrue(self.app.storage().write(file, content))

        self.assertTrue(self.app.storage().exists(file))
        self.assertEqual(self.app.storage().read(file), content)
        self.assertTrue(self.app.storage().remove(file))
        self.assertFalse(self.app.storage().exists(file))


if __name__ == '__main__':
    unittest.main()
