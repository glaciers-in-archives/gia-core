from dataclasses import dataclass, field
import random
from typing import List, Optional

from rdflib import Literal, URIRef

from ..service.fuseki import Fuseki
from ..service.object_storage import ObjectStorage
from .utils.namespaces import DCTERMS, GIA, RDF, RDFS, SCHEMA, init_graph


@dataclass()
class Landform:
    name: str
    description: str
    latitude: float = field(repr=False)
    longitude: float = field(repr=False)
    local_identifier: str = field(init=False)
    wikidata: Optional[URIRef] = field(default=None, repr=False)
    parts: Optional[List[URIRef]] = field(default=None, repr=False)
    parent: Optional[URIRef] = field(default_factory=list, repr=False)

    def __post_init__(self):
        self.local_identifier = str(random.randrange(101, 1000))

    @property
    def uri(self) -> URIRef:
        return URIRef(str(GIA) + 'landform/' + self.local_identifier)

    @property
    def rdf(self) -> str:
        graph = init_graph()
        record = self.uri

        graph.add((record, RDF.type, SCHEMA.Landform))
        graph.add((record, SCHEMA.name, Literal(self.name, lang='en')))
        graph.add((record, SCHEMA.description, Literal(self.description, lang='en')))
        graph.add((record, RDFS.seeAlso, self.wikidata))
        graph.add((record, SCHEMA.latitude, Literal(self.latitude)))
        graph.add((record, SCHEMA.longitude, Literal(self.longitude)))
        
        for part in self.parts or []:
            graph.add((record, DCTERMS.hasPart, part))

        if self.parent:
            graph.add((record, DCTERMS.partOf, self.parent))

        return graph.serialize(format='xml').decode('utf-8')

    def store(self, endpoint=None, access_key=None, secret_key=None) -> None:
        objstore = ObjectStorage(
            bucket='record-store',
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
        )

        objstore.put_object(self.rdf, (str(self.uri).replace(str(GIA), '')))

    def index(self, endpoint=None) -> None:
        fuseki_client = Fuseki(endpoint=endpoint)
        fuseki_client.index(self.rdf)
