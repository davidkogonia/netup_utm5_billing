import requests

token = 'your_  key'
link = 'link'
count = 0
#       -> getting account_id via house_id <-
zone_id = 250
switch_id = 249
response = requests.get(url=f'{link}/referencebooks/houses', cookies={'token': token}).json()
for item in response:
    if zone_id in item.get('zones'):
        params_get_user_by_house = {
            "page": 1,
            "per_page": 10000,
            "is_desc": True,
            "sort_field": "user_id",
            "queries_conditions": "and",
            "queries":
                [
                    {
                        "field": "house_id",
                        "value": str(item['house_id']),
                        "condition": "equal"
                    },
                ]
        }
        response_get_user_by_house = requests.post(url=f'{link}/users/extended_search', json=params_get_user_by_house,
                                                   cookies={'token': token}).json()
        if response_get_user_by_house['total_rows'] == 1:
            print('id дома:', item['house_id'])
            print(response_get_user_by_house['users'][0]['user_id'], '- user id')

            #       -> getting slink_id via account_id <-
            params_get_slink_by_user = {
                'user_id': response_get_user_by_house['users'][0]['user_id']
            }
            response_get_slink_by_user = requests.get(url=f'{link}/users', params=params_get_slink_by_user,
                                                      cookies={'token': token}).json()

            for user_account_id in response_get_slink_by_user['slinks']:

                #       -> get information about servicelinks <-
                params_get = {
                    "slink_id": user_account_id
                }
                response_get = requests.get(url=f'{link}/users/servicelinks/iptraffic', params=params_get,
                                            cookies={'token': token})
                if response_get.status_code != 200:
                    continue
                response_get = response_get.json()
                if response_get['servicedata']['service_type'] == 3:
                    count += 1
                    print(user_account_id, '- slink_id')
                    print(response_get['ip_group']['items'][0]['switch_id'], '- current switch_id')
                    print(count, '- счётчик')
                    print('________________________________________________________')

                    # print(json.dumps(response_get['ip_group']['items'][0]['mask'], indent=4, ensure_ascii=False))
                    params_put = {
                        "slink_id": params_get["slink_id"],
                        "user_id": response_get["servicelink"]["user_id"],
                        "account_id": response_get["servicelink"]["account_id"],
                        "service_id": response_get['servicelink']['service_id'],
                        "accounting_period_id": response_get["periodicservicelink"]["accounting_period_id"],
                        "start_date": response_get["periodicservicelink"]["start_date"],
                        "expire_date": response_get["periodicservicelink"]["expire_date"],
                        "policy_id": response_get["periodicservicelink"]["policy_id"],
                        "cost_coef": response_get["periodicservicelink"]["cost_coef"],
                        "house_comment": response_get["periodicservicelink"]["house_comment"],
                        "comment": response_get["periodicservicelink"]["comment"],
                        "house_id": response_get["periodicservicelink"]["house_id"],
                        "ip_group": [
                            {
                                "ip": response_get['ip_group']['items'][0]['ip'],
                                "mask": 32,
                                "mac": response_get['ip_group']['items'][0]['mac'],
                                "login": response_get['ip_group']['items'][0]['login'],
                                "allowed_cid": "",
                                "password": "",
                                "pool_name": "",
                                "flags": response_get['ip_group']['items'][0]['flags'],
                                "nfprovider_id": response_get['ip_group']['items'][0]['nfprovider_id'],
                                "switch_id": switch_id,
                                "port_id": response_get['ip_group']['items'][0]['port_id'],
                                "vlan_id": response_get['ip_group']['items'][0]['vlan_id'],
                                "pool_id": response_get['ip_group']['items'][0]['pool_id'],
                                "owner_id": 0,
                                "owner_type": 0,
                                "dhcp_options": response_get['ip_group']['items'][0]['dhcp_options'],
                                "isg_attrs": response_get['ip_group']['items'][0]['isg_attrs']
                            }
                        ],
                        "traffic_quota": response_get['iptrafficServiceLink']['traffic_quota']
                    }
                    response_put = requests.put(url=f'{link}/users/servicelinks/iptraffic', json=params_put,
                                                cookies={'token': token}).json()
        #         else:
        #             print('У пользователя с id,', response_get_user_by_house['users'][0]['user_id'],
        #                   'нет услуги интернет')
        # else:
        #     print('user with house', str(item['house_id']), 'id does not exist')
