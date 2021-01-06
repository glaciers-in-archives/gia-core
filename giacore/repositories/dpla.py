import os

import requests


def dpla(query: str):
    has_more = True
    dpla_api_key = os.environ['DPLA_API_KEY']
    page = 1
    fields = 'object,isShownAt,id,sourceResource.title,sourceResource.description,dataProvider'

    while has_more:
        response = requests.get('https://api.dp.la/v2/items?api_key={}&q={}&page_size=500&page={}&fields={}'.format(dpla_api_key, query, page, fields))
        data = response.json()
        print(response.url)
        print(data)

        current_items = page * 500
        if current_items >= data['count']:
            has_more = False
        page += 1

        for item in data['docs']:

            if not 'object' in item:
                continue

            #TODO titels and descriptions can be arrays

            # description can sometimes not be present
            description = ''
            if 'sourceResource.description' in item:
                description = str(item['sourceResource.description'])


            g_a_item = {
                'id': item['id'],
                'harvest_source': 'dpla',
                'source_url': item['isShownAt'],
                'text': str(item['sourceResource.title']) + ' - ' + description,
                'provider': item['dataProvider'],
                'thumbnail': item['object'],
            }

            yield g_a_item