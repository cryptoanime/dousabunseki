# 🎾 SoftTennis AI Coach

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Android API 24+](https://img.shields.io/badge/Android-API%2024+-green.svg)](https://developer.android.com/)

**軟式テニス専用AI動作分析アプリ** - 初心者向けフォーム改善とトレーニングメニュー生成

## ✨ 概要

SoftTennis AI Coachは、軟式テニス初心者のために特別に設計された動作分析アプリです。スマホで撮影した動画をアップロードするだけで、AI が詳細なフォーム分析を行い、個別の改善提案とトレーニングメニューを提供します。

### 🎯 主な特徴

- **🔬 高精度分析**: Kinovea技術を移植した軟式テニス特化の動作解析
- **📱 使いやすさ**: 初心者でも簡単に使えるAndroidアプリUI
- **🆓 完全無料**: オープンソース技術による高品質な無料アプリ
- **📊 進捗管理**: レベルシステムとバッジでモチベーション維持
- **🏠 場所を選ばない**: コートでも自宅でもできるトレーニングメニュー

## 🚀 主な機能

### 📹 動画解析
- **対応動画**: 10-30秒のMP4/MOV形式
- **撮影角度**: 正面・側面の2つのアングル
- **解析項目**: スタンス、スイング軌道、タイミング、バランス
- **追跡対象**: ボール、ラケット、身体の関節点

### 🤖 AI分析システム
- **姿勢検出**: MediaPipeによる高精度な身体追跡
- **軟式特化**: 軟式ボールの特性（変形、低バウンド）に対応
- **初心者向け**: 分かりやすい評価とアドバイス
- **図解表示**: テキストと図解による改善提案

### 💪 トレーニングメニュー
- **個別最適化**: 弱点に応じたカスタムメニュー
- **実践的練習**: 壁打ち、素振り、フットワーク等
- **場所対応**: コート練習・自宅練習の両方
- **継続サポート**: 週間スケジュールとリマインダー

### 📈 進捗追跡
- **7段階レベル**: ビギナーからレジェンドまで
- **10種バッジ**: 様々な達成項目
- **月次分析**: 改善傾向の可視化
- **履歴管理**: 過去の解析結果との比較

## 🛠 技術スタック

### フロントエンド (Android)
- **Kotlin** - モダンなAndroid開発言語
- **Jetpack Compose** - 宣言的UI
- **Material Design 3** - 美しいデザインシステム
- **CameraX** - カメラ統合
- **Navigation Component** - 画面遷移

### バックエンド (Python)
- **FastAPI** - 高性能Web API
- **MediaPipe** - AI姿勢検出
- **OpenCV** - コンピュータビジョン
- **NumPy/SciPy** - 数値計算
- **Pydantic** - データバリデーション

### AI・分析エンジン
- **Kinovea移植** - 高精度動作追跡
- **テンプレートマッチング** - ボール・ラケット追跡
- **運動学解析** - 速度・角度計算
- **軟式テニス特化モデル** - 専用評価基準

### インフラ・デプロイ
- **Docker** - コンテナ化
- **Google Cloud Platform** - クラウドホスティング
- **Firebase** - データ管理
- **GitHub Actions** - CI/CD

## 📁 プロジェクト構造

```
SoftTennisAI/
├── 📱 android/                    # Androidアプリ
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/softtennis/
│   │   │   │   ├── MainActivity.kt          # メイン画面
│   │   │   │   ├── VideoUploadActivity.kt   # 動画アップロード
│   │   │   │   └── ui/theme/                # テーマ設定
│   │   │   └── res/                         # リソース
│   │   └── build.gradle
│   └── build.gradle
├── 🧠 backend/                    # Python解析エンジン
│   ├── analysis/
│   │   ├── kinovea_engine.py               # Kinovea技術移植
│   │   ├── pose_detector.py                # 姿勢検出
│   │   ├── ball_tracker.py                 # ボール追跡
│   │   └── racket_detector.py              # ラケット検出
│   ├── ai_coach/
│   │   ├── form_analyzer.py                # フォーム分析AI
│   │   ├── training_generator.py           # メニュー生成
│   │   └── improvement_ai.py               # 改善提案
│   ├── api/
│   │   ├── main.py                         # FastAPI メイン
│   │   └── models.py                       # データモデル
│   ├── database/
│   │   └── progress_manager.py             # 進捗管理
│   ├── requirements.txt
│   └── Dockerfile
├── 🐳 docker-compose.yml            # Docker設定
├── 📋 .gitignore
└── 📖 README.md
```

## 🚀 クイックスタート

### 前提条件
- Python 3.11以上
- Android Studio (アプリ開発時)
- Docker & Docker Compose (推奨)

### バックエンド起動

```bash
# リポジトリクローン
git clone https://github.com/[username]/SoftTennisAI.git
cd SoftTennisAI

# Docker使用（推奨）
docker-compose up -d

# または手動起動
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### Androidアプリビルド

```bash
cd android
./gradlew assembleDebug
```

## 📊 使用例

### 1. 動画アップロード
```kotlin
// アップロード画面で動画選択
VideoUploadActivity.uploadVideo(
    videoUri = selectedVideoUri,
    angle = "side", // "front" or "side"
    onSuccess = { analysisResult -> 
        // 解析結果表示
    }
)
```

### 2. API呼び出し例
```python
# 動画解析API
POST /analyze/video
Content-Type: multipart/form-data

{
    "video": video_file,
    "angle": "side",
    "user_id": "user123"
}
```

### 3. 解析結果例
```json
{
    "session_id": "analysis_123",
    "overall_score": 75.5,
    "category_scores": {
        "stance": {"score": 80.0, "percentage": 80.0},
        "swing_path": {"score": 70.0, "percentage": 70.0}
    },
    "improvement_points": [
        {
            "title": "スタンス幅の改善",
            "advice": "足を肩幅程度に開き、安定した土台を作りましょう",
            "priority": "high"
        }
    ]
}
```

## 🤝 コントリビューション

SoftTennis AI Coachはオープンソースプロジェクトです。貢献を歓迎します！

### 開発の流れ
1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. Pull Requestを作成

### 貢献できる分野
- **解析精度向上**: 軟式テニス特有の動作分析改善
- **UI/UX改善**: より使いやすいアプリデザイン
- **多言語対応**: 国際化サポート
- **新機能追加**: 戦術分析、グループ機能等
- **ドキュメント**: 使い方や技術文書の充実

## 📜 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。

## 🙏 謝辞

- **Kinovea**: オープンソース動作分析ツールの先駆者
- **MediaPipe**: 高品質な姿勢検出技術
- **軟式テニス界**: 専門知識とフィードバック

## 📧 お問い合わせ

- **プロジェクト**: [GitHub Issues](https://github.com/[username]/SoftTennisAI/issues)
- **Email**: softtennis.ai@example.com

---

**🎾 軟式テニスの上達を、AIの力でサポートします！**