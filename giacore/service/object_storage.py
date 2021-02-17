import io
import os
from dataclasses import dataclass, field
from typing import Generator, Optional

from minio import Minio, Object


@dataclass
class ObjectStorage:
    bucket: str
    endpoint: Optional[str] = field(default=None)
    access_key: Optional[str] = field(default=None)
    secret_key: Optional[str] = field(default=None)
    secure: bool = field(default=False)
    client: Minio = field(init=False)

    def __post_init__(self):
        if not self.endpoint: self.endpoint = os.environ.get('GIA_OBJECT_STORAGE_ENDPOINT')
        if not self.access_key: self.access_key = os.environ.get('GIA_OBJECT_STORAGE_ACCESS_KEY')
        if not self.secret_key: self.secret_key = os.environ.get('GIA_OBJECT_STORAGE_SECRET_KEY')

        if os.environ.get('GIA_OBJECT_STORAGE_SSL_ENABLED'):
            self.secure = True

        self.client = Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure,
        )

    def bucket_exists(self)-> bool:
        return self.client.bucket_exists(self.bucket)

    def list_objects(self, prefix: Optional[str] = None) -> Generator[Object, None, None]:
        for obj in self.client.list_objects_v2(self.bucket, prefix=prefix, recursive=True):
            yield obj

    def put_object(self, content: str, location: str) -> None:
        content_bytes = io.BytesIO(bytes(content, 'utf-8'))

        self.client.put_object(
            self.bucket,
            f'{location}.xml',
            content_bytes,
            len(content_bytes.getvalue()),
        )

    def get_object(self, obj: str) -> str:
        response = self.client.get_object(self.bucket, f'{obj}.xml')
        data = response.data.decode('utf-8')
        response.close()
        response.release_conn()
        return data
