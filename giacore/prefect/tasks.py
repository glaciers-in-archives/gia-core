from typing import Union

from prefect import task

from ..datamodel.landform import Landform
from ..datamodel.record import Record

@task
def index(entity: Union[Record, Landform]) -> None:
    entity.index()

@task
def store(entity: Union[Record, Landform]) -> None:
    entity.store()
