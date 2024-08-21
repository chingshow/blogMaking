import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json
import glob
import checkTxt
import finishUpdate


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

    with open('content_article.json', 'w', encoding="utf-8") as fJson:
        json.dump(response_dict, fJson, ensure_ascii=False, indent=4)

    with open('content_article.json', 'r', encoding="utf-8") as fJson:
        load_dict = json.load(fJson)
        print(len(load_dict))

        dict_iter = iter(load_dict)

        while True:
            try:
                key = next(dict_iter)
                if site in load_dict[key]['Website'] and load_dict[key]['有改動'] == "Yes":
                    if load_dict[key]['available'] == "No":
                        print("bad")
                        with open(f'./{site}/content.json', 'r', encoding="utf-8") as file:
                            content = json.load(file)
                        content['documents']['items'] = [item for item in content['documents']['items'] if item['no'] != int(key)]

                        with open(f'./{site}/content.json', 'w', encoding="utf-8") as file:
                            json.dump(content, file, ensure_ascii=False, indent=4)
                        os.remove(f'./{site}/documents/txt/{key}.md')
                        os.remove(f'./{site}/documents/txt/{key}.txt')
                        os.remove(f'./{site}/documents/{key}.html')

                    else:
                        value = load_dict[key]["Title"]
                        no = load_dict[key]['_ragicId']
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


if __name__ == '__main__':
    main("Brain tumor")
