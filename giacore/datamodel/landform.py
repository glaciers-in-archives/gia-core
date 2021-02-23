from dataclasses import dataclass, field
import random
from typing import List, Optional

from rdflib import Literal, URIRef, XSD

from .utils.namespaces import DCTERMS, GIA, RDF, SCHEMA, init_graph


@dataclass()
class Landform:
    name: str
    description: str
    latitude: float = field(repr=False)
    longitude: float = field(repr=False)
    local_identifier: str = field(init=False)
    wikidata: Optional[URIRef] = field(default=None, repr=False)
    wikipedia: Optional[URIRef] = field(default=None, repr=False)
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
        graph.add((record, SCHEMA.sameAs, self.wikidata))
        graph.add((record, SCHEMA.relatedlink, self.wikipedia))
        graph.add((record, SCHEMA.latitude, Literal(self.latitude, datatype=XSD.decimal)))
        graph.add((record, SCHEMA.longitude, Literal(self.longitude, datatype=XSD.decimal)))

        for part in self.parts or []:
            graph.add((record, DCTERMS.hasPart, part))

        if self.parent:
            graph.add((record, DCTERMS.partOf, self.parent))

        return graph.serialize(format='xml').decode('utf-8')
