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
import datetime
import oneBlogDatas
import oneBlogImages
import getRagicContents



def project_exists_locally(project_name, base_path):
    project_path = os.path.join(base_path, project_name)
    return os.path.exists(project_path)


def main():
    # get ragic
    n = getRagicData.main()

    with open('content_all.json', 'r', encoding='utf-8') as file:
        datas = json.load(file)
    dict_iter = iter(datas)

    while True:
        try:
            key = next(dict_iter)
            dataTitle = datas[key]["Website tag"]

            if datas[key]['user name'] != "" and datas[key]['email'] != "" and datas[key]['github token'] != "":
                git_username = datas[key]['user name']
                git_email = datas[key]['email']
                github_token = datas[key]['github token']
            else:
                load_dotenv()
                git_username = os.getenv('GIT_USERNAME')
                git_email = os.getenv('GIT_EMAIL')
                github_token = os.getenv('GITHUB_TOKEN')

            # 新海報長新網站(init)
            if not project_exists_locally(dataTitle, "."):
                gitMake.main(dataTitle, git_username, git_email, github_token)
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

            success = auto_git_process(repo_path, commit_message, git_username, git_email, github_token)
            if success:
                print("Git process completed successfully")
            else:
                print("Git process failed or no changes to commit")

            print(datas[key]["_ragicId"])

        except StopIteration:
            break


main()

