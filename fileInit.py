import os
from git import Repo
import shutil


def main(repo_path):
    # 檢查倉庫是否存在
    if not os.path.exists(repo_path):
        raise Exception(f"Repository not found at {repo_path}")

    # 打開現有的倉庫
    repo = Repo(repo_path)
    print(f"Opened existing repo at: {repo.working_dir}")

    # 確保工作目錄是乾淨的
    if repo.is_dirty():
        print("Warning: Repository has uncommitted changes")

    # 定義要複製的文件列表
    files_to_copy = ["./script.js",
                     ".gitignore",
                     "./index.html",
                     "intro.html",
                     "./styles.css",
                     "./documents/ad_init.png"]

    # 複製文件到倉庫
    for file_path in files_to_copy:
        if os.path.exists(file_path):
            destination = os.path.join(repo.working_dir, os.path.basename(file_path))
            shutil.copy2(file_path, destination)
            print(f"Copied {file_path} to {destination}")
        else:
            print(f"File not found: {file_path}")

    dirMake = ["documents", "images"]

    for dirs in dirMake:
        subfolder_path = os.path.join(repo.working_dir, dirs)
        os.makedirs(subfolder_path, exist_ok=True)
        if dirs == "documents":
            print(repo.working_dir, subfolder_path)
            destination = os.path.join(repo.working_dir, os.path.basename("./documents"))
            print(destination)
            shutil.copy2("./documents/styles2.css", subfolder_path)
            shutil.copy2("./documents/script_articles.js", subfolder_path)

            subfolder_path = os.path.join(subfolder_path, "txt")
            os.makedirs(subfolder_path, exist_ok=True)

        print(f"Created subfolder: {subfolder_path}")


if __name__ == "__main__":
    repo_path = "./Avater Medicine 2023"
    main(repo_path)
