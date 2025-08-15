"""
API データモデル定義
Pydanticベースのリクエスト・レスポンスモデル
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class VideoAnalysisRequest(BaseModel):
    """動画解析リクエスト"""
    angle: str = Field(..., description="撮影角度 ('front' または 'side')")
    user_id: Optional[str] = Field(None, description="ユーザーID")

class CategoryScore(BaseModel):
    """カテゴリ別スコア"""
    score: float = Field(..., description="スコア (0-100)")
    percentage: float = Field(..., description="パーセンテージ")
    details: Dict[str, float] = Field(default_factory=dict, description="詳細スコア")

class ImprovementPoint(BaseModel):
    """改善ポイント"""
    category: str = Field(..., description="カテゴリ")
    priority: str = Field(..., description="優先度 (high/medium/low)")
    title: str = Field(..., description="改善点のタイトル")
    description: str = Field(..., description="詳細説明")
    advice: str = Field(..., description="具体的なアドバイス")
    training_focus: List[str] = Field(default_factory=list, description="重点練習項目")

class VideoAnalysisResponse(BaseModel):
    """動画解析レスポンス"""
    session_id: str = Field(..., description="セッションID")
    overall_score: float = Field(..., description="総合スコア (0-100)")
    category_scores: Dict[str, CategoryScore] = Field(..., description="カテゴリ別スコア")
    strengths: List[str] = Field(default_factory=list, description="長所")
    weaknesses: List[str] = Field(default_factory=list, description="弱点")
    improvement_points: List[ImprovementPoint] = Field(default_factory=list, description="改善ポイント")
    recommended_training: List[str] = Field(default_factory=list, description="推奨トレーニング")
    analysis_angle: str = Field(..., description="解析角度")
    analysis_date: datetime = Field(default_factory=datetime.now, description="解析日時")

class Exercise(BaseModel):
    """トレーニング種目"""
    name: str = Field(..., description="種目名")
    duration: int = Field(..., description="実施時間（分）")
    description: str = Field(..., description="説明")
    focus_area: str = Field(..., description="重点エリア")
    location: str = Field(..., description="実施場所 (court/home)")
    difficulty: str = Field(default="beginner", description="難易度")
    instructions: List[str] = Field(default_factory=list, description="実施手順")
    tips: List[str] = Field(default_factory=list, description="コツ")

class DailyPlan(BaseModel):
    """日別練習プラン"""
    day: int = Field(..., description="日数")
    exercises: List[str] = Field(..., description="実施種目名リスト")
    total_duration: int = Field(..., description="合計時間（分）")
    focus: str = Field(..., description="その日の重点")

class TrainingMenuResponse(BaseModel):
    """トレーニングメニューレスポンス"""
    total_duration: int = Field(..., description="総練習時間（分）")
    focus_areas: List[str] = Field(..., description="重点エリア")
    location: str = Field(..., description="実施場所")
    exercises: List[Exercise] = Field(..., description="トレーニング種目リスト")
    daily_plan: List[DailyPlan] = Field(default_factory=list, description="日別プラン")
    tips: List[str] = Field(default_factory=list, description="全般的なアドバイス")

class ScoreHistory(BaseModel):
    """スコア履歴"""
    date: datetime = Field(..., description="解析日")
    overall_score: float = Field(..., description="総合スコア")
    angle: str = Field(..., description="解析角度")
    session_id: str = Field(..., description="セッションID")

class Badge(BaseModel):
    """バッジ"""
    id: str = Field(..., description="バッジID")
    name: str = Field(..., description="バッジ名")
    description: str = Field(..., description="獲得条件")
    earned_date: datetime = Field(..., description="獲得日")
    icon: str = Field(default="🏆", description="アイコン")

class ImprovementTrend(BaseModel):
    """改善傾向"""
    category: str = Field(..., description="カテゴリ名")
    trend: str = Field(..., description="傾向 (improving/stable/declining)")
    change_rate: float = Field(..., description="変化率 (%)")
    description: str = Field(..., description="説明")

class NextLevelRequirements(BaseModel):
    """次レベル要件"""
    points_needed: int = Field(..., description="必要ポイント")
    analyses_needed: int = Field(..., description="必要解析回数")
    description: str = Field(default="", description="レベルアップの説明")

class ProgressResponse(BaseModel):
    """進捗レスポンス"""
    user_id: str = Field(..., description="ユーザーID")
    total_analyses: int = Field(..., description="総解析回数")
    current_level: int = Field(..., description="現在のレベル")
    experience_points: int = Field(..., description="経験値")
    badges: List[Badge] = Field(default_factory=list, description="獲得バッジ")
    score_history: List[ScoreHistory] = Field(default_factory=list, description="スコア履歴")
    improvement_trends: Dict[str, ImprovementTrend] = Field(default_factory=dict, description="改善傾向")
    next_level_requirements: NextLevelRequirements = Field(..., description="次レベル要件")
    last_analysis_date: Optional[datetime] = Field(None, description="最終解析日")

class TrainingMenuRequest(BaseModel):
    """トレーニングメニューリクエスト"""
    focus_areas: List[str] = Field(default_factory=list, description="重点エリア")
    location: str = Field(default="both", description="実施場所")
    duration_minutes: int = Field(default=30, description="練習時間（分）")
    skill_level: str = Field(default="beginner", description="技術レベル")

class BadgeAwardRequest(BaseModel):
    """バッジ授与リクエスト"""
    badge_id: str = Field(..., description="バッジID")
    reason: Optional[str] = Field(None, description="授与理由")

class ErrorResponse(BaseModel):
    """エラーレスポンス"""
    error_code: str = Field(..., description="エラーコード")
    message: str = Field(..., description="エラーメッセージ")
    details: Optional[Dict[str, Any]] = Field(None, description="詳細情報")
    timestamp: datetime = Field(default_factory=datetime.now, description="発生時刻")

class HealthCheckResponse(BaseModel):
    """ヘルスチェックレスポンス"""
    status: str = Field(default="healthy", description="ステータス")
    version: str = Field(..., description="APIバージョン")
    timestamp: datetime = Field(default_factory=datetime.now, description="チェック時刻")
    services: Dict[str, str] = Field(default_factory=dict, description="各サービスの状態")

# 定数
class AnalysisAngles:
    """解析角度定数"""
    FRONT = "front"
    SIDE = "side"

class Priorities:
    """優先度定数"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Locations:
    """練習場所定数"""
    COURT = "court"
    HOME = "home"
    BOTH = "both"

class SkillLevels:
    """技術レベル定数"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class FormCategories:
    """フォームカテゴリ定数"""
    STANCE = "stance"
    SWING_PATH = "swing_path"
    TIMING = "timing"
    BALANCE = "balance"
    FOLLOW_THROUGH = "follow_through"