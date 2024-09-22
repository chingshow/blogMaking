import requests
from dotenv import load_dotenv
import os
import json
import base64
import urllib.parse
import shutil


def download_image(image_field_value, path, base_url, api_key):
    if '@' in image_field_value:
        file_id, filename = image_field_value.split('@')
        print(f'Downloading image {filename}...')

        # 构建图片文件的下载 URL
        encoded_filename = urllib.parse.quote(filename)
        image_url = f'{base_url}/sims/file.jsp?a=cancerfree&f={file_id}@{encoded_filename}'
        print('Image URL:', image_url)


        # 下载图片文件
        image_response = requests.get(image_url, headers={'Authorization': 'Basic ' + api_key})
        if image_response.status_code != 200:
            print(f'Failed to download image {filename}:', image_response.status_code, image_response.text)
            return

        # 将图片文件保存到本地
        with open(f'./{path}/images/{filename}', 'wb') as f:
            f.write(image_response.content)
        print(f'图片已下载并保存为 {filename}')
    else:
        print('Invalid image field value format')


def main(no, path):
    params = {'api': '', 'v': 3}
    load_dotenv()
    api_key = os.getenv('RAGIC_API_2')

    base_url = 'https://ap12.ragic.com'
    tag = "cancerfree/articles"
    sheet_id = "6"

    ENDPOINT = f'{base_url}/{tag}/{sheet_id}'
    response = requests.get(ENDPOINT, params=params, headers={'Authorization': 'Basic ' + api_key})

    response_dict = response.json()

    #print(json.dumps(response_dict, indent=4))

    record = response_dict[f'{no}']
    os.makedirs(f'{path}/images', exist_ok=True)

    image_fields = ['Image', 'Image2', 'Image3', 'Image4']
    for field in image_fields:
        if field in record:
            download_image(record[field], path, base_url, api_key)


