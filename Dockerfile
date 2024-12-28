# より小さなベースイメージを使う
FROM python:3.9-alpine

WORKDIR /app

# 必要な依存関係のみをインストール
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

# 不要なファイルを削除する
RUN rm -rf /root/.cache

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
