import os
from dataclasses import dataclass, field
from typing import Optional

import requests


@dataclass
class Fuseki:
    endpoint: Optional[str] = field(default=None)

    def __post_init__(self):
        if not self.endpoint: self.endpoint = os.environ.get('GIA_FUSEKI_DATASET_ENDPOINT')

    def index(self, data: str) -> int:
        r = requests.post(f'{self.endpoint}/data', files={ 'files[]': ('data.rdf', data, 'application/rdf+xml') })
        return r.json()['tripleCount']

    def clean_index(self) -> None:
        r = requests.post(f'{self.endpoint}/update', 'DELETE { ?s ?p ?o } WHERE { ?s ?p ?o }')
        if r.status_code != 204:
            print(r.text, r.status_code)
            raise Exception
