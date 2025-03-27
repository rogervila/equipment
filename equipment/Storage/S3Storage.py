from typing import TYPE_CHECKING
import boto3
from botocore.exceptions import ClientError

from equipment.Storage.AbstractStorage import AbstractStorage

if TYPE_CHECKING:
    from mypy_boto3_s3.client import S3Client
    from equipment.Log.AbstractLogger import AbstractLogger


class S3Storage(AbstractStorage):
    s3: 'S3Client'

    def __init__(self, config: dict, log: 'AbstractLogger'):
        self.config = config
        self.log = log

    def client(self) -> 'S3Client':
        if not hasattr(self, 's3'):
            self.s3 = boto3.client(
                's3',
                endpoint_url=self.config['endpoint'],
                aws_access_key_id=self.config['access_key'],
                aws_secret_access_key=self.config['secret_key'],
                region_name=self.config['region']
            )

        return self.s3

    def _get_full_path(self, file: str) -> str:
        prefix = self.config['prefix'] if 'prefix' in self.config else ''
        prefix = '' if prefix is None or prefix == 'None' or prefix == 'null' else prefix
        if prefix and not prefix.endswith('/'):
            prefix += '/'
        return f"{prefix}{file}"

    def path(self, file: str) -> str:
        return self._get_full_path(file)

    def write(self, file: str, data: str) -> bool:
        try:
            s3_path = self._get_full_path(file)

            self.client().put_object(
                Bucket=self.config['bucket'],
                Key=s3_path,
                Body=data
            )
            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def read(self, file: str) -> str:
        if not self.exists(file):
            raise FileNotFoundError(file)

        try:
            s3_path = self._get_full_path(file)

            response = self.client().get_object(
                Bucket=self.config['bucket'],
                Key=s3_path
            )
            return response['Body'].read().decode('utf-8')
        except Exception as e:
            self.log.error(e, exc_info=True)
            raise

    def exists(self, file: str) -> bool:
        try:
            s3_path = self._get_full_path(file)
            self.client().head_object(
                Bucket=self.config['bucket'],
                Key=s3_path
            )
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            self.log.error(e, exc_info=True)
            return False
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def remove(self, file: str) -> bool:
        try:
            s3_path = self._get_full_path(file)

            self.client().delete_object(
                Bucket=self.config['bucket'],
                Key=s3_path
            )
            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def move(self, source: str, destination: str) -> bool:
        try:
            source_path = self._get_full_path(source)
            dest_path = self._get_full_path(destination)

            # Copy the object to the new location
            self.client().copy_object(
                Bucket=self.config['bucket'],
                CopySource={
                    'Bucket': self.config['bucket'], 'Key': source_path},
                Key=dest_path
            )

            # Delete the original
            self.client().delete_object(
                Bucket=self.config['bucket'],
                Key=source_path
            )

            return True
        except Exception as e:
            self.log.error(e, exc_info=True)
            return False

    def list(self, path: str) -> list:
        try:
            s3_path = self._get_full_path(path)
            if not s3_path.endswith('/'):
                s3_path += '/'

            response = self.client().list_objects_v2(
                Bucket=self.config['bucket'],
                Prefix='' if s3_path == '/' else s3_path,
            )

            # Extract just filenames from the full paths
            contents = response.get('Contents', [])
            files = []

            for obj in contents:
                if 'Key' not in obj:
                    continue

                # Skip directories (objects that end with /)
                key = obj['Key']
                if not key.endswith('/'):
                    # Remove the prefix and path to get just the filename
                    name = key.replace(s3_path, '', 1)
                    if name:  # Only add non-empty names
                        files.append(name)

            return files
        except Exception as e:
            self.log.error(e, exc_info=True)
            raise
