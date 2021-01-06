import functools
from typing import List, Optional

import requests
from rdflib import URIRef

from ..datamodel.utils.namespaces import WD

user_agent_header = 'Glacier\'s in Archives Harvester'

@functools.lru_cache
def resolve_item_label(qid: str) -> str:
    endpoint = 'https://www.wikidata.org/w/api.php?action=wbgetentities&props=labels&languages=en&utf8=1&&format=json&ids={}'.format(qid)
    r = requests.get(endpoint, headers={'User-Agent': user_agent_header})
    data = r.json()
    
    # this assumes there is always a English label
    return data['entities'][qid]['labels']['en']['value']


def create_location_label_from_wikidata_claims(wikidata_data: dict) -> Optional[str]:
    continent = None
    country = None
    if 'P30' in wikidata_data:
        continent = resolve_item_label(wikidata_data['P30'])
    if 'P17' in wikidata_data:
        country = resolve_item_label(wikidata_data['P17'])

    if continent and country:
        return '{}, {}'.format(country, continent)
    if continent:
        return continent
    return country


# get_entity_claims('Q278245', ['P30', 'P17', 'P625'])
def get_entity_claims(qid: str, claims: List[str]) -> dict:
    endpoint = 'https://www.wikidata.org/w/api.php?action=wbgetentities&props=claims&utf8=1&format=json&ids={}'.format(qid)
    r = requests.get(endpoint, headers={'User-Agent': user_agent_header})
    data = r.json()

    requested_claims = dict()
    for claim in data['entities'][qid]['claims'].items():
        if claim[0] in claims:
            if claim[1][0]['mainsnak']['snaktype'] == 'novalue':
                continue

            claim_data_value = claim[1][0]['mainsnak']['datavalue']
            if claim_data_value['type'] == 'wikibase-entityid':
                value = claim_data_value['value']['id']
            elif claim_data_value['type'] == 'string':
                value = claim_data_value['value']
            elif claim_data_value['type'] == 'globecoordinate':
                value = [claim_data_value['value']['latitude'], claim_data_value['value']['longitude']]
            else:
                raise ValueError('Unsupported data type: {}'.format(claim_data_value['type']))

            requested_claims[claim[0]] = value
    return requested_claims


def wd_uri(qid) -> URIRef:
    return URIRef(str(WD) + qid)
