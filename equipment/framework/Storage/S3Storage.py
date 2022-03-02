from boto3 import client
from botocore.errorfactory import ClientError
from equipment.framework.Config.AbstractConfig import AbstractConfig
from equipment.framework.Log.AbstractLog import AbstractLog
from equipment.framework.Storage.AbstractStorage import AbstractStorage


class S3Storage(AbstractStorage):
    def __init__(self, config: AbstractConfig, log: AbstractLog):
        self.config = config
        self.log = log
        self.client = None

    def load(self) -> None:
        if self.client is None:
            self.reload()

    def reload(self) -> None:
        self.client = client(
            service_name='s3',
            endpoint_url=self.config.get('STORAGE_S3', 'aws_endpoint'),
            region_name=self.config.get('STORAGE_S3', 'aws_region'),
            aws_access_key_id=self.config.get(
                'STORAGE_S3', 'aws_access_key_id'),
            aws_secret_access_key=self.config.get(
                'STORAGE_S3', 'aws_secret_access_key'),
        )

    def path(self, file: str) -> str:
        raise NotImplementedError  # TODO

    def write(self, file: str, data: str) -> bool:
        try:
            self.load()
            self.client.put_object(
                Bucket=self.config.get('STORAGE_S3', 'aws_bucket'),
                Key=file,
                Body=data
            )

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def read(self, file: str) -> str:
        self.load()

        self.log.debug('S3Storage@read file: ' + file)

        result = self.client.get_object(
            Bucket=self.config.get('STORAGE_S3', 'aws_bucket'),
            Key=file,
        )

        return result['Body'].read().decode(self.config.get('STORAGE_S3', 'aws_decode'))

    def exists(self, file: str) -> bool:
        try:
            self.load()

            self.client.head_object(
                Bucket=self.config.get('STORAGE_S3', 'aws_bucket'),
                Key=file,
            )
            return True
        except ClientError as e:
            if e.response['ResponseMetadata']['HTTPStatusCode'] == 404:
                return False

            self.log.error(e, exc_info=True)
            raise e

    def remove(self, file: str) -> bool:
        try:
            self.load()

            self.client.delete_object(
                Bucket=self.config.get('STORAGE_S3', 'aws_bucket'),
                Key=file,
            )
            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False
