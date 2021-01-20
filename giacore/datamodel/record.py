from dataclasses import dataclass, field
import random
from typing import List, Optional, Union

from rdflib import Literal, URIRef

from ..service.fuseki import Fuseki
from ..service.object_storage import ObjectStorage
from .annotation import Annotation
from .utils.namespaces import GIA, RDF, SCHEMA, init_graph


@dataclass()
class Record:
    entities: List[URIRef]
    description: Optional[Union[str, Literal]]
    publisher: Union[str, Literal]
    creator: Optional[Union[str, Literal]]
    created: Optional[Union[str, Literal]]
    media_license: Optional[URIRef]
    local_identifier: str = field(init=False)
    record_type: Optional[URIRef]
    same_as: List[URIRef]
    annotations: Optional[List[Annotation]] = field(default=None, repr=False)

    def __post_init__(self):
        self.local_identifier = str(random.randrange(101, 10000))

    @property
    def uri(self) -> URIRef:
        return URIRef(str(GIA) + 'record/' + self.local_identifier)

    @property
    def rdf(self) -> str:
        graph = init_graph()
        record = self.uri

        graph.add((record, RDF.type, SCHEMA.CreativeWork))
        if self.same_as:
            graph.add((record, GIA.type, self.record_type))

        graph.add((record, SCHEMA.description, Literal(self.description)))

        for same_as in self.same_as:
            graph.add((record, SCHEMA.sameAs, same_as))

        for entity in self.entities:
            graph.add((record, SCHEMA.spatial, entity))

        graph.add((record, SCHEMA.creator, Literal(self.creator)))
        graph.add((record, SCHEMA.publisher, Literal(self.publisher)))
        graph.add((record, SCHEMA.temporal, Literal(self.created)))
        graph.add((record, SCHEMA.license, self.media_license))

        for annotation in self.annotations:
            graph + annotation.graph

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
