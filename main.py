import shutil
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from os import listdir
import json

import getRagicContents
from gitProcess import auto_git_process
import getRagicData
import gitMake
import fileInit
import checkTxt
import datetime
import finishUpdate


def project_exists_locally(project_name, base_path):
    project_path = os.path.join(base_path, project_name)
    return os.path.exists(project_path)


def main():
    # get ragic
    n = getRagicData.main()
    files = listdir(".")
    folders = [item for item in files if os.path.isdir(os.path.join(".", item))]
    with open('content_all.json', 'r', encoding='utf-8') as file:
        datas = json.load(file)

    sites = []
    dict_iter = iter(datas)

    while True:
        try:
            key = next(dict_iter)
            if datas[key]["有改動"] == "Yes" and datas[key]["已確認"] == "Yes":
                dataTitle = datas[key]["Website"]
                if dataTitle not in sites:
                    # print(dataTitle)
                    sites.append(dataTitle)
                # 新海報長新網站(init)
                if not project_exists_locally(dataTitle, "."):
                    gitMake.main(dataTitle)
                    fileInit.main(f"./{dataTitle}")
        except StopIteration:
            break

    for site in sites:
        print(site)
        # get
        # 生content.json .txt .md
        getRagicContents.main(site)
        # checktxt...
        checkTxt.main(site)
        # add .
        # push
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        repo_path = f"./{site}"
        commit_message = f"Article Updated {now.strftime('%Y/%m/%d %H:%M:%S')}"
        print(repo_path)

        success = auto_git_process(repo_path, commit_message)
        if success:
            print("Git process completed successfully")
        else:
            print("Git process failed or no changes to commit")

    dict_iter = iter(datas)
    while True:
        try:
            key = next(dict_iter)
            if datas[key]["有改動"] == "Yes":
                print(key)
                finishUpdate.main(datas[key]["_ragicId"])
        except StopIteration:
            break


if __name__ == "__main__":
    main()

