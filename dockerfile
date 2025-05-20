# Dockerfile (もっともシンプルな Python ETL イメージ例)
FROM python:3.10-slim

WORKDIR /app

# 依存リストだけ先にコピーしてキャッシュ活用
COPY requirements.txt .

# グローバルにインストール（コンテナ隔離済みなので問題なし）
RUN pip install --no-cache-dir -r requirements.txt

# アプリコードを全コピー
COPY . .

# 環境変数（Compose / Kubernetes 等から上書き可能）
ENV MYSQL_HOST=mysql \
    MYSQL_PORT=3306 \
    MYSQL_USER=user \
    MYSQL_PASSWORD=pass \
    MYSQL_DATABASE=dbname

# 単純にスクリプトを実行
CMD ["python", "etl.py"]
