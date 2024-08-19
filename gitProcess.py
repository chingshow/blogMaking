import os
from dotenv import load_dotenv
from git import Repo
import datetime


def setup_git_config(repo):
    load_dotenv()
    git_username = os.getenv('GIT_USERNAME')
    git_email = os.getenv('GIT_EMAIL')

    if not git_username or not git_email:
        raise ValueError("GIT_USERNAME or GIT_EMAIL not set in .env file")

    with repo.config_writer() as git_config:
        git_config.set_value('user', 'name', git_username)
        git_config.set_value('user', 'email', git_email)

    print(f"Git config set to: User = {git_username}, Email = {git_email}")


def auto_git_process(repo_path, commit_message):
    try:
        repo = Repo(repo_path)
        setup_git_config(repo)

        if not repo.is_dirty(untracked_files=True):
            print("No changes to commit")
            return False

        repo.git.add(A=True)
        commit = repo.index.commit(commit_message)
        print(f"Commit created: {commit.hexsha}")
        print(f"Author: {commit.author.name} <{commit.author.email}>")

        origin = repo.remote('origin')
        push_info = origin.push()

        for info in push_info:
            print(f"Push info: {info.summary}")

        print(f"Successfully added, committed, and pushed changes")
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False


if __name__ == "__main__":
    repo_path = "."  # 當前目錄
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
    commit_message = f"Article Updated {now.strftime('%Y/%m/%d %H:%M:%S')}"
    auto_git_process(repo_path, commit_message)