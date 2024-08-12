import os
from dotenv import load_dotenv
from git import Repo
import datetime
import threading

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Push operation timed out")


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


from git import Repo, RemoteProgress
import datetime
import time

def auto_git_process(repo_path, commit_message, retries=3, timeout=30):
    try:
        repo = Repo(repo_path)
        setup_git_config(repo)

        if not repo.is_dirty(untracked_files=True):
            print(f"No changes to commit in {repo_path}")
            return False

        repo.git.add(A=True)
        commit = repo.index.commit(commit_message)
        print(f"Commit created: {commit.hexsha}")
        print(f"Author: {commit.author.name} <{commit.author.email}>")

        origin = repo.remote('origin')

        def raise_timeout_exception():
            raise TimeoutException("Push operation timed out")

        for attempt in range(1, retries + 1):
            timer = threading.Timer(timeout, raise_timeout_exception)
            try:
                timer.start()
                push_info = origin.push()
                timer.cancel()  # 推送成功，取消超時計時
                for info in push_info:
                    print(f"Push info: {info.summary}")
                print(f"Successfully pushed changes from {repo_path} on attempt {attempt}")
                return True
            except TimeoutException:
                print(f"Push operation timed out after {timeout} seconds")
            except Exception as push_error:
                print(f"Attempt {attempt} failed to push {repo_path}: {str(push_error)}")
                if attempt < retries:
                    time.sleep(2)  # 等待幾秒再重試
                else:
                    print(f"Failed to push changes from {repo_path} after {retries} attempts")
                    return False
            finally:
                timer.cancel()

    except Exception as e:
        print(f"An error occurred in {repo_path}: {str(e)}")
        return False


if __name__ == "__main__":
    repo_path = "."  # 當前目錄
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
    commit_message = f"Article Updated {now.strftime('%Y/%m/%d %H:%M:%S')}"
    auto_git_process(repo_path, commit_message)