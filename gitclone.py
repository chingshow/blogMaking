import subprocess
import os

def clone_github_repo(destination_folder, repo_name, username):
    repo_url = f"https://github.com/{username}/{repo_name}.git"
    try:
        if destination_folder:
            os.makedirs(destination_folder, exist_ok=True)
            os.chdir(destination_folder)

        subprocess.check_call(['git', 'clone', repo_url])
        print(f"成功克隆倉庫: {repo_url}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"克隆倉庫時發生錯誤: {e}")
        return False
    except Exception as e:
        print(f"發生未知錯誤: {e}")
        return False