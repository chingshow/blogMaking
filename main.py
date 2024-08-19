import shutil
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from os import listdir
import json

from gitProcess import auto_git_process
import getRagicData
import gitMake
import fileInit
import checkTxt
import datetime
import oneBlogDatas
import oneBlogImages
import getRagicContents
import finishUpdate


def project_exists_locally(project_name, base_path):
    project_path = os.path.join(base_path, project_name)
    return os.path.exists(project_path)


def main():
    print(open("./CRM/documents/txt/253.md").read())
    # get ragic
    n = getRagicData.main()

    with open('content_all.json', 'r', encoding='utf-8') as file:
        datas = json.load(file)
    dict_iter = iter(datas)

    while True:
        try:
            key = next(dict_iter)
            dataTitle = datas[key]["Website tag"]
            # 新海報長新網站(init)
            if not project_exists_locally(dataTitle, "."):
                gitMake.main(dataTitle)
                fileInit.main(f"./{dataTitle}")

            # get
            # 生content.json .txt .md
            oneBlogDatas.main(key, dataTitle)

            # add ./images
            oneBlogImages.main(key, dataTitle)

            getRagicContents.main(dataTitle)
            # add .
            # push
            now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
            repo_path = f"./{dataTitle}"
            commit_message = f"Article Updated {now.strftime('%Y/%m/%d %H:%M:%S')}"

            success = auto_git_process(repo_path, commit_message)
            if success:
                print("Git process completed successfully")
            else:
                print("Git process failed or no changes to commit")

            print(datas[key]["_ragicId"])

        except StopIteration:
            break


main()

