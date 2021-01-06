import os

import requests


def digitalnz(query: str):
    has_more = True
    digitalnz_api_key = os.environ['DIGITALNZ_API_KEY']
    page = 1
    fields = 'id,title,description,content_partner,source_url,large_thumbnail_url'

    while has_more:
        response = requests.get('http://api.digitalnz.org/v3/records.json?api_key={}&text={}&per_page=100&page={}&fields={}'.format(digitalnz_api_key, query, page, fields))
        data = response.json()

        current_items = page * 100
        if current_items >= data['search']['result_count']:
            has_more = False
        page += 1

        for item in data['search']['results']:

            if not item['large_thumbnail_url']:
                continue

            g_a_item = {
                'id': item['id'],
                'harvest_source': 'digital nz',
                'source_url': item['source_url'],
                'text': item['title'] + ' - ' + str(item['description']),
                'provider': item['content_partner'][0],
                'thumbnail': item['large_thumbnail_url'],
            }

            yield g_a_item