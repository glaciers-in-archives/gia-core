from rdflib import Namespace, Graph

RDF = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
SCHEMA = Namespace('https://schema.org/')
RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
DCTERMS = Namespace('http://purl.org/dc/terms/')
WD = Namespace('http://www.wikidata.org/entity/')
OA = Namespace('http://www.w3.org/ns/oa#')
AS = Namespace('http://www.w3.org/ns/activitystreams#')
GIA = Namespace('https://www.glaciersinarchives.org/')
PROV = Namespace('http://www.w3.org/ns/prov#')
GIAT = Namespace('https://www.glaciersinarchives.org/terms#')

def init_graph() -> Graph:
    graph = Graph()
    graph.bind('rdf', RDF)
    graph.bind('schema', SCHEMA)
    graph.bind('rdfs', RDFS)
    graph.bind('dcterms', DCTERMS)
    graph.bind('wd', WD)
    graph.bind('OA', OA)
    graph.bind('AS', AS)
    graph.bind('GIA', GIA)
    graph.bind('PROV', PROV)

    return graph
