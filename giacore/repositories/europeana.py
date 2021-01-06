import os
import urllib.parse

import requests


def europeana(query: str, key=None):
    cursor = '*'
    uri_prefix = 'http://data.europeana.eu/item'
    has_more = True
    if not key:
        europeana_api_key = os.environ['EUROPEANA_API_KEY']
    else:
        europeana_api_key = key

    while has_more:
        response = requests.get('https://www.europeana.eu/api/v2/search.json?wskey={}&query={}&media=true&rows=100&cursor={}'.format(europeana_api_key, query, cursor))
        data = response.json()

        #todo if not items in data: check common errors
        for item in data['items']:
            if not 'edmIsShownAt' in item:
                continue

            merged_description = ''
            if 'dcDescription' in item:
                for desc in item['dcDescription']:
                    merged_description += desc + '\n'

                merged_description = item['title'][0] + ' ' + merged_description
                
            g_a_item = {
                'id': uri_prefix + item['id'],
                'author': item['dcCreator'][0] if 'dcCreator' in item else '',
                'source_url': item['edmIsShownAt'][0],
                'text': item['dcDescription'][0] if 'dcDescription' in item else '',
                'provider': item['dataProvider'][0],
                'thumbnail': item['edmPreview'][0],
                'made_up_description': merged_description,
            }

            yield g_a_item

        if 'nextCursor' in data:
            cursor = urllib.parse.quote_plus(data['nextCursor'])
        else:
            has_more = False
