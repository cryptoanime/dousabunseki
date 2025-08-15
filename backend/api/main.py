"""
軟式テニスAIコーチ - メインAPIエンドポイント
FastAPIベースのREST API
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
import os
import tempfile
from typing import Optional
import logging

from .models import (
    VideoAnalysisRequest, 
    VideoAnalysisResponse, 
    TrainingMenuResponse,
    ProgressResponse
)
from ..analysis.kinovea_engine import SoftTennisKinoveaEngine, AnalysisAngle
from ..ai_coach.form_analyzer import SoftTennisFormAnalyzer
from ..ai_coach.training_generator import TrainingMenuGenerator
from ..database.progress_manager import ProgressManager

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPIアプリケーション初期化
app = FastAPI(
    title="SoftTennis AI Coach API",
    description="軟式テニス専用動作解析・フォーム改善API",
    version="1.0.0"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# コンポーネント初期化
kinovea_engine = SoftTennisKinoveaEngine()
form_analyzer = SoftTennisFormAnalyzer()
training_generator = TrainingMenuGenerator()
progress_manager = ProgressManager()

@app.get("/")
async def root():
    """ヘルスチェック"""
    return {"message": "SoftTennis AI Coach API is running", "version": "1.0.0"}

@app.post("/analyze/video", response_model=VideoAnalysisResponse)
async def analyze_video(
    background_tasks: BackgroundTasks,
    video: UploadFile = File(...),
    angle: str = "side",  # "front" or "side"
    user_id: Optional[str] = None
):
    """
    動画解析エンドポイント
    
    Args:
        video: アップロードされた動画ファイル
        angle: 撮影角度 ("front" または "side")
        user_id: ユーザーID（進捗追跡用）
    
    Returns:
        VideoAnalysisResponse: 解析結果
    """
    
    # バリデーション
    if not video.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="動画ファイルのみ対応しています")
    
    if angle not in ["front", "side"]:
        raise HTTPException(status_code=400, detail="角度は 'front' または 'side' を指定してください")
    
    # 動画の長さチェック（実装簡略化）
    file_size = 0
    content = await video.read()
    file_size = len(content)
    
    # 30MBを超える場合はエラー（約30秒の動画想定）
    if file_size > 30 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="動画ファイルが大きすぎます（30MB以下にしてください）")
    
    # 一意のセッションIDを生成
    session_id = str(uuid.uuid4())
    
    try:
        # 一時ファイルに保存
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            temp_file.write(content)
            temp_video_path = temp_file.name
        
        logger.info(f"動画解析開始: session_id={session_id}, angle={angle}")
        
        # 解析実行
        analysis_angle = AnalysisAngle.FRONT if angle == "front" else AnalysisAngle.SIDE
        kinovea_result = kinovea_engine.analyze_video(temp_video_path, analysis_angle)
        
        # フォーム分析
        form_report = form_analyzer.analyze_form(kinovea_result, analysis_angle)
        
        # レスポンス生成
        response = VideoAnalysisResponse(
            session_id=session_id,
            overall_score=form_report.overall_score,
            category_scores={
                category.value: {
                    "score": score.score,
                    "percentage": score.percentage,
                    "details": score.details or {}
                }
                for category, score in form_report.category_scores.items()
            },
            strengths=form_report.strengths,
            weaknesses=form_report.weaknesses,
            improvement_points=[
                {
                    "category": point.category.value,
                    "priority": point.priority,
                    "title": point.title,
                    "description": point.description,
                    "advice": point.specific_advice,
                    "training_focus": point.training_focus
                }
                for point in form_report.improvement_points
            ],
            recommended_training=form_report.recommended_training,
            analysis_angle=angle
        )
        
        # バックグラウンドで進捗保存
        if user_id:
            background_tasks.add_task(
                save_analysis_progress, 
                user_id, 
                session_id, 
                form_report.overall_score,
                angle
            )
        
        # 一時ファイル削除
        background_tasks.add_task(cleanup_temp_file, temp_video_path)
        
        logger.info(f"動画解析完了: session_id={session_id}, score={form_report.overall_score:.1f}")
        
        return response
        
    except Exception as e:
        logger.error(f"動画解析エラー: {str(e)}")
        # 一時ファイルが残っている場合は削除
        if 'temp_video_path' in locals():
            try:
                os.unlink(temp_video_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"解析中にエラーが発生しました: {str(e)}")

@app.get("/training/menu", response_model=TrainingMenuResponse)
async def get_training_menu(
    focus_areas: str = "all",  # カンマ区切りの改善エリア
    location: str = "both",    # "court", "home", "both"
    duration: int = 30         # 練習時間（分）
):
    """
    トレーニングメニュー取得
    
    Args:
        focus_areas: 重点練習エリア（例: "stance,swing_path"）
        location: 練習場所
        duration: 練習時間
    
    Returns:
        TrainingMenuResponse: トレーニングメニュー
    """
    
    try:
        # フォーカスエリアの解析
        focus_list = [area.strip() for area in focus_areas.split(",")] if focus_areas != "all" else []
        
        # トレーニングメニュー生成
        menu = training_generator.generate_menu(
            focus_areas=focus_list,
            location=location,
            duration_minutes=duration
        )
        
        response = TrainingMenuResponse(
            total_duration=duration,
            focus_areas=focus_list or ["all"],
            location=location,
            exercises=menu.exercises,
            daily_plan=menu.daily_plan,
            tips=menu.tips
        )
        
        return response
        
    except Exception as e:
        logger.error(f"トレーニングメニュー生成エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"メニュー生成中にエラーが発生しました: {str(e)}")

@app.get("/progress/{user_id}", response_model=ProgressResponse)
async def get_user_progress(user_id: str):
    """
    ユーザー進捗取得
    
    Args:
        user_id: ユーザーID
    
    Returns:
        ProgressResponse: 進捗データ
    """
    
    try:
        progress_data = progress_manager.get_user_progress(user_id)
        
        if not progress_data:
            # 新規ユーザーの場合はデフォルトデータを返す
            return ProgressResponse(
                user_id=user_id,
                total_analyses=0,
                current_level=1,
                experience_points=0,
                badges=[],
                score_history=[],
                improvement_trends={},
                next_level_requirements={
                    "points_needed": 100,
                    "analyses_needed": 5
                }
            )
        
        return ProgressResponse(**progress_data)
        
    except Exception as e:
        logger.error(f"進捗取得エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"進捗取得中にエラーが発生しました: {str(e)}")

@app.post("/progress/{user_id}/badge")
async def award_badge(user_id: str, badge_id: str):
    """
    バッジ授与
    
    Args:
        user_id: ユーザーID
        badge_id: バッジID
    """
    
    try:
        success = progress_manager.award_badge(user_id, badge_id)
        
        if success:
            return {"message": f"バッジ '{badge_id}' を授与しました", "success": True}
        else:
            return {"message": "バッジ授与に失敗しました", "success": False}
            
    except Exception as e:
        logger.error(f"バッジ授与エラー: {str(e)}")
        raise HTTPException(status_code=500, detail=f"バッジ授与中にエラーが発生しました: {str(e)}")

# バックグラウンドタスク
async def save_analysis_progress(user_id: str, session_id: str, score: float, angle: str):
    """解析結果を進捗として保存"""
    try:
        progress_manager.add_analysis_record(
            user_id=user_id,
            session_id=session_id,
            score=score,
            angle=angle
        )
        logger.info(f"進捗保存完了: user_id={user_id}, score={score}")
    except Exception as e:
        logger.error(f"進捗保存エラー: {str(e)}")

async def cleanup_temp_file(file_path: str):
    """一時ファイル削除"""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
            logger.info(f"一時ファイル削除: {file_path}")
    except Exception as e:
        logger.error(f"一時ファイル削除エラー: {str(e)}")

# エラーハンドラー
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """一般的な例外ハンドラー"""
    logger.error(f"予期しないエラー: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "内部サーバーエラーが発生しました"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)