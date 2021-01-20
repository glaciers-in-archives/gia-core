from dataclasses import dataclass, field
from datetime import date
import random

from rdflib import Graph, Literal, URIRef

from .utils.namespaces import DCTERMS, OA, RDF, init_graph


@dataclass()
class Annotation:
    created: date = field(init=False)
    contributor: URIRef
    creator: URIRef
    target: URIRef
    body: tuple
    motivation: URIRef
    local_identifier: str = field(init=False)
    source: URIRef

    def __post_init__(self):
        self.local_identifier = 'oa-' + str(random.randrange(101, 10000))
        self.created = Literal(date.today())

    @property
    def uri(self) -> URIRef:
        return URIRef(str(self.target) + '#' + self.local_identifier)

    @property
    def graph(self) -> Graph:
        graph = init_graph()
        annotation = self.uri

        graph.add((annotation, RDF.type, OA.Annotation))
        graph.add((annotation, DCTERMS.contributor, self.contributor))
        graph.add((annotation, DCTERMS.creator, self.creator))
        graph.add((annotation, OA.hasTarget, self.target))
        graph.add((annotation, OA.hasBody, self.body))
        graph.add((annotation, OA.hasBody, (OA.hasSource, self.source)))
        graph.add((annotation, OA.motivatedBy. self.motivation))

        return graph
