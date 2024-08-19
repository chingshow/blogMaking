import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json


def main():
    params = {'api': '', 'v': 3}
    # 设置API密钥和URL
    load_dotenv()
    api_key = os.getenv('RAGIC_API_2')

    base_url = 'https://ap12.ragic.com/cancerfree'
    tag = "articles"
    sheet_id = "6"

    ENDPOINT = f'{base_url}/{tag}/{sheet_id}'
    response = requests.get(ENDPOINT, params=params, headers={'Authorization': 'Basic '+api_key})

    response_dict = response.json()

    # print(json.dumps(response_dict, indent=4))

    with open('content_all.json', 'w', encoding="utf-8") as fJson:
        json.dump(response_dict, fJson, ensure_ascii=False, indent=4)
    print(len(response_dict))

    return len(response_dict)


if __name__ == "__main__":
    main()
