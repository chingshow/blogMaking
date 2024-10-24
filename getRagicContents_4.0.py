import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json
import glob
import checkTxt
import finishUpdate


def main(site):
    params = {'api': '',
              'v': 3,
              'where': '1003463,eq,Yes'   # 有改動
              }
    # 设置API密钥和URL
    load_dotenv()
    api_key = os.getenv('RAGIC_API_2')
    base_url = 'https://ap12.ragic.com/cancerfree'
    tag = "articles"
    sheet_id = "4"

    ENDPOINT = f'{base_url}/{tag}/{sheet_id}'
    response = requests.get(ENDPOINT, params=params, headers={'Authorization': 'Basic '+api_key})

    response_dict = response.json()

    #print(json.dumps(response_dict, indent=4))

    with open(f'content_article.json', 'w', encoding="utf-8") as fJson:
        json.dump(response_dict, fJson, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main("Brain tumor")
