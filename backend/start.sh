#!/bin/bash

# 軟式テニスAIコーチ バックエンド起動スクリプト

echo "🎾 SoftTennis AI Coach バックエンド起動中..."

# 環境変数の設定
export PYTHONPATH="${PYTHONPATH}:/app"
export ENVIRONMENT=${ENVIRONMENT:-development}
export LOG_LEVEL=${LOG_LEVEL:-info}

# データディレクトリの作成
mkdir -p /app/uploads
mkdir -p /app/data
mkdir -p /app/logs

# 依存関係の確認
echo "依存関係を確認中..."
python -c "import cv2, mediapipe, numpy, fastapi; print('✅ 主要な依存関係が正常にインストールされています')"

# データベースの初期化（必要に応じて）
if [ ! -f "/app/data/user_progress.json" ]; then
    echo "初期データファイルを作成中..."
    echo "{}" > /app/data/user_progress.json
fi

# ログ設定
echo "ログ設定を初期化中..."
python -c "
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/app.log'),
        logging.StreamHandler()
    ]
)
"

echo "🚀 サーバーを起動しています..."

# FastAPIサーバーの起動
if [ "$ENVIRONMENT" = "production" ]; then
    echo "本番モードで起動..."
    exec uvicorn api.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --workers 4 \
        --log-level $LOG_LEVEL \
        --access-log \
        --log-config logging.conf
else
    echo "開発モードで起動..."
    exec uvicorn api.main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload \
        --log-level $LOG_LEVEL
fi