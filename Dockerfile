# より小さなベースイメージを使う
FROM python:3.9-alpine

WORKDIR /app

# 必要な依存関係のみをインストール
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# 不要なファイルを削除する
RUN rm -rf /root/.cache

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
