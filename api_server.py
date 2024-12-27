import streamlit as st
from model import generate_response
from save_to_github import save_to_github
import json
from datetime import datetime
import os

# 使用状況を記録するファイル
LOG_FILE = "api_usage.json"

# 初期化
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump({"requests": 0, "success": 0, "failures": 0, "logs": []}, f)

# APIリクエストハンドラ
st.title("AI API Server")

# エンドポイント: /api
if "api" in st.experimental_get_query_params():
    st.write("### AI API Endpoint")
    # クエリパラメータを取得
    query_params = st.experimental_get_query_params()
    prompt = query_params.get("prompt", [""])[0]

    if prompt:
        try:
            response = generate_response(prompt)
            st.json({"status": "success", "response": response})

            # 会話データをGitHubに保存
            conversation_data = {"prompt": prompt, "response": response}
            save_to_github(conversation_data)

            # ログ更新
            with open(LOG_FILE, "r+") as f:
                data = json.load(f)
                data["requests"] += 1
                data["success"] += 1
                data["logs"].append({"timestamp": datetime.now().isoformat(), "prompt": prompt, "response": response})
                f.seek(0)
                json.dump(data, f, indent=4)
        except Exception as e:
            st.json({"status": "failure", "error": str(e)})

            # ログ更新
            with open(LOG_FILE, "r+") as f:
                data = json.load(f)
                data["requests"] += 1
                data["failures"] += 1
                f.seek(0)
                json.dump(data, f, indent=4)
    else:
        st.json({"status": "failure", "error": "No prompt provided."})

# ホーム画面
else:
    st.write("### API Usage Dashboard")

    # 使用状況データをロード
    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    # グラフ表示
    st.write("#### API Request Statistics")
    st.bar_chart({"Requests": [data["requests"]], "Success": [data["success"]], "Failures": [data["failures"]]})

    # 使用例の表示
    st.write("#### Recent Logs")
    st.json(data["logs"][-5:])  # 最新5件を表示
