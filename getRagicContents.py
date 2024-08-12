import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json


def main(site):
    params = {'api': '', 'v': 3}
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

    with open('content_all.json', 'w', encoding="utf-8") as fJson:
        json.dump(response_dict, fJson, ensure_ascii=False, indent=4)

    with open('content_all.json', 'r', encoding="utf-8") as fJson:
        load_dict = json.load(fJson)
        print(len(load_dict))

        dict_iter = iter(load_dict)

        content_init = {
            "title": site,
            "articles": []
        }

        with open(f'./{site}/content.json', 'w', encoding="utf-8") as file:
            json.dump(content_init, file, ensure_ascii=False, indent=4)

        while True:
            try:
                key = next(dict_iter)
                if load_dict[key]['Website'] == site:
                    value = load_dict[key]["Title"]
                    print(f"Key: {key}, Value: {value}")
                    no = load_dict[key]['_ragicId']
                    f = open(f'./{site}/documents/txt/{no}.txt', 'w', encoding="utf-8")
                    f.write(str(load_dict[key]['_ragicId']) + '\n')
                    f.write(load_dict[key]['時間'] + '\n')
                    f.write(load_dict[key]['Title'] + '\n')
                    f.write(load_dict[key]['Author'] + '\n')
                    f = open(f'./{site}/documents/txt/{no}.md', 'w', encoding="utf-8")
                    f.write(load_dict[key]['Content'])

                    with open(f'./{site}/content.json', 'r', encoding='utf-8') as file:
                        old_dict = json.load(file)
                        print(old_dict)

                        new_data = {
                            "titles": load_dict[key]["Title"],
                            "author": load_dict[key]['Author'],
                            "no": no,
                            "date": load_dict[key]['時間'],
                            "tags": load_dict[key]['Tags'],
                        }

                        old_dict["articles"].append(new_data)

                    # 保存新的 JSON 文件
                    with open(f'./{site}/content.json', 'w', encoding='utf-8') as file:
                        json.dump(old_dict, file, ensure_ascii=False, indent=4)
            except StopIteration:
                break


if __name__ == '__main__':
    main("Brain tumor")
