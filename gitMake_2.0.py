import os
from dotenv import load_dotenv
import requests
from git import Repo
import re
import shutil

# GitHub API 設置
github_api_url = "https://api.github.com"
load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')
headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}


def create_github_repo(repo_name):
    """使用 GitHub API 創建新的遠程倉庫"""
    data = {"name": repo_name, "auto_init": True}
    response = requests.post(f"{github_api_url}/user/repos", headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["ssh_url"]  # 使用 SSH URL 而不是 clone_url
    else:
        raise Exception(f"Failed to create repo: {response.content}")


def setup_git_config(repo):
    """設置 Git 配置"""
    git_username = os.getenv('GIT_USERNAME')
    git_email = os.getenv('GIT_EMAIL')
    with repo.config_writer() as git_config:
        git_config.set_value('user', 'name', git_username)
        git_config.set_value('user', 'email', git_email)


def setup_local_repo(repo_name, remote_url):
    """設置本地倉庫並連接到遠程"""
    local_path = os.path.join(os.getcwd(), repo_name)
    repo = Repo.clone_from(remote_url, local_path)
    setup_git_config(repo)
    return repo


def main(title):
    github_api_url = "https://api.github.com"
    load_dotenv()
    github_token = os.getenv('GITHUB_TOKEN')
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    print(title)
    # 創建新的 GitHub 倉庫
    remote_url = create_github_repo(title)
    print(f"Created new repo: {remote_url}")

    # 設置本地倉庫
    repo = setup_local_repo(title, remote_url)
    print(f"Local repo set up at: {repo.working_dir}")

