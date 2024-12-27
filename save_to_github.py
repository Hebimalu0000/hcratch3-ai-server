import os
import json
import subprocess

REPO_URL = "https://github.com/Hebimalu0000/hcratch3-ai-brain.git"  # 使用するGitHubリポジトリのURL
LOCAL_REPO_DIR = "/tmp/hcratch3-ai-brain"  # ローカルにクローンするディレクトリ

def clone_repo():
    if not os.path.exists(LOCAL_REPO_DIR):
        subprocess.run(["git", "clone", REPO_URL, LOCAL_REPO_DIR])

def save_to_github(data: dict, file_path: str = "data.json"):
    # リポジトリをクローン
    clone_repo()

    # 保存するファイルパス
    file_full_path = os.path.join(LOCAL_REPO_DIR, file_path)

    # クローンしたリポジトリのdata.jsonを更新
    try:
        with open(file_full_path, "r") as f:
            current_data = json.load(f)
        current_data.append(data)
    except FileNotFoundError:
        current_data = [data]

    # 更新したデータをファイルに書き込む
    with open(file_full_path, "w") as f:
        json.dump(current_data, f, ensure_ascii=False, indent=4)

    # Git操作
    os.chdir(LOCAL_REPO_DIR)

    # Gitの設定（GitHub Actionsユーザー）
    subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions"])
    subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"])

    # 変更をステージング
    subprocess.run(["git", "add", file_path])

    # コミット
    subprocess.run(["git", "commit", "-m", "Update conversation data"])

    # プッシュ（公開リポジトリの場合、認証なしで可能）
    subprocess.run(["git", "push", REPO_URL])
