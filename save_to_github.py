from github import Github
import json

# GitHubのアクセストークンとリポジトリ情報
GITHUB_TOKEN = "your_github_token"  # GitHubアクセストークンをここに入力
REPO_NAME = "your_username/your_repo"  # GitHubリポジトリ名

def save_to_github(data: dict, file_path: str = "data.json"):
    # GitHubリポジトリに接続
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # 既存ファイルを取得または新規作成
    try:
        file = repo.get_contents(file_path)
        current_data = json.loads(file.decoded_content.decode())
        current_data.append(data)
        repo.update_file(file.path, "Update conversation data", json.dumps(current_data, ensure_ascii=False, indent=4), file.sha)
    except:
        # 新規ファイル作成
        repo.create_file(file_path, "Create conversation data", json.dumps([data], ensure_ascii=False, indent=4))
