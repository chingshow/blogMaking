import shutil
import time

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from os import listdir
import json
import stat
import subprocess

from gitProcess import auto_git_process
import getRagicData
import gitMake
import fileInit
import gitclone
import datetime
import oneBlogDatas
import oneBlogImages
import getRagicContents
import finishUpdate


def project_exists_locally(project_name, base_path):
    project_path = os.path.join(base_path, project_name)
    return os.path.exists(project_path)


def check_repo_exists(owner, repo, token):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(f"{repo} is available")
        return True
    elif response.status_code == 404:
        print(f"{repo} is not available or doesn't exist")
        return False
    else:
        print(f"error: {response.status_code}")
        return None


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
                dataTitle = dataTitle.replace(" ", "-")
                if not check_repo_exists(git_username, dataTitle, github_token):
                    gitMake.main(dataTitle, git_username, git_email, github_token)
                    fileInit.main(f"./{dataTitle}")
                else:
                    gitclone.clone_github_repo(None, dataTitle, git_username)

            # get
            # 生content.json
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

            def on_rm_error(func, path, exc_info):
                # 檢查是否有權限錯誤
                if not os.access(path, os.W_OK):
                    # 嘗試更改文件權限
                    os.chmod(path, stat.S_IWUSR)
                    # 重試刪除
                    func(path)
                else:
                    raise

            def delete_folder(folder_path):
                try:
                    # 如果是 Git 倉庫，先嘗試清理 Git 相關文件
                    if os.path.exists(os.path.join(folder_path, '.git')):
                        try:
                            subprocess.run(['git', 'clean', '-fxd'], cwd=folder_path, check=True,
                                           stderr=subprocess.DEVNULL)
                        except subprocess.CalledProcessError:
                            print(f"無法清理 Git 倉庫，將嘗試直接刪除")

                    # 使用 shutil.rmtree 刪除資料夾，並使用自定義的錯誤處理函數
                    shutil.rmtree(folder_path, onerror=on_rm_error)
                    print(f"成功刪除資料夾: {folder_path}")
                    return True
                except FileNotFoundError:
                    print(f"資料夾不存在: {folder_path}")
                    return False
                except PermissionError:
                    print(f"沒有權限刪除資料夾: {folder_path}")
                    return False
                except Exception as e:
                    print(f"刪除資料夾時發生錯誤: {e}")
                    return False
            time.sleep(1)
            delete_folder(f"./{dataTitle}")

        except StopIteration:
            break

    with open('content_article.json', 'r', encoding="utf-8") as fJson:
        datas = json.load(fJson)

    dict_iter = iter(datas)
    while True:
        try:
            key = next(dict_iter)
            if datas[key]["有改動"] == "Yes":
                finishUpdate.main(datas[key]["_ragicId"])
        except StopIteration:
            break


if __name__ == "__main__":
    main()

