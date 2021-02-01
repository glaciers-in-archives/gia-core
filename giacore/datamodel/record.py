from dataclasses import dataclass, field
import random
from typing import List, Optional, Union

from rdflib import BNode, Literal, URIRef

from .annotation import Annotation
from .utils.namespaces import DCTERMS, GIA, GIAT, OA, PROV, RDF, SCHEMA, init_graph


@dataclass()
class Record:
    publisher: Union[str, Literal] = field(repr=False)
    source: URIRef
    same_as: List[URIRef] = field(repr=False)
    annotations: List[Annotation] = field(repr=False)
    local_identifier: str = field(init=False)
    image: Optional[URIRef] = field(default=None, repr=False)

    def __post_init__(self):
        self.local_identifier = str(random.randrange(101, 100000))

    @property
    def uri(self) -> URIRef:
        return URIRef(str(GIA) + 'record/' + self.local_identifier)

    @property
    def rdf(self) -> str:
        graph = init_graph()
        record = self.uri

        graph.add((record, SCHEMA.provider, Literal(self.publisher)))
        graph.add((record, DCTERMS.source, self.source))

        if self.image:
            graph.add((record, SCHEMA.image, self.image))

        for same_as in self.same_as:
            graph.add((record, SCHEMA.sameAs, same_as))

        for annotation in self.annotations:
            ag = init_graph()
            annotation_uri = URIRef(f'{self.uri}#{annotation.local_identifier}')
            ag.add((annotation_uri, OA.hasTarget, self.uri))
            ag.add((annotation_uri, RDF.type, OA.Annotation))
            ag.add((annotation_uri, OA.motivatedBy, annotation.motivation))
            ag.add((annotation_uri, DCTERMS.issued, annotation.created))

            body = BNode()
            ag.add((annotation_uri, OA.hasBody, body))
            if annotation.body[0] == GIAT.type:
                ag.add((body, GIAT.type, annotation.body[1]))
                graph.add((record, RDF.type, annotation.body[1]))
            else:
                ag.add((body, annotation.body[0], annotation.body[1]))
                graph.add((record, annotation.body[0], annotation.body[1]))

            if annotation.creator:
                graph.add((annotation_uri, DCTERMS.creator, annotation.creator))

            if annotation.contributor:
                graph.add((annotation_uri, DCTERMS.contributor, annotation.contributor))

            if annotation.derived_from:
                graph.add((annotation_uri, PROV.wasDerivedFrom, annotation.derived_from))

            graph += ag

        return graph.serialize(format='xml').decode('utf-8')
