import random
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from rdflib import Literal, URIRef

from .utils.namespaces import GIA, OA


@dataclass()
class Annotation:
    created: date = field(init=False, repr=False)
    body: tuple
    motivation: str
    contributor: Optional[str] = field(default=None, repr=False)
    creator: Optional[str] = field(default=None, repr=False)
    derived_from: Optional[URIRef] = field(default=None, repr=False)
    local_identifier: str = field(init=False)

    def __post_init__(self):
        self.local_identifier = 'oa-' + str(random.randrange(101, 10000))
        self.created = Literal(date.today())

        valid_motivations = ['linking', 'describing', 'classifying']
        if self.motivation in valid_motivations:
            self.motivation = URIRef(str(OA) + self.motivation)
        else:
            raise ValueError(f'Invalid motivation: {self.motivation}')

        valid_agents = ['machine', 'person']

        if self.contributor:
            if self.contributor in valid_agents:
                self.contributor = URIRef(str(GIA) + f'concept/agent/{self.contributor}')
            else:
                raise ValueError(f'Invalid contributor: {self.contributor}')

        if self.creator:
            if self.creator in valid_agents:
                self.creator = URIRef(str(GIA) + f'concept/agent/{self.creator}')
            else:
                raise ValueError(f'Invalid creator: {self.creator}')
