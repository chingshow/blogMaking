import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json


def main():
    # 设置API密钥和URL
    load_dotenv()
    api_key = os.getenv('RAGIC_API_2')

    base_url = 'https://ap12.ragic.com/cancerfree'
    tag = "articles"
    sheet_id = "4"

    params = {'api': '',
              'v': 3,
              'where': [
                  '1003464,eq,Yes',  # 已確認
                  '1003463,eq,Yes'  # 有改動
              ]}

    ENDPOINT = f'{base_url}/{tag}/{sheet_id}'
    response = requests.get(ENDPOINT, params=params, headers={'Authorization': 'Basic '+api_key})

    response_dict = response.json()

    # print(json.dumps(response_dict, indent=4))
    if response_dict != {}:
        """dict_iter = iter(response_dict)
        while True:
            try:
                key = next(dict_iter)

            except StopIteration:
                break"""

        data = response_dict
        all_websites = []
        for item in data.values():
            websites = item.get("Website", [])
            if isinstance(websites, str):
                all_websites.append(websites)
            elif isinstance(websites, list):
                all_websites.extend(websites)

        sheet_id = "6"
        params = {'api': '', 'v': 3}

        ENDPOINT = f'{base_url}/{tag}/{sheet_id}'
        response = requests.get(ENDPOINT, params=params, headers={'Authorization': 'Basic ' + api_key})

        response_dict = response.json()

        # print(json.dumps(response_dict, indent=4))

        with open('content_all.json', 'w', encoding="utf-8") as fJson:
            json.dump(response_dict, fJson, ensure_ascii=False, indent=4)
        print(len(response_dict))

        return list(set(all_websites))
    else:
        return []


if __name__ == "__main__":
    main()
