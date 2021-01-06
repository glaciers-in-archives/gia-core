import os
from dataclasses import dataclass, field
from typing import Optional

import requests


@dataclass
class Fuseki:
    endpoint: Optional[str] = field(default=None)

    def __post_init__(self):
        if not self.endpoint: self.endpoint = os.environ.get('GIA_FUSEKI_UPLOAD_ENDPOINT')

    def index(self, data: str) -> int:
        r = requests.post(str(self.endpoint), files={ 'files[]': ('data.rdf', data, 'application/rdf+xml') })
        return r.json()['tripleCount']
