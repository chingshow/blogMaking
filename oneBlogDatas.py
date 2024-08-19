import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json


def load_existing_content(path):
    content_path = os.path.join(path, 'content.json')
    if os.path.exists(content_path):
        try:
            with open(content_path, 'r', encoding="utf-8") as file:
                data = json.load(file)
                return data.get('documents', {}).get('items', [])
        except json.JSONDecodeError:
            print(f"錯誤：'{content_path}' 不是有效的JSON文件。")
        except IOError:
            print(f"錯誤：無法讀取文件 '{content_path}'。")
    return []

def main(no, path):
    # 读取原始 JSON 文件
    with open('content_all.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    def get_filename(path):
        return path.split('@')[-1] if '@' in path else path

    def checkImage(path):
        if path == "":
            return ""
        else:
            return f"./images/{get_filename(path)}"

    # 创建新的 JSON 结构
    print(data[no])
    new_data = {
        "color1": data[no]["color1"],
        "color2": data[no]["color2"],
        "color3": data[no]["color3"],
        "color4": data[no]["color4"],
        "color5": data[no]["color5"],
        "siteTitle": data[no]["Website tag"],
        "hero": {
            "title": data[no]["Website Name"],
            "backgroundImage": checkImage(data[no]['Image'])
        },
        "introduction": {
            "content": data[no]["Introduction"],
            "image": checkImage(data[no]['Image'])
        },
        "documents": {
            "title": "Documents",
            "items": load_existing_content(path)
        },
        "ad": {
            "image": checkImage(data[no]['Image2']),
            "content": data[no]['content'],
            "link": data[no]['link']
        }
    }

    # 保存新的 JSON 文件
    with open(f'./{path}/content.json', 'w', encoding='utf-8') as file:
        json.dump(new_data, file, ensure_ascii=False, indent=4)




