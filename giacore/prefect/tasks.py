from typing import Union, Optional

from prefect import task

from ..datamodel.landform import Landform
from ..datamodel.record import Record
from ..datamodel.utils.namespaces import GIA
from ..service.fuseki import Fuseki
from ..service.object_storage import ObjectStorage

@task
def index(entity: Union[Record, Landform], endpoint=None) -> None:
    fuseki_client = Fuseki(endpoint=endpoint)
    fuseki_client.index(entity.rdf)

@task
def store(entity: Union[Record, Landform], endpoint=None, access_key=None, secret_key=None) -> None:
    objstore = ObjectStorage(
        bucket='record-store',
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
    )

    objstore.put_object(entity.rdf, (str(entity.uri).replace(str(GIA), '')))

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

@task
def replace_string_store(old: str, new: str, prefix: Optional[str]=None, store_endpoint=None, store_access_key=None, store_secret_key=None) -> None:
    objstore = ObjectStorage(
        bucket='record-store',
        endpoint=store_endpoint,
        access_key=store_access_key,
        secret_key=store_secret_key,
    )

    for o in objstore.list_objects(prefix=prefix):
        if not o.is_dir:
            data = objstore.get_object(o.object_name)
            if old in data:
                data = data.replace(old, new)
                objstore.put_object(data, o.object_name)

@task
def clean_index(index_endpoint=None) -> None:
    f = Fuseki(endpoint=index_endpoint)
    f.clean_index()

@task
def uri_is_used(uri: str, store_endpoint=None, store_access_key=None, store_secret_key=None) -> bool:
    objstore = ObjectStorage(
        bucket='record-store',
        endpoint=store_endpoint,
        access_key=store_access_key,
        secret_key=store_secret_key,
    )

    local_id = uri.replace(str(GIA), '')
    return objstore.object_exists(local_id)
