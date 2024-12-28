# Pythonベースイメージ
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なライブラリをインストール
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# アプリケーションコードをコピー
COPY app /app

# FastAPIアプリを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
