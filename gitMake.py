import os
from dotenv import load_dotenv
import requests
from git import Repo
import re
import shutil

'''# GitHub API 設置
github_api_url = "https://api.github.com"
load_dotenv()
github_token = os.getenv('GITHUB_TOKEN')
github_username = os.getenv('GIT_USERNAME')
headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json"
}'''

def create_github_repo(github_api_url, headers, repo_name):
    """使用 GitHub API 創建新的遠程倉庫"""
    data = {"name": repo_name, "auto_init": True}
    response = requests.post(f"{github_api_url}/user/repos", headers=headers, json=data)
    if response.status_code == 201:
        return response.json()["clone_url"]
    else:
        raise Exception(f"Failed to create repo: {response.content}")

def setup_git_config(repo, git_username, git_email, github_token):
    """設置 Git 配置"""
    """git_username = os.getenv('GIT_USERNAME')
    git_email = os.getenv('GIT_EMAIL')"""
    with repo.config_writer() as git_config:
        git_config.set_value('user', 'name', git_username)
        git_config.set_value('user', 'email', git_email)

def setup_local_repo(repo_name, remote_url, git_username, git_email, github_token):
    """設置本地倉庫並連接到遠程"""
    local_path = os.path.join(os.getcwd(), repo_name)
    # 使用帶有認證的 URL 進行克隆
    auth_remote_url = re.sub(r'https://', f'https://{git_username}:{github_token}@', remote_url)
    repo = Repo.clone_from(auth_remote_url, local_path)
    setup_git_config(repo, git_username, git_email, github_token)
    return repo

def main(title, git_username, git_email, github_token):
    github_api_url = "https://api.github.com"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    print(title)
    # 創建新的 GitHub 倉庫
    remote_url = create_github_repo(github_api_url, headers, title)
    print(f"Created new repo: {remote_url}")

    # 設置本地倉庫
    repo = setup_local_repo(title, remote_url, git_username, git_email, github_token)
    print(f"Local repo set up at: {repo.working_dir}")
    print(f"Remote URL: {repo.remote('origin').url}")

    return repo.working_dir

if __name__ == "__main__":
    repo_title = input("Enter the repository name: ")
    main(repo_title)