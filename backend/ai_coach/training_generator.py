"""
軟式テニス専用トレーニングメニュー生成システム
初心者向けの個別最適化されたトレーニングプログラム
"""

import json
import random
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class TrainingLocation(Enum):
    """練習場所"""
    COURT = "court"
    HOME = "home"
    BOTH = "both"

class FocusArea(Enum):
    """重点エリア"""
    STANCE = "stance"
    SWING_PATH = "swing_path"
    TIMING = "timing"
    BALANCE = "balance"
    FOLLOW_THROUGH = "follow_through"
    FOOTWORK = "footwork"
    SPIN = "spin"

@dataclass
class Exercise:
    """トレーニング種目"""
    name: str
    duration: int  # 分
    description: str
    focus_area: str
    location: str
    difficulty: str
    instructions: List[str]
    tips: List[str]
    equipment_needed: List[str] = None

@dataclass
class DailyPlan:
    """日別練習プラン"""
    day: int
    exercises: List[str]
    total_duration: int
    focus: str

@dataclass
class TrainingMenu:
    """トレーニングメニュー"""
    exercises: List[Exercise]
    daily_plan: List[DailyPlan]
    tips: List[str]

class TrainingMenuGenerator:
    """軟式テニス専用トレーニングメニュー生成器"""
    
    def __init__(self):
        self.exercise_database = self._load_exercise_database()
        self.training_principles = self._load_training_principles()
    
    def _load_exercise_database(self) -> Dict:
        """軟式テニス専用練習データベース"""
        return {
            "stance": {
                "court": [
                    {
                        "name": "鏡前スタンス確認",
                        "duration": 5,
                        "description": "コートの壁や鏡で正しいスタンスを確認する練習",
                        "focus_area": "stance",
                        "location": "court",
                        "difficulty": "beginner",
                        "instructions": [
                            "壁や鏡の前に立つ",
                            "足を肩幅に開く",
                            "膝を軽く曲げる",
                            "重心を前後に移動させながら最適な位置を見つける",
                            "この姿勢を30秒キープ×5回"
                        ],
                        "tips": [
                            "軟式テニスでは低いバウンドに対応するため、硬式より低い姿勢を意識",
                            "体重は踵に乗せすぎず、つま先寄りに"
                        ],
                        "equipment_needed": ["なし"]
                    },
                    {
                        "name": "動的スタンス練習",
                        "duration": 10,
                        "description": "実際のプレイを想定したスタンス移動練習",
                        "focus_area": "stance",
                        "location": "court",
                        "difficulty": "beginner",
                        "instructions": [
                            "ベースラインの中央に構える",
                            "左右にサイドステップで移動",
                            "各位置で正しいスタンスを作る",
                            "1回の移動で3歩以内",
                            "10往復×3セット"
                        ],
                        "tips": [
                            "移動後は必ず安定したスタンスを作る",
                            "急に止まらず、最後の一歩で姿勢を整える"
                        ],
                        "equipment_needed": ["コーン（あれば）"]
                    }
                ],
                "home": [
                    {
                        "name": "室内スタンス練習",
                        "duration": 5,
                        "description": "自宅でできるスタンス基礎練習",
                        "focus_area": "stance",
                        "location": "home",
                        "difficulty": "beginner",
                        "instructions": [
                            "鏡の前または窓ガラスの前に立つ",
                            "軟式テニス用のスタンスを作る",
                            "片足立ちを左右各30秒",
                            "スクワット10回（ゆっくり）",
                            "最後にスタンスの姿勢で1分間キープ"
                        ],
                        "tips": [
                            "毎日継続することが大切",
                            "正しいフォームを鏡で確認"
                        ],
                        "equipment_needed": ["鏡"]
                    }
                ]
            },
            "swing_path": {
                "court": [
                    {
                        "name": "壁打ち連続ストローク",
                        "duration": 15,
                        "description": "壁に向かって一定リズムでストローク練習",
                        "focus_area": "swing_path",
                        "location": "court",
                        "difficulty": "beginner",
                        "instructions": [
                            "壁から3メートル離れて構える",
                            "軟式ボールで壁打ち",
                            "1回1回のスイングを丁寧に",
                            "連続50回を目標",
                            "休憩1分×3セット"
                        ],
                        "tips": [
                            "軟式ボールは変形しやすいので面を安定させる",
                            "下から上へのスイングでトップスピンを意識"
                        ],
                        "equipment_needed": ["軟式ボール", "ラケット"]
                    },
                    {
                        "name": "トップスピン練習",
                        "duration": 10,
                        "description": "軟式テニス特有のトップスピンをマスターする",
                        "focus_area": "swing_path",
                        "location": "court",
                        "difficulty": "beginner",
                        "instructions": [
                            "ネット際に立つ",
                            "山なりの軌道でベースラインを狙う",
                            "インパクト後、ラケット面を下向きに",
                            "ボールの下半分を擦り上げる感覚",
                            "成功10回×3セット"
                        ],
                        "tips": [
                            "軟式ボールは回転がかかりやすいのでメリットを活用",
                            "力任せではなく、回転で制御"
                        ],
                        "equipment_needed": ["軟式ボール", "ラケット"]
                    }
                ],
                "home": [
                    {
                        "name": "鏡前素振り",
                        "duration": 5,
                        "description": "鏡を見ながら正しいスイングフォームを習得",
                        "focus_area": "swing_path",
                        "location": "home",
                        "difficulty": "beginner",
                        "instructions": [
                            "鏡の前でラケットを持つ",
                            "ゆっくりとしたスイング練習",
                            "テイクバック→インパクト→フォロースルー",
                            "各段階で2秒ずつ止める",
                            "20回×3セット"
                        ],
                        "tips": [
                            "速度より正確性を重視",
                            "軟式特有の下から上への軌道を意識"
                        ],
                        "equipment_needed": ["ラケット", "鏡"]
                    },
                    {
                        "name": "シャドースイング",
                        "duration": 8,
                        "description": "実際のボールを想定したスイング練習",
                        "focus_area": "swing_path",
                        "location": "home",
                        "difficulty": "beginner",
                        "instructions": [
                            "十分なスペースを確保",
                            "実際の試合を想定",
                            "フォアハンド20回",
                            "バックハンド20回",
                            "各ショットでフォームを確認"
                        ],
                        "tips": [
                            "毎回同じフォームで打てるよう意識",
                            "軟式の特徴である回転を意識したスイング"
                        ],
                        "equipment_needed": ["ラケット"]
                    }
                ]
            },
            "timing": {
                "court": [
                    {
                        "name": "リズム打ち練習",
                        "duration": 10,
                        "description": "一定のリズムでタイミングを習得",
                        "focus_area": "timing",
                        "location": "court",
                        "difficulty": "beginner",
                        "instructions": [
                            "パートナーと向かい合う",
                            "ゆっくりとしたラリー",
                            "1、2、3のリズムで打つ",
                            "1（準備）、2（テイクバック）、3（インパクト）",
                            "連続10回成功を目標"
                        ],
                        "tips": [
                            "軟式ボールは滞空時間が長いので余裕を持って",
                            "早すぎる準備を避ける"
                        ],
                        "equipment_needed": ["軟式ボール", "ラケット", "パートナー"]
                    }
                ],
                "home": [
                    {
                        "name": "メトロノーム練習",
                        "duration": 5,
                        "description": "一定のリズムでスイングタイミングを養う",
                        "focus_area": "timing",
                        "location": "home",
                        "difficulty": "beginner",
                        "instructions": [
                            "メトロノームを60BPMに設定",
                            "1拍目でテイクバック開始",
                            "2拍目でインパクト",
                            "3拍目でフォロースルー完了",
                            "このリズムで20回"
                        ],
                        "tips": [
                            "慣れてきたら70BPMに上げる",
                            "正確なタイミングが身につくまで継続"
                        ],
                        "equipment_needed": ["ラケット", "メトロノーム（スマホアプリでOK）"]
                    }
                ]
            },
            "balance": {
                "court": [
                    {
                        "name": "片足立ちショット",
                        "duration": 8,
                        "description": "バランス力強化のための片足立ち練習",
                        "focus_area": "balance",
                        "location": "court",
                        "difficulty": "beginner",
                        "instructions": [
                            "軸足一本で立つ",
                            "その状態でシャドースイング",
                            "左足軸で10回、右足軸で10回",
                            "最初はゆっくり、慣れたら普通の速度",
                            "3セット実施"
                        ],
                        "tips": [
                            "転倒注意、無理をしない",
                            "軸足の膝を軽く曲げて安定性を確保"
                        ],
                        "equipment_needed": ["ラケット"]
                    }
                ],
                "home": [
                    {
                        "name": "バランスボール練習",
                        "duration": 10,
                        "description": "体幹とバランス力の向上",
                        "focus_area": "balance",
                        "location": "home",
                        "difficulty": "beginner",
                        "instructions": [
                            "バランスボールに座る",
                            "両手でラケットを持つ",
                            "ゆっくりとしたスイング動作",
                            "座った状態をキープしながら",
                            "フォア・バック各10回"
                        ],
                        "tips": [
                            "転倒防止のため壁の近くで実施",
                            "慣れるまでは支えを使っても良い"
                        ],
                        "equipment_needed": ["バランスボール", "ラケット"]
                    },
                    {
                        "name": "体幹エクササイズ",
                        "duration": 8,
                        "description": "テニス専用の体幹強化",
                        "focus_area": "balance",
                        "location": "home",
                        "difficulty": "beginner",
                        "instructions": [
                            "プランク30秒×2回",
                            "サイドプランク左右各20秒",
                            "バードドッグ左右各10回",
                            "最後にテニススタンスで1分",
                            "週3回実施"
                        ],
                        "tips": [
                            "正しいフォームで実施",
                            "呼吸を止めずに継続"
                        ],
                        "equipment_needed": ["ヨガマット（あれば）"]
                    }
                ]
            },
            "footwork": {
                "court": [
                    {
                        "name": "ラダートレーニング",
                        "duration": 10,
                        "description": "敏捷性と正確なフットワーク習得",
                        "focus_area": "footwork",
                        "location": "court",
                        "difficulty": "beginner",
                        "instructions": [
                            "ラダーまたはライン使用",
                            "前向きステップ往復3回",
                            "横向きステップ往復3回",
                            "後ろ向きステップ往復3回",
                            "休憩30秒×3セット"
                        ],
                        "tips": [
                            "速度より正確性重視",
                            "軟式テニスの機敏な動きを意識"
                        ],
                        "equipment_needed": ["ラダー（またはライン）"]
                    }
                ],
                "home": [
                    {
                        "name": "その場ステップ",
                        "duration": 5,
                        "description": "室内でできるフットワーク基礎",
                        "focus_area": "footwork",
                        "location": "home",
                        "difficulty": "beginner",
                        "instructions": [
                            "その場で軽くジャンプ",
                            "前後左右のステップ",
                            "1分間継続×3セット",
                            "テニスの構えを維持",
                            "リズムよく実施"
                        ],
                        "tips": [
                            "着地は音を立てずに",
                            "常にテニスポジションをキープ"
                        ],
                        "equipment_needed": ["なし"]
                    }
                ]
            }
        }
    
    def _load_training_principles(self) -> Dict:
        """トレーニング原則"""
        return {
            "beginner_duration": {
                "min": 20,
                "max": 40,
                "optimal": 30
            },
            "focus_distribution": {
                "primary": 0.5,    # 主要改善エリア
                "secondary": 0.3,  # 副次改善エリア
                "maintenance": 0.2  # 維持エリア
            },
            "location_preference": {
                "court": 0.7,
                "home": 0.3
            },
            "weekly_plan": {
                "training_days": 4,
                "rest_days": 3
            }
        }
    
    def generate_menu(self, focus_areas: List[str] = None, 
                     location: str = "both", 
                     duration_minutes: int = 30) -> TrainingMenu:
        """
        カスタマイズされたトレーニングメニューを生成
        
        Args:
            focus_areas: 重点練習エリアのリスト
            location: 練習場所 ("court", "home", "both")
            duration_minutes: 練習時間（分）
        
        Returns:
            TrainingMenu: 生成されたトレーニングメニュー
        """
        
        # デフォルト設定
        if not focus_areas:
            focus_areas = ["stance", "swing_path"]
        
        # 場所に応じた練習選択
        available_locations = self._get_available_locations(location)
        
        # エクササイズ選択
        selected_exercises = self._select_exercises(
            focus_areas, available_locations, duration_minutes
        )
        
        # 週間プラン生成
        daily_plan = self._generate_daily_plan(selected_exercises, focus_areas)
        
        # アドバイス生成
        tips = self._generate_tips(focus_areas, location)
        
        return TrainingMenu(
            exercises=selected_exercises,
            daily_plan=daily_plan,
            tips=tips
        )
    
    def _get_available_locations(self, location: str) -> List[str]:
        """利用可能な練習場所を取得"""
        if location == "both":
            return ["court", "home"]
        else:
            return [location]
    
    def _select_exercises(self, focus_areas: List[str], 
                         locations: List[str], 
                         duration_minutes: int) -> List[Exercise]:
        """エクササイズ選択"""
        selected_exercises = []
        remaining_time = duration_minutes
        
        # 主要フォーカスエリアから選択
        for area in focus_areas:
            if remaining_time <= 0:
                break
                
            if area in self.exercise_database:
                for loc in locations:
                    if loc in self.exercise_database[area]:
                        exercises = self.exercise_database[area][loc]
                        
                        # 時間内に収まるエクササイズを選択
                        for exercise_data in exercises:
                            if exercise_data["duration"] <= remaining_time:
                                exercise = Exercise(**exercise_data)
                                selected_exercises.append(exercise)
                                remaining_time -= exercise.duration
                                break
        
        # 残り時間があれば基本練習を追加
        if remaining_time > 5:
            basic_exercises = self._get_basic_exercises(locations, remaining_time)
            selected_exercises.extend(basic_exercises)
        
        return selected_exercises
    
    def _get_basic_exercises(self, locations: List[str], remaining_time: int) -> List[Exercise]:
        """基本練習取得"""
        basic_exercises = []
        
        # 基本的なウォームアップやクールダウン
        if "home" in locations and remaining_time >= 5:
            basic_exercises.append(Exercise(
                name="ストレッチング",
                duration=5,
                description="軟式テニスに特化したストレッチ",
                focus_area="general",
                location="home",
                difficulty="beginner",
                instructions=[
                    "肩回し前後各10回",
                    "手首回し前後各10回", 
                    "アキレス腱伸ばし左右各30秒",
                    "股関節ストレッチ",
                    "深呼吸で仕上げ"
                ],
                tips=["練習前後のストレッチは怪我予防に重要"],
                equipment_needed=["なし"]
            ))
        
        return basic_exercises
    
    def _generate_daily_plan(self, exercises: List[Exercise], 
                           focus_areas: List[str]) -> List[DailyPlan]:
        """日別プラン生成"""
        daily_plans = []
        
        # 4日間の練習プランを生成（初心者は週4回）
        for day in range(1, 5):
            if day <= len(exercises):
                day_exercises = exercises[:2] if len(exercises) >= 2 else exercises
                total_time = sum(ex.duration for ex in day_exercises)
                
                # その日のフォーカス決定
                focus = focus_areas[0] if focus_areas else "基本練習"
                
                daily_plans.append(DailyPlan(
                    day=day,
                    exercises=[ex.name for ex in day_exercises],
                    total_duration=total_time,
                    focus=focus
                ))
        
        return daily_plans
    
    def _generate_tips(self, focus_areas: List[str], location: str) -> List[str]:
        """アドバイス生成"""
        tips = [
            "軟式テニスは硬式と異なり、ボールが柔らかく変形しやすいので、面の安定が重要です",
            "低いバウンドに対応するため、膝を曲げた低い姿勢を心がけましょう",
            "トップスピンを多用する軟式テニスでは、下から上へのスイングを意識してください"
        ]
        
        # フォーカスエリアに応じたアドバイス
        if "stance" in focus_areas:
            tips.append("安定したスタンスは全てのショットの基礎です。毎日の練習で確認しましょう")
        
        if "swing_path" in focus_areas:
            tips.append("軟式ボールの特性を活かし、回転をかけることでコントロールが向上します")
        
        if "timing" in focus_areas:
            tips.append("軟式ボールは滞空時間が長いので、余裕を持った準備が可能です")
        
        # 場所に応じたアドバイス
        if location == "home":
            tips.append("自宅練習では正しいフォームの確認を重視し、鏡を活用しましょう")
        elif location == "court":
            tips.append("コート練習では実戦を意識し、様々な状況を想定して練習しましょう")
        
        return tips[:5]  # 最大5つのアドバイス