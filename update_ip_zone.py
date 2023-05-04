import requests

token = 'your_key'
link = 'link'
count = 0
current_id = 622
next_id = 464
response = requests.get(url=f'{link}/referencebooks/houses', cookies={'token': token}).json()
for item in response:
    if current_id in item.get('zones'):
        print(item['house_id'])
        params_put = {
            "house_id": item['house_id'],
            "connect_date": item['connect_date'],
            "post_code": item['post_code'],
            "country": item['country'],
            "region": item['region'],
            "city": item['city'],
            "street": item['street'],
            "number": item['number'],
            "building": item['building'],
            "description": item['description'],
            "ip_zones": [
                {
                    "id": next_id
                }
            ]
        }
        count += 1
        resp = requests.put(url=f'{link}/referencebooks/houses', cookies={'token': token}, json=params_put).json()
        print(count, '- счётчик')
        print(resp)
