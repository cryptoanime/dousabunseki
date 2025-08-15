"""
軟式テニス専用フォーム分析AI
初心者向けの詳細なフォーム評価と改善提案システム
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json

from ..analysis.kinovea_engine import AnalysisResult, AnalysisAngle, Point2D

class FormCategory(Enum):
    """フォーム評価カテゴリ"""
    STANCE = "stance"                # スタンス
    SWING_PATH = "swing_path"        # スイング軌道
    TIMING = "timing"                # タイミング
    BALANCE = "balance"              # バランス
    FOLLOW_THROUGH = "follow_through" # フォロースルー

class SkillLevel(Enum):
    """技術レベル"""
    BEGINNER = "beginner"     # 初心者
    INTERMEDIATE = "intermediate"  # 中級者
    ADVANCED = "advanced"     # 上級者

@dataclass
class FormScore:
    """フォーム評価スコア"""
    category: FormCategory
    score: float  # 0-100
    max_score: float = 100.0
    details: Dict[str, float] = None
    
    @property
    def percentage(self) -> float:
        return (self.score / self.max_score) * 100

@dataclass
class ImprovementPoint:
    """改善ポイント"""
    category: FormCategory
    priority: str  # "high", "medium", "low"
    title: str
    description: str
    specific_advice: str
    training_focus: List[str]

@dataclass
class FormAnalysisReport:
    """フォーム分析レポート"""
    overall_score: float
    category_scores: Dict[FormCategory, FormScore]
    improvement_points: List[ImprovementPoint]
    strengths: List[str]
    weaknesses: List[str]
    recommended_training: List[str]

class SoftTennisFormAnalyzer:
    """軟式テニス専用フォーム分析システム"""
    
    def __init__(self):
        # 軟式テニス専用評価基準を読み込み
        self.evaluation_criteria = self._load_evaluation_criteria()
        self.improvement_database = self._load_improvement_database()
        
    def _load_evaluation_criteria(self) -> Dict:
        """軟式テニス評価基準を読み込み"""
        return {
            "stance": {
                "foot_distance": {"min": 0.5, "max": 0.8, "optimal": 0.65},  # 肩幅比
                "knee_bend": {"min": 10, "max": 45, "optimal": 25},  # 度
                "weight_distribution": {"front": 0.4, "back": 0.6}  # 初期構え
            },
            "swing_path": {
                "racket_speed": {"min": 8, "optimal": 15, "max": 25},  # m/s
                "swing_arc": {"min": 120, "optimal": 160, "max": 200},  # 度
                "impact_angle": {"min": 85, "optimal": 90, "max": 95}  # 度
            },
            "timing": {
                "preparation_time": {"min": 0.3, "optimal": 0.6, "max": 1.0},  # 秒
                "contact_timing": {"early": -0.1, "optimal": 0.0, "late": 0.1}  # 秒
            },
            "balance": {
                "body_sway": {"max": 0.2},  # メートル
                "center_of_gravity": {"forward": 0.1, "backward": -0.05}  # メートル
            },
            "follow_through": {
                "completion_ratio": {"min": 0.7, "optimal": 0.9},  # 完了度
                "direction_accuracy": {"min": 0.8, "optimal": 0.95}  # 方向精度
            }
        }
    
    def _load_improvement_database(self) -> Dict:
        """改善提案データベースを読み込み"""
        return {
            "stance_issues": {
                "narrow_stance": {
                    "title": "スタンスが狭すぎます",
                    "description": "足の幅が狭く、安定性に欠けています",
                    "advice": "足を肩幅程度に開き、安定した土台を作りましょう",
                    "training": ["鏡前でのスタンス練習", "バランス練習"]
                },
                "insufficient_knee_bend": {
                    "title": "膝の曲がりが不十分です",
                    "description": "軟式テニスの低いバウンドに対応できていません",
                    "advice": "膝をもう少し曲げて、低い姿勢を心がけましょう",
                    "training": ["スクワット練習", "低い姿勢でのボレー練習"]
                }
            },
            "swing_issues": {
                "slow_swing": {
                    "title": "スイングスピードが遅いです",
                    "description": "ラケットの振りが遅く、ボールに威力が伝わりません",
                    "advice": "体重移動を使って、よりダイナミックにスイングしましょう",
                    "training": ["素振り練習", "シャドースイング", "体重移動練習"]
                },
                "flat_swing": {
                    "title": "スイングが水平すぎます",
                    "description": "軟式ボールに適したトップスピンがかかっていません",
                    "advice": "下から上へのスイング軌道でトップスピンをかけましょう",
                    "training": ["トップスピン練習", "ブラッシング練習"]
                }
            },
            "timing_issues": {
                "late_preparation": {
                    "title": "準備が遅れています",
                    "description": "ボールに対する反応が遅く、余裕がありません",
                    "advice": "早めのテイクバックで余裕を持った準備をしましょう",
                    "training": ["反応練習", "フットワーク練習"]
                }
            },
            "balance_issues": {
                "unstable_balance": {
                    "title": "バランスが不安定です",
                    "description": "打球時に体が左右に揺れています",
                    "advice": "軸足をしっかり固定し、安定したスイングを心がけましょう",
                    "training": ["片足立ち練習", "バランスボール練習"]
                }
            }
        }
    
    def analyze_form(self, analysis_result: AnalysisResult, 
                    angle: AnalysisAngle) -> FormAnalysisReport:
        """
        フォーム分析を実行
        
        Args:
            analysis_result: Kinovea解析結果
            angle: 分析角度
            
        Returns:
            FormAnalysisReport: 詳細なフォーム分析レポート
        """
        
        # カテゴリ別スコア計算
        category_scores = {}
        
        if angle == AnalysisAngle.SIDE:
            # 側面からの分析
            category_scores[FormCategory.SWING_PATH] = self._evaluate_swing_path(analysis_result)
            category_scores[FormCategory.TIMING] = self._evaluate_timing(analysis_result)
            category_scores[FormCategory.FOLLOW_THROUGH] = self._evaluate_follow_through(analysis_result)
            
        elif angle == AnalysisAngle.FRONT:
            # 正面からの分析
            category_scores[FormCategory.STANCE] = self._evaluate_stance(analysis_result)
            category_scores[FormCategory.BALANCE] = self._evaluate_balance(analysis_result)
        
        # 総合スコア計算
        overall_score = self._calculate_overall_score(category_scores)
        
        # 改善ポイント特定
        improvement_points = self._identify_improvement_points(category_scores, analysis_result)
        
        # 長所・短所分析
        strengths = self._identify_strengths(category_scores)
        weaknesses = self._identify_weaknesses(category_scores)
        
        # 推奨トレーニング生成
        recommended_training = self._generate_training_recommendations(improvement_points)
        
        return FormAnalysisReport(
            overall_score=overall_score,
            category_scores=category_scores,
            improvement_points=improvement_points,
            strengths=strengths,
            weaknesses=weaknesses,
            recommended_training=recommended_training
        )
    
    def _evaluate_stance(self, analysis_result: AnalysisResult) -> FormScore:
        """スタンス評価"""
        details = {}
        total_score = 0
        max_points = 3
        
        # 足の幅評価
        if 'left_ankle' in analysis_result.tracking_points and 'right_ankle' in analysis_result.tracking_points:
            foot_distance = self._calculate_foot_distance(analysis_result)
            criteria = self.evaluation_criteria["stance"]["foot_distance"]
            
            if criteria["min"] <= foot_distance <= criteria["max"]:
                foot_score = 100 - abs(foot_distance - criteria["optimal"]) * 200
                total_score += max(foot_score, 60)
                details["foot_distance"] = foot_score
            else:
                details["foot_distance"] = 30
                total_score += 30
        
        # 膝の曲がり評価
        if 'knee_angle' in analysis_result.angles:
            knee_angles = analysis_result.angles['knee_angle'].values
            avg_knee_angle = np.mean(knee_angles) if knee_angles else 0
            
            criteria = self.evaluation_criteria["stance"]["knee_bend"]
            if criteria["min"] <= avg_knee_angle <= criteria["max"]:
                knee_score = 100 - abs(avg_knee_angle - criteria["optimal"]) * 2
                total_score += max(knee_score, 60)
                details["knee_bend"] = knee_score
            else:
                details["knee_bend"] = 40
                total_score += 40
        
        # 体重配分評価（推定）
        weight_score = self._evaluate_weight_distribution(analysis_result)
        total_score += weight_score
        details["weight_distribution"] = weight_score
        
        final_score = total_score / max_points
        
        return FormScore(
            category=FormCategory.STANCE,
            score=final_score,
            details=details
        )
    
    def _evaluate_swing_path(self, analysis_result: AnalysisResult) -> FormScore:
        """スイング軌道評価"""
        details = {}
        total_score = 0
        max_points = 3
        
        # ラケット速度評価
        if analysis_result.swing_analysis and 'swing_speed' in analysis_result.swing_analysis:
            swing_speed = analysis_result.swing_analysis['swing_speed']
            criteria = self.evaluation_criteria["swing_path"]["racket_speed"]
            
            if criteria["min"] <= swing_speed <= criteria["max"]:
                speed_score = 100 - abs(swing_speed - criteria["optimal"]) * 3
                total_score += max(speed_score, 50)
                details["swing_speed"] = speed_score
            else:
                details["swing_speed"] = 30
                total_score += 30
        
        # スイング軌道評価
        if analysis_result.racket_trajectory:
            arc_score = self._evaluate_swing_arc(analysis_result.racket_trajectory)
            total_score += arc_score
            details["swing_arc"] = arc_score
        
        # インパクト角度評価
        impact_score = self._evaluate_impact_angle(analysis_result)
        total_score += impact_score
        details["impact_angle"] = impact_score
        
        final_score = total_score / max_points
        
        return FormScore(
            category=FormCategory.SWING_PATH,
            score=final_score,
            details=details
        )
    
    def _evaluate_timing(self, analysis_result: AnalysisResult) -> FormScore:
        """タイミング評価"""
        details = {}
        total_score = 0
        
        if analysis_result.swing_analysis:
            timing_data = analysis_result.swing_analysis.get('timing_analysis', {})
            
            # 準備時間評価
            prep_time = timing_data.get('preparation_time', 0.5)
            criteria = self.evaluation_criteria["timing"]["preparation_time"]
            
            if criteria["min"] <= prep_time <= criteria["max"]:
                prep_score = 100 - abs(prep_time - criteria["optimal"]) * 100
                total_score = max(prep_score, 60)
                details["preparation_time"] = prep_score
            else:
                details["preparation_time"] = 40
                total_score = 40
        
        return FormScore(
            category=FormCategory.TIMING,
            score=total_score,
            details=details
        )
    
    def _evaluate_balance(self, analysis_result: AnalysisResult) -> FormScore:
        """バランス評価"""
        details = {}
        total_score = 70  # デフォルトスコア
        
        if analysis_result.swing_analysis:
            balance_data = analysis_result.swing_analysis.get('body_balance', {})
            
            # 左右バランス
            lr_balance = balance_data.get('left_right_balance', 0.8)
            lr_score = lr_balance * 100
            
            # 前後バランス
            fb_balance = balance_data.get('forward_backward_balance', 0.8)
            fb_score = fb_balance * 100
            
            total_score = (lr_score + fb_score) / 2
            details["left_right_balance"] = lr_score
            details["forward_backward_balance"] = fb_score
        
        return FormScore(
            category=FormCategory.BALANCE,
            score=total_score,
            details=details
        )
    
    def _evaluate_follow_through(self, analysis_result: AnalysisResult) -> FormScore:
        """フォロースルー評価"""
        details = {}
        total_score = 75  # デフォルトスコア
        
        if analysis_result.racket_trajectory and len(analysis_result.racket_trajectory.points) > 10:
            # フォロースルーの完成度を評価
            points = analysis_result.racket_trajectory.points
            
            # 軌道の滑らかさ
            smoothness = self._calculate_trajectory_smoothness(points)
            details["smoothness"] = smoothness * 100
            
            # 方向性
            direction_score = self._evaluate_follow_through_direction(points)
            details["direction"] = direction_score
            
            total_score = (smoothness * 100 + direction_score) / 2
        
        return FormScore(
            category=FormCategory.FOLLOW_THROUGH,
            score=total_score,
            details=details
        )
    
    def _calculate_overall_score(self, category_scores: Dict[FormCategory, FormScore]) -> float:
        """総合スコア計算"""
        if not category_scores:
            return 0.0
        
        total = sum(score.score for score in category_scores.values())
        return total / len(category_scores)
    
    def _identify_improvement_points(self, category_scores: Dict[FormCategory, FormScore], 
                                   analysis_result: AnalysisResult) -> List[ImprovementPoint]:
        """改善ポイント特定"""
        improvement_points = []
        
        for category, score in category_scores.items():
            if score.score < 70:  # 改善が必要なレベル
                priority = "high" if score.score < 50 else "medium"
                
                # カテゴリに応じた具体的な改善ポイントを生成
                points = self._generate_category_improvements(category, score, analysis_result)
                improvement_points.extend(points)
        
        # 優先度でソート
        improvement_points.sort(key=lambda x: {"high": 3, "medium": 2, "low": 1}[x.priority], reverse=True)
        
        return improvement_points[:5]  # 上位5つの改善ポイント
    
    def _generate_category_improvements(self, category: FormCategory, score: FormScore, 
                                      analysis_result: AnalysisResult) -> List[ImprovementPoint]:
        """カテゴリ別改善ポイント生成"""
        improvements = []
        
        if category == FormCategory.STANCE:
            if score.details and score.details.get("foot_distance", 100) < 60:
                improvements.append(ImprovementPoint(
                    category=category,
                    priority="high",
                    title="スタンス幅の改善",
                    description="足の幅が適切でなく、安定性に欠けています",
                    specific_advice="足を肩幅程度に開き、安定した土台を作りましょう。軟式テニスでは低いバウンドに対応するため、しっかりとした構えが重要です。",
                    training_focus=["スタンス練習", "バランス強化", "鏡前での確認"]
                ))
            
            if score.details and score.details.get("knee_bend", 100) < 60:
                improvements.append(ImprovementPoint(
                    category=category,
                    priority="high",
                    title="膝の曲がりを改善",
                    description="膝の曲がりが不十分で、軟式ボールの低いバウンドに対応できていません",
                    specific_advice="膝をもう少し曲げて、低い姿勢を心がけましょう。軟式テニスボールは硬式より低くバウンドするため、低い姿勢が大切です。",
                    training_focus=["スクワット練習", "低い姿勢での練習", "フットワーク改善"]
                ))
        
        elif category == FormCategory.SWING_PATH:
            if score.details and score.details.get("swing_speed", 100) < 60:
                improvements.append(ImprovementPoint(
                    category=category,
                    priority="high",
                    title="スイングスピードの向上",
                    description="ラケットの振りが遅く、ボールに十分な威力が伝わっていません",
                    specific_advice="体重移動を使って、よりダイナミックにスイングしましょう。腰の回転から肩、腕の順番で力を伝える運動連鎖を意識してください。",
                    training_focus=["素振り練習", "体重移動練習", "シャドースイング"]
                ))
        
        # その他のカテゴリも同様に実装...
        
        return improvements
    
    def _identify_strengths(self, category_scores: Dict[FormCategory, FormScore]) -> List[str]:
        """長所特定"""
        strengths = []
        
        for category, score in category_scores.items():
            if score.score >= 80:
                if category == FormCategory.STANCE:
                    strengths.append("安定したスタンスができています")
                elif category == FormCategory.SWING_PATH:
                    strengths.append("スイング軌道が良好です")
                elif category == FormCategory.TIMING:
                    strengths.append("タイミングが適切です")
                elif category == FormCategory.BALANCE:
                    strengths.append("バランスが安定しています")
                elif category == FormCategory.FOLLOW_THROUGH:
                    strengths.append("フォロースルーが滑らかです")
        
        if not strengths:
            strengths.append("基本的なフォームの土台ができつつあります")
        
        return strengths
    
    def _identify_weaknesses(self, category_scores: Dict[FormCategory, FormScore]) -> List[str]:
        """弱点特定"""
        weaknesses = []
        
        sorted_scores = sorted(category_scores.items(), key=lambda x: x[1].score)
        
        for category, score in sorted_scores[:2]:  # 下位2つ
            if score.score < 70:
                if category == FormCategory.STANCE:
                    weaknesses.append("スタンスの安定性")
                elif category == FormCategory.SWING_PATH:
                    weaknesses.append("スイング軌道の精度")
                elif category == FormCategory.TIMING:
                    weaknesses.append("タイミングの調整")
                elif category == FormCategory.BALANCE:
                    weaknesses.append("体のバランス")
                elif category == FormCategory.FOLLOW_THROUGH:
                    weaknesses.append("フォロースルーの完成度")
        
        return weaknesses
    
    def _generate_training_recommendations(self, improvement_points: List[ImprovementPoint]) -> List[str]:
        """トレーニング推奨事項生成"""
        training_set = set()
        
        for point in improvement_points:
            training_set.update(point.training_focus)
        
        # 軟式テニス特有の練習も追加
        training_set.add("壁打ち練習（軟式ボール専用）")
        training_set.add("トップスピン練習")
        
        return list(training_set)[:6]  # 最大6つの推奨練習
    
    # ヘルパーメソッド（簡略化実装）
    def _calculate_foot_distance(self, analysis_result: AnalysisResult) -> float:
        """足の距離計算"""
        # 実装の詳細は省略
        return 0.65  # サンプル値
    
    def _evaluate_weight_distribution(self, analysis_result: AnalysisResult) -> float:
        """体重配分評価"""
        return 75.0  # サンプル値
    
    def _evaluate_swing_arc(self, racket_trajectory) -> float:
        """スイング軌道評価"""
        return 80.0  # サンプル値
    
    def _evaluate_impact_angle(self, analysis_result: AnalysisResult) -> float:
        """インパクト角度評価"""
        return 85.0  # サンプル値
    
    def _calculate_trajectory_smoothness(self, points: List[Point2D]) -> float:
        """軌道の滑らかさ計算"""
        return 0.8  # サンプル値
    
    def _evaluate_follow_through_direction(self, points: List[Point2D]) -> float:
        """フォロースルー方向評価"""
        return 82.0  # サンプル値