import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json
import glob
import checkTxt
import finishUpdate



def main(site):
    tag = site.replace('-', ' ')
    params = {'api': '', 'v': 3, 'where': [
        f'1003227,eq,{tag}',  # Website
        '1003464,eq,Yes',  # 已確認
        '1003463,eq,Yes'   # 有改動
    ]}

    params = {'api': '', 'v': 3, 'where': [
        f'1003227,eq,{tag}',  # Website
    ]}
    # 设置API密钥和URL
    load_dotenv()
    api_key = os.getenv('RAGIC_API_2')
    base_url = 'https://ap12.ragic.com/cancerfree'
    tag = "articles"
    sheet_id = "7"

    ENDPOINT = f'{base_url}/{tag}/{sheet_id}'
    response = requests.get(ENDPOINT, params=params, headers={'Authorization': 'Basic '+api_key})

    response_dict = response.json()

    #print(json.dumps(response_dict, indent=4))

    with open(f'content_{site}_article.json', 'w', encoding="utf-8") as fJson:
        json.dump(response_dict, fJson, ensure_ascii=False, indent=4)

    with open(f'content_{site}_article.json', 'r', encoding="utf-8") as fJson:
        load_dict = json.load(fJson)
        print(len(load_dict))

        dict_iter = iter(load_dict)

        while True:
            try:
                key = next(dict_iter)
                if load_dict[key]['available'] == "No":
                    print("bad")
                    with open(f'./{site}/content.json', 'r', encoding="utf-8") as file:
                        content = json.load(file)
                    content['documents']['items'] = [item for item in content['documents']['items'] if
                                                     item['no'] != int(key)]

                    with open(f'./{site}/content.json', 'w', encoding="utf-8") as file:
                        json.dump(content, file, ensure_ascii=False, indent=4)

                    def remove_if_exists(file_path):
                        if os.path.exists(file_path):
                            os.remove(file_path)

                    remove_if_exists(f'./{site}/documents/txt/{key}.md')
                    remove_if_exists(f'./{site}/documents/txt/{key}.txt')
                    remove_if_exists(f'./{site}/documents/{key}.html')

                else:
                    value = load_dict[key]["Title"]
                    no = load_dict[key]['_ragicId']
                    if not os.path.exists(f'./{site}/documents/txt/'):
                        os.makedirs(f'./{site}/documents/txt/', exist_ok=True)
                    f = open(f'./{site}/documents/txt/{no}.txt', 'w', encoding="utf-8")
                    f.write(str(load_dict[key]['_ragicId']) + '\n')
                    f.write(load_dict[key]['時間'] + '\n')
                    f.write(load_dict[key]['Title'] + '\n')
                    f.write(load_dict[key]['Author'] + '\n')
                    f = open(f'./{site}/documents/txt/{no}.md', 'w', encoding="utf-8")
                    f.write(load_dict[key]['Content'])
                    f.close()

                    new_data = {
                        "titles": load_dict[key]["Title"],
                        "author": load_dict[key]['Author'],
                        "no": no,
                        "date": load_dict[key]['時間'],
                        "tags": load_dict[key]['Tags'],
                    }
                    checkTxt.main(key, site, new_data)
                if len(load_dict[key]['Website']) == 1:
                    finishUpdate.main(load_dict[key]["_ragicId"])
            except StopIteration:
                break


def checkAll(site):
    params = {'api': '', 'v': 3, 'where': f'1005231,like,{site}'}
    # 设置API密钥和URL
    load_dotenv()
    api_key = os.getenv('RAGIC_API_2')
    base_url = 'https://ap12.ragic.com/cancerfree'
    tag = "articles"
    sheet_id = "7"

    ENDPOINT = f'{base_url}/{tag}/{sheet_id}'
    response = requests.get(ENDPOINT, params=params, headers={'Authorization': 'Basic '+api_key})

    response_dict = response.json()

    print(json.dumps(response_dict, indent=4))

    with open(f'content_article.json', 'w', encoding="utf-8") as fJson:
        json.dump(response_dict, fJson, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    checkAll("Breast Cancer")
    #main("Breast Cancer")
