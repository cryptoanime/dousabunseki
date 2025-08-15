# 🎾 SoftTennis AI Coach - Web Application

軟式テニス専用AI動作分析Webアプリケーション

## 📱 Web版の特徴

- **ブラウザで動作**: インストール不要でどのデバイスからでもアクセス可能
- **レスポンシブデザイン**: スマートフォン、タブレット、PCに対応
- **軟式テニス特化**: 軟式テニスの特性に最適化されたAI解析
- **リアルタイム解析**: 動画アップロード後、数秒で詳細な分析結果を表示
- **完全無料**: すべての機能を無料で利用可能

## 🚀 機能一覧

### 1. 動画解析機能 (`/upload`)
- ドラッグ&ドロップでの簡単アップロード
- 撮影角度選択（正面・側面）
- リアルタイム解析進捗表示
- 詳細なフォーム分析結果

### 2. 解析結果表示 (`/analysis`)
- 総合スコア表示（100点満点）
- カテゴリ別評価（スタンス、スイング軌道、タイミング、バランス）
- 改善ポイントの詳細説明
- 具体的な練習アドバイス

### 3. トレーニングメニュー (`/training`)
- AI生成のパーソナライズされたトレーニング
- コート練習とホーム練習の両方に対応
- インタラクティブなトレーニング実行
- リアルタイム進捗追跡

### 4. 進捗確認 (`/progress`)
- 週別スコア推移グラフ
- レーダーチャートによる能力可視化
- 実績バッジシステム
- 詳細な活動履歴

## 🛠 技術スタック

### フロントエンド
- **Next.js 14**: Reactベースのフルスタックフレームワーク
- **Material-UI (MUI)**: Googleマテリアルデザインコンポーネント
- **Framer Motion**: 滑らかなアニメーション
- **TypeScript**: 型安全性の確保
- **React Query**: 効率的なデータフェッチ

### UI/UXライブラリ
- **react-dropzone**: ドラッグ&ドロップファイルアップロード
- **recharts**: データ可視化（グラフ・チャート）
- **Material-UI Icons**: 豊富なアイコンセット

### 軟式テニス専用テーマ
```typescript
const softTennisTheme = createTheme({
  palette: {
    primary: { main: '#1565C0' }, // テニスブルー
    secondary: { main: '#4CAF50' }, // テニスグリーン
    warning: { main: '#FF9800' }, // エネルギッシュオレンジ
  }
})
```

## 📦 セットアップ

### 前提条件
- Node.js 18以上
- npm または yarn

### インストール
```bash
cd webapp
npm install
```

### 開発サーバー起動
```bash
npm run dev
```

ブラウザで `http://localhost:3000` にアクセス

### プロダクションビルド
```bash
npm run build
npm start
```

## 🌐 デプロイ

### Vercel（推奨）
```bash
# Vercel CLIインストール
npm i -g vercel

# デプロイ
vercel
```

### その他のプラットフォーム
- **Netlify**: `npm run build` 後に `out` フォルダをデプロイ
- **AWS Amplify**: GitHubリポジトリと連携
- **Firebase Hosting**: `firebase deploy`

## 🔧 環境変数

`.env.local` ファイルを作成:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📱 レスポンシブデザイン

### ブレークポイント
- **モバイル**: < 600px
- **タブレット**: 600px - 960px
- **デスクトップ**: > 960px

### 対応機能
- タッチ操作最適化
- モバイルファーストデザイン
- 可変レイアウト
- 高解像度ディスプレイ対応

## 🎨 デザインシステム

### カラーパレット
- **プライマリー**: #1565C0 (テニスブルー)
- **セカンダリー**: #4CAF50 (テニスグリーン)
- **アクセント**: #FF9800 (エネルギッシュオレンジ)

### タイポグラフィ
- **見出し**: Roboto, 600-700 font-weight
- **本文**: -apple-system, BlinkMacSystemFont
- **日本語**: ヒラギノ角ゴ, メイリオ対応

## 🔄 バックエンド連携

### API エンドポイント
- `POST /analyze/video`: 動画解析
- `GET /analysis/{session_id}`: 解析結果取得
- `GET /training/recommendations`: トレーニング推奨
- `GET /progress/{user_id}`: 進捗データ

### データフロー
```
ユーザー動画アップロード
    ↓
フロントエンド (Next.js)
    ↓
バックエンドAPI (FastAPI)
    ↓
AI解析エンジン (Python)
    ↓
結果返却 & 表示
```

## 📊 パフォーマンス最適化

### 実装済み最適化
- **Code Splitting**: ページ単位の自動分割
- **Image Optimization**: Next.js Image コンポーネント
- **Bundle Analysis**: webpack-bundle-analyzer
- **Lazy Loading**: 遅延読み込み
- **Caching**: React Query による効率的キャッシュ

### パフォーマンス指標
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1

## 🧪 テスト

### テスト実行
```bash
npm test
npm run test:e2e
```

### テスト構成
- **Unit Tests**: Jest + React Testing Library
- **E2E Tests**: Playwright
- **Visual Tests**: Storybook

## 🔒 セキュリティ

### 実装済みセキュリティ
- **HTTPS強制**: プロダクション環境
- **CSP**: Content Security Policy
- **CORS**: Cross-Origin Resource Sharing設定
- **ファイル検証**: 動画ファイル形式・サイズ制限
- **Rate Limiting**: API呼び出し制限

## 📈 監視・分析

### 実装予定
- **Google Analytics**: ユーザー行動分析
- **Sentry**: エラートラッキング
- **Lighthouse CI**: パフォーマンス監視

## 🤝 コントリビューション

1. フォークしてブランチ作成
2. 機能開発・バグ修正
3. テスト実行
4. プルリクエスト作成

## 📄 ライセンス

MIT License - 詳細は [LICENSE](../LICENSE) を参照

## 🆘 サポート

- **Issues**: GitHubでのバグ報告・機能要望
- **Discord**: リアルタイムサポート
- **Email**: support@softtennis-ai.com

---

**🎾 軟式テニス上達への道を、AIと一緒に歩もう！**