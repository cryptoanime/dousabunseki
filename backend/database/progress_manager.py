"""
進捗管理・レベルシステム
ユーザーの上達過程を追跡し、モチベーション維持をサポート
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import uuid

@dataclass
class AnalysisRecord:
    """解析記録"""
    session_id: str
    date: datetime
    overall_score: float
    angle: str  # "front" or "side"
    category_scores: Dict[str, float] = None
    
    def to_dict(self):
        return {
            "session_id": self.session_id,
            "date": self.date.isoformat(),
            "overall_score": self.overall_score,
            "angle": self.angle,
            "category_scores": self.category_scores or {}
        }

@dataclass
class Badge:
    """バッジ"""
    id: str
    name: str
    description: str
    earned_date: datetime
    icon: str = "🏆"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "earned_date": self.earned_date.isoformat(),
            "icon": self.icon
        }

@dataclass
class UserProgress:
    """ユーザー進捗"""
    user_id: str
    total_analyses: int = 0
    current_level: int = 1
    experience_points: int = 0
    analysis_records: List[AnalysisRecord] = None
    badges: List[Badge] = None
    created_date: datetime = None
    last_analysis_date: Optional[datetime] = None
    
    def __post_init__(self):
        if self.analysis_records is None:
            self.analysis_records = []
        if self.badges is None:
            self.badges = []
        if self.created_date is None:
            self.created_date = datetime.now()

class ProgressManager:
    """進捗管理システム"""
    
    def __init__(self, data_file: str = "user_progress.json"):
        self.data_file = data_file
        self.progress_data = self._load_data()
        self.level_requirements = self._define_level_requirements()
        self.badge_definitions = self._define_badges()
    
    def _load_data(self) -> Dict[str, UserProgress]:
        """データファイルから進捗データを読み込み"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                progress_dict = {}
                for user_id, user_data in data.items():
                    # datetime変換
                    user_data['created_date'] = datetime.fromisoformat(user_data['created_date'])
                    if user_data.get('last_analysis_date'):
                        user_data['last_analysis_date'] = datetime.fromisoformat(user_data['last_analysis_date'])
                    
                    # AnalysisRecord変換
                    records = []
                    for record_data in user_data.get('analysis_records', []):
                        record_data['date'] = datetime.fromisoformat(record_data['date'])
                        records.append(AnalysisRecord(**record_data))
                    user_data['analysis_records'] = records
                    
                    # Badge変換
                    badges = []
                    for badge_data in user_data.get('badges', []):
                        badge_data['earned_date'] = datetime.fromisoformat(badge_data['earned_date'])
                        badges.append(Badge(**badge_data))
                    user_data['badges'] = badges
                    
                    progress_dict[user_id] = UserProgress(**user_data)
                
                return progress_dict
            except Exception as e:
                print(f"データ読み込みエラー: {e}")
                return {}
        
        return {}
    
    def _save_data(self):
        """データファイルに進捗データを保存"""
        try:
            save_data = {}
            for user_id, progress in self.progress_data.items():
                user_dict = {
                    "user_id": progress.user_id,
                    "total_analyses": progress.total_analyses,
                    "current_level": progress.current_level,
                    "experience_points": progress.experience_points,
                    "created_date": progress.created_date.isoformat(),
                    "last_analysis_date": progress.last_analysis_date.isoformat() if progress.last_analysis_date else None,
                    "analysis_records": [record.to_dict() for record in progress.analysis_records],
                    "badges": [badge.to_dict() for badge in progress.badges]
                }
                save_data[user_id] = user_dict
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"データ保存エラー: {e}")
    
    def _define_level_requirements(self) -> Dict[int, Dict[str, Any]]:
        """レベル要件定義"""
        return {
            1: {"name": "ビギナー", "min_points": 0, "min_analyses": 0},
            2: {"name": "プレイヤー", "min_points": 100, "min_analyses": 5},
            3: {"name": "スキルドプレイヤー", "min_points": 300, "min_analyses": 15},
            4: {"name": "アドバンスプレイヤー", "min_points": 600, "min_analyses": 30},
            5: {"name": "エキスパート", "min_points": 1000, "min_analyses": 50},
            6: {"name": "マスター", "min_points": 1500, "min_analyses": 75},
            7: {"name": "レジェンド", "min_points": 2500, "min_analyses": 100}
        }
    
    def _define_badges(self) -> Dict[str, Dict[str, Any]]:
        """バッジ定義"""
        return {
            "first_analysis": {
                "name": "初回解析",
                "description": "初めての動画解析を完了",
                "icon": "🎾",
                "auto_award": True,
                "condition": "analysis_count >= 1"
            },
            "consistent_week": {
                "name": "継続の一歩",
                "description": "1週間以内に3回解析",
                "icon": "📅",
                "auto_award": True,
                "condition": "weekly_analyses >= 3"
            },
            "form_improver": {
                "name": "フォーム改善者",
                "description": "総合スコアが20ポイント向上",
                "icon": "📈",
                "auto_award": True,
                "condition": "score_improvement >= 20"
            },
            "stance_master": {
                "name": "スタンスマスター",
                "description": "スタンススコア90点以上を達成",
                "icon": "🏛️",
                "auto_award": True,
                "condition": "stance_score >= 90"
            },
            "swing_artist": {
                "name": "スイングアーティスト",
                "description": "スイング軌道スコア85点以上を達成",
                "icon": "🎨",
                "auto_award": True,
                "condition": "swing_score >= 85"
            },
            "balance_keeper": {
                "name": "バランスキーパー",
                "description": "バランススコア85点以上を達成",
                "icon": "⚖️",
                "auto_award": True,
                "condition": "balance_score >= 85"
            },
            "monthly_warrior": {
                "name": "月間戦士",
                "description": "1ヶ月間継続練習",
                "icon": "🗓️",
                "auto_award": True,
                "condition": "monthly_analyses >= 8"
            },
            "perfectionist": {
                "name": "完璧主義者",
                "description": "総合スコア95点以上を達成",
                "icon": "💎",
                "auto_award": True,
                "condition": "overall_score >= 95"
            },
            "dedicated_student": {
                "name": "熱心な生徒",
                "description": "50回の解析を完了",
                "icon": "📚",
                "auto_award": True,
                "condition": "total_analyses >= 50"
            },
            "improvement_champion": {
                "name": "改善チャンピオン",
                "description": "全カテゴリで80点以上を達成",
                "icon": "🏆",
                "auto_award": True,
                "condition": "all_categories_above_80"
            }
        }
    
    def get_user_progress(self, user_id: str) -> Optional[Dict[str, Any]]:
        """ユーザー進捗取得"""
        if user_id not in self.progress_data:
            return None
        
        progress = self.progress_data[user_id]
        
        # 改善傾向分析
        improvement_trends = self._analyze_improvement_trends(progress)
        
        # 次レベル要件
        next_level_req = self._get_next_level_requirements(progress.current_level)
        
        return {
            "user_id": user_id,
            "total_analyses": progress.total_analyses,
            "current_level": progress.current_level,
            "experience_points": progress.experience_points,
            "badges": [badge.to_dict() for badge in progress.badges],
            "score_history": self._get_score_history(progress),
            "improvement_trends": improvement_trends,
            "next_level_requirements": next_level_req,
            "last_analysis_date": progress.last_analysis_date.isoformat() if progress.last_analysis_date else None
        }
    
    def add_analysis_record(self, user_id: str, session_id: str, 
                          score: float, angle: str, 
                          category_scores: Dict[str, float] = None):
        """解析記録追加"""
        
        # ユーザー存在確認
        if user_id not in self.progress_data:
            self.progress_data[user_id] = UserProgress(user_id=user_id)
        
        progress = self.progress_data[user_id]
        
        # 解析記録追加
        record = AnalysisRecord(
            session_id=session_id,
            date=datetime.now(),
            overall_score=score,
            angle=angle,
            category_scores=category_scores
        )
        progress.analysis_records.append(record)
        
        # 統計更新
        progress.total_analyses += 1
        progress.last_analysis_date = datetime.now()
        
        # 経験値計算・追加
        exp_gained = self._calculate_experience_points(score)
        progress.experience_points += exp_gained
        
        # レベルアップチェック
        new_level = self._check_level_up(progress)
        if new_level > progress.current_level:
            progress.current_level = new_level
            self._award_level_up_badge(progress, new_level)
        
        # 自動バッジ授与チェック
        self._check_auto_badges(progress)
        
        # データ保存
        self._save_data()
        
        return {
            "exp_gained": exp_gained,
            "new_level": new_level if new_level > progress.current_level else None,
            "new_badges": []  # 実装時に追加されたバッジのリストを返す
        }
    
    def _calculate_experience_points(self, score: float) -> int:
        """経験値計算"""
        base_points = 10
        
        # スコアに応じたボーナス
        if score >= 90:
            bonus = 20
        elif score >= 80:
            bonus = 15
        elif score >= 70:
            bonus = 10
        elif score >= 60:
            bonus = 5
        else:
            bonus = 0
        
        return base_points + bonus
    
    def _check_level_up(self, progress: UserProgress) -> int:
        """レベルアップチェック"""
        current_level = progress.current_level
        
        for level, requirements in self.level_requirements.items():
            if (progress.experience_points >= requirements["min_points"] and 
                progress.total_analyses >= requirements["min_analyses"]):
                current_level = max(current_level, level)
        
        return current_level
    
    def _check_auto_badges(self, progress: UserProgress):
        """自動バッジ授与チェック"""
        earned_badge_ids = {badge.id for badge in progress.badges}
        
        for badge_id, badge_def in self.badge_definitions.items():
            if not badge_def.get("auto_award", False):
                continue
                
            if badge_id in earned_badge_ids:
                continue
            
            if self._check_badge_condition(progress, badge_def["condition"]):
                self._award_badge_internal(progress, badge_id)
    
    def _check_badge_condition(self, progress: UserProgress, condition: str) -> bool:
        """バッジ条件チェック"""
        if condition == "analysis_count >= 1":
            return progress.total_analyses >= 1
        
        elif condition == "weekly_analyses >= 3":
            week_ago = datetime.now() - timedelta(days=7)
            weekly_count = sum(1 for record in progress.analysis_records 
                             if record.date >= week_ago)
            return weekly_count >= 3
        
        elif condition == "monthly_analyses >= 8":
            month_ago = datetime.now() - timedelta(days=30)
            monthly_count = sum(1 for record in progress.analysis_records 
                              if record.date >= month_ago)
            return monthly_count >= 8
        
        elif condition == "score_improvement >= 20":
            if len(progress.analysis_records) < 5:
                return False
            recent_scores = [r.overall_score for r in progress.analysis_records[-5:]]
            early_scores = [r.overall_score for r in progress.analysis_records[:5]]
            if early_scores and recent_scores:
                improvement = max(recent_scores) - max(early_scores)
                return improvement >= 20
        
        elif condition == "overall_score >= 95":
            recent_records = progress.analysis_records[-3:] if len(progress.analysis_records) >= 3 else progress.analysis_records
            return any(record.overall_score >= 95 for record in recent_records)
        
        elif condition == "total_analyses >= 50":
            return progress.total_analyses >= 50
        
        # カテゴリ別スコア条件は簡略化
        elif "stance_score >= 90" in condition:
            return self._check_category_score(progress, "stance", 90)
        elif "swing_score >= 85" in condition:
            return self._check_category_score(progress, "swing_path", 85)
        elif "balance_score >= 85" in condition:
            return self._check_category_score(progress, "balance", 85)
        
        return False
    
    def _check_category_score(self, progress: UserProgress, category: str, threshold: float) -> bool:
        """カテゴリ別スコアチェック"""
        recent_records = progress.analysis_records[-3:] if len(progress.analysis_records) >= 3 else progress.analysis_records
        
        for record in recent_records:
            if record.category_scores and category in record.category_scores:
                if record.category_scores[category] >= threshold:
                    return True
        
        return False
    
    def _award_badge_internal(self, progress: UserProgress, badge_id: str):
        """内部バッジ授与"""
        if badge_id in self.badge_definitions:
            badge_def = self.badge_definitions[badge_id]
            badge = Badge(
                id=badge_id,
                name=badge_def["name"],
                description=badge_def["description"],
                earned_date=datetime.now(),
                icon=badge_def["icon"]
            )
            progress.badges.append(badge)
    
    def award_badge(self, user_id: str, badge_id: str) -> bool:
        """手動バッジ授与"""
        if user_id not in self.progress_data:
            return False
        
        if badge_id not in self.badge_definitions:
            return False
        
        progress = self.progress_data[user_id]
        
        # 既に獲得済みかチェック
        earned_badge_ids = {badge.id for badge in progress.badges}
        if badge_id in earned_badge_ids:
            return False
        
        self._award_badge_internal(progress, badge_id)
        self._save_data()
        
        return True
    
    def _award_level_up_badge(self, progress: UserProgress, level: int):
        """レベルアップバッジ授与"""
        level_badge_id = f"level_{level}"
        badge = Badge(
            id=level_badge_id,
            name=f"レベル{level}達成",
            description=f"レベル{level}に到達しました",
            earned_date=datetime.now(),
            icon="⭐"
        )
        progress.badges.append(badge)
    
    def _analyze_improvement_trends(self, progress: UserProgress) -> Dict[str, Any]:
        """改善傾向分析"""
        if len(progress.analysis_records) < 3:
            return {}
        
        # 直近1ヶ月のデータ
        month_ago = datetime.now() - timedelta(days=30)
        recent_records = [r for r in progress.analysis_records if r.date >= month_ago]
        
        if len(recent_records) < 2:
            return {}
        
        # 全体スコアの傾向
        scores = [r.overall_score for r in recent_records]
        if len(scores) >= 2:
            trend = "improving" if scores[-1] > scores[0] else "stable" if abs(scores[-1] - scores[0]) < 5 else "declining"
            change_rate = ((scores[-1] - scores[0]) / scores[0]) * 100 if scores[0] > 0 else 0
        else:
            trend = "stable"
            change_rate = 0
        
        return {
            "overall": {
                "trend": trend,
                "change_rate": round(change_rate, 1),
                "description": self._get_trend_description(trend, change_rate)
            }
        }
    
    def _get_trend_description(self, trend: str, change_rate: float) -> str:
        """傾向説明文生成"""
        if trend == "improving":
            if change_rate > 10:
                return "素晴らしい上達を見せています！"
            else:
                return "着実に改善が見られます"
        elif trend == "declining":
            return "少し調子が落ちているようです。基礎練習を重視しましょう"
        else:
            return "安定したパフォーマンスを維持しています"
    
    def _get_score_history(self, progress: UserProgress) -> List[Dict[str, Any]]:
        """スコア履歴取得"""
        return [
            {
                "date": record.date.isoformat(),
                "overall_score": record.overall_score,
                "angle": record.angle,
                "session_id": record.session_id
            }
            for record in progress.analysis_records[-10:]  # 直近10回
        ]
    
    def _get_next_level_requirements(self, current_level: int) -> Dict[str, Any]:
        """次レベル要件取得"""
        next_level = current_level + 1
        
        if next_level in self.level_requirements:
            req = self.level_requirements[next_level]
            return {
                "level": next_level,
                "name": req["name"],
                "points_needed": req["min_points"],
                "analyses_needed": req["min_analyses"],
                "description": f"レベル{next_level}「{req['name']}」まであと少し！"
            }
        else:
            return {
                "level": current_level,
                "name": "最高レベル",
                "points_needed": 0,
                "analyses_needed": 0,
                "description": "おめでとうございます！最高レベルに到達しました！"
            }