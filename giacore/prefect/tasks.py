from typing import Union, Optional

from prefect import task

from ..datamodel.landform import Landform
from ..datamodel.record import Record
from ..service.fuseki import Fuseki
from ..service.object_storage import ObjectStorage

@task
def index(entity: Union[Record, Landform]) -> None:
    entity.index()

@task
def store(entity: Union[Record, Landform]) -> None:
    entity.store()

@task
def index_all(prefix: Optional[str]=None, store_endpoint=None, store_access_key=None, store_secret_key=None, index_endpoint=None) -> None:
    objstore = ObjectStorage(
        bucket='record-store',
        endpoint=store_endpoint,
        access_key=store_access_key,
        secret_key=store_secret_key,
    )

    for o in objstore.list_objects(prefix=prefix):
        if not o.is_dir:
            data = objstore.get_object(o.object_name)
            fuseki_client = Fuseki(endpoint=index_endpoint)
            fuseki_client.index(data)