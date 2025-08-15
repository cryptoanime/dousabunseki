"""
Kinovea動作解析エンジンの軟式テニス特化版
Kinoveaの追跡・解析技術をPythonに移植し、軟式テニス用に最適化
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import math
import json

class AnalysisAngle(Enum):
    """分析角度の種類"""
    FRONT = "front"  # 正面
    SIDE = "side"    # 側面

@dataclass
class Point2D:
    """2D座標点"""
    x: float
    y: float
    
    def distance_to(self, other: 'Point2D') -> float:
        """他の点との距離を計算"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def angle_to(self, other: 'Point2D') -> float:
        """他の点への角度を計算（ラジアン）"""
        return math.atan2(other.y - self.y, other.x - self.x)

@dataclass
class TrackingPoint:
    """追跡ポイント"""
    name: str
    points: List[Point2D]
    confidence: List[float]
    frame_numbers: List[int]

@dataclass
class AngleData:
    """角度データ"""
    name: str
    values: List[float]  # 角度の時系列データ（度）
    frame_numbers: List[int]

@dataclass
class AnalysisResult:
    """解析結果"""
    tracking_points: Dict[str, TrackingPoint]
    angles: Dict[str, AngleData]
    ball_trajectory: Optional[TrackingPoint]
    racket_trajectory: Optional[TrackingPoint]
    swing_analysis: Dict[str, any]
    recommendations: List[str]

class SoftTennisKinoveaEngine:
    """軟式テニス専用Kinovea解析エンジン"""
    
    def __init__(self):
        # MediaPipe初期化
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # OpenCV初期化
        self.ball_tracker = cv2.TrackerCSRT_create()
        self.racket_tracker = cv2.TrackerCSRT_create()
        
        # 軟式テニス専用パラメータ
        self.soft_tennis_params = self._load_soft_tennis_parameters()
        
    def _load_soft_tennis_parameters(self) -> Dict:
        """軟式テニス専用パラメータを読み込み"""
        return {
            "ball_color_range": {
                "lower": np.array([0, 100, 100]),  # HSV下限（赤色系）
                "upper": np.array([10, 255, 255])  # HSV上限
            },
            "racket_color_range": {
                "lower": np.array([0, 0, 0]),      # 黒色系
                "upper": np.array([180, 255, 50])
            },
            "court_dimensions": {
                "length": 23.77,  # メートル
                "width": 10.97,
                "net_height": 1.07
            }
        }
    
    def analyze_video(self, video_path: str, angle: AnalysisAngle) -> AnalysisResult:
        """
        動画を解析してフォーム分析結果を返す
        
        Args:
            video_path: 動画ファイルのパス
            angle: 分析角度（正面または側面）
            
        Returns:
            AnalysisResult: 解析結果
        """
        cap = cv2.VideoCapture(video_path)
        
        # フレーム情報取得
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # データ格納用
        pose_data = []
        ball_data = []
        racket_data = []
        frame_count = 0
        
        # 初期フレームでボール・ラケット検出
        ret, first_frame = cap.read()
        if ret:
            ball_bbox = self._detect_ball(first_frame)
            racket_bbox = self._detect_racket(first_frame)
            
            if ball_bbox:
                self.ball_tracker.init(first_frame, ball_bbox)
            if racket_bbox:
                self.racket_tracker.init(first_frame, racket_bbox)
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # 姿勢検出
            pose_result = self._detect_pose(frame)
            pose_data.append({
                'frame': frame_count,
                'landmarks': pose_result,
                'timestamp': frame_count / fps
            })
            
            # ボール追跡
            if ball_bbox:
                ball_pos = self._track_ball(frame)
                if ball_pos:
                    ball_data.append({
                        'frame': frame_count,
                        'position': ball_pos,
                        'timestamp': frame_count / fps
                    })
            
            # ラケット追跡
            if racket_bbox:
                racket_pos = self._track_racket(frame)
                if racket_pos:
                    racket_data.append({
                        'frame': frame_count,
                        'position': racket_pos,
                        'timestamp': frame_count / fps
                    })
            
            frame_count += 1
        
        cap.release()
        
        # データ解析
        return self._analyze_motion_data(pose_data, ball_data, racket_data, angle)
    
    def _detect_pose(self, frame: np.ndarray) -> Optional[Dict]:
        """MediaPipeで姿勢検出"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        if results.pose_landmarks:
            landmarks = {}
            for i, landmark in enumerate(results.pose_landmarks.landmark):
                landmarks[i] = {
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z,
                    'visibility': landmark.visibility
                }
            return landmarks
        return None
    
    def _detect_ball(self, frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """ボール検出（色ベース + 円検出）"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # 色フィルタリング
        mask = cv2.inRange(hsv, 
                          self.soft_tennis_params["ball_color_range"]["lower"],
                          self.soft_tennis_params["ball_color_range"]["upper"])
        
        # 円検出
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                                  param1=50, param2=30, minRadius=5, maxRadius=50)
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            if len(circles) > 0:
                # 最も可能性の高い円を選択
                x, y, r = circles[0]
                return (x-r, y-r, 2*r, 2*r)
        
        return None
    
    def _detect_racket(self, frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """ラケット検出（エッジ検出ベース）"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # 輪郭検出
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if 500 < area < 5000:  # ラケットサイズの範囲
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h
                if 0.3 < aspect_ratio < 3.0:  # ラケットの縦横比
                    return (x, y, w, h)
        
        return None
    
    def _track_ball(self, frame: np.ndarray) -> Optional[Point2D]:
        """ボール追跡"""
        success, bbox = self.ball_tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]
            center_x = x + w // 2
            center_y = y + h // 2
            return Point2D(center_x, center_y)
        return None
    
    def _track_racket(self, frame: np.ndarray) -> Optional[Point2D]:
        """ラケット追跡"""
        success, bbox = self.racket_tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]
            center_x = x + w // 2
            center_y = y + h // 2
            return Point2D(center_x, center_y)
        return None
    
    def _analyze_motion_data(self, pose_data: List[Dict], ball_data: List[Dict], 
                           racket_data: List[Dict], angle: AnalysisAngle) -> AnalysisResult:
        """動作データを解析"""
        
        # 追跡ポイント生成
        tracking_points = self._generate_tracking_points(pose_data)
        
        # 角度データ計算
        angles = self._calculate_angles(pose_data, angle)
        
        # ボール軌道
        ball_trajectory = self._generate_ball_trajectory(ball_data)
        
        # ラケット軌道
        racket_trajectory = self._generate_racket_trajectory(racket_data)
        
        # スイング解析
        swing_analysis = self._analyze_swing(pose_data, racket_data, angle)
        
        # 改善提案生成
        recommendations = self._generate_recommendations(swing_analysis, angle)
        
        return AnalysisResult(
            tracking_points=tracking_points,
            angles=angles,
            ball_trajectory=ball_trajectory,
            racket_trajectory=racket_trajectory,
            swing_analysis=swing_analysis,
            recommendations=recommendations
        )
    
    def _generate_tracking_points(self, pose_data: List[Dict]) -> Dict[str, TrackingPoint]:
        """主要な身体ポイントの追跡データを生成"""
        key_points = {
            'left_shoulder': 11,
            'right_shoulder': 12,
            'left_elbow': 13,
            'right_elbow': 14,
            'left_wrist': 15,
            'right_wrist': 16,
            'left_hip': 23,
            'right_hip': 24,
            'left_knee': 25,
            'right_knee': 26,
            'left_ankle': 27,
            'right_ankle': 28
        }
        
        tracking_points = {}
        
        for name, landmark_id in key_points.items():
            points = []
            confidence = []
            frame_numbers = []
            
            for frame_data in pose_data:
                if frame_data['landmarks'] and landmark_id in frame_data['landmarks']:
                    landmark = frame_data['landmarks'][landmark_id]
                    points.append(Point2D(landmark['x'], landmark['y']))
                    confidence.append(landmark['visibility'])
                    frame_numbers.append(frame_data['frame'])
            
            if points:
                tracking_points[name] = TrackingPoint(
                    name=name,
                    points=points,
                    confidence=confidence,
                    frame_numbers=frame_numbers
                )
        
        return tracking_points
    
    def _calculate_angles(self, pose_data: List[Dict], angle: AnalysisAngle) -> Dict[str, AngleData]:
        """関節角度を計算"""
        angles = {}
        
        if angle == AnalysisAngle.SIDE:
            # 側面：スイング関連角度
            angles['elbow_angle'] = self._calculate_elbow_angle(pose_data)
            angles['shoulder_angle'] = self._calculate_shoulder_angle(pose_data)
            angles['hip_angle'] = self._calculate_hip_angle(pose_data)
        
        elif angle == AnalysisAngle.FRONT:
            # 正面：スタンス関連角度
            angles['stance_angle'] = self._calculate_stance_angle(pose_data)
            angles['body_rotation'] = self._calculate_body_rotation(pose_data)
        
        return angles
    
    def _calculate_elbow_angle(self, pose_data: List[Dict]) -> AngleData:
        """肘角度を計算"""
        angles = []
        frame_numbers = []
        
        for frame_data in pose_data:
            if frame_data['landmarks']:
                landmarks = frame_data['landmarks']
                
                # 右腕の肘角度計算（例）
                if all(id in landmarks for id in [12, 14, 16]):  # 肩、肘、手首
                    shoulder = landmarks[12]
                    elbow = landmarks[14]
                    wrist = landmarks[16]
                    
                    # ベクトル計算
                    v1 = np.array([shoulder['x'] - elbow['x'], shoulder['y'] - elbow['y']])
                    v2 = np.array([wrist['x'] - elbow['x'], wrist['y'] - elbow['y']])
                    
                    # 角度計算
                    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
                    angle_degrees = np.degrees(angle)
                    
                    angles.append(angle_degrees)
                    frame_numbers.append(frame_data['frame'])
        
        return AngleData(name="elbow_angle", values=angles, frame_numbers=frame_numbers)
    
    def _analyze_swing(self, pose_data: List[Dict], racket_data: List[Dict], 
                      angle: AnalysisAngle) -> Dict[str, any]:
        """スイング解析"""
        analysis = {}
        
        if angle == AnalysisAngle.SIDE:
            analysis.update({
                'swing_speed': self._calculate_swing_speed(racket_data),
                'swing_path': self._analyze_swing_path(racket_data),
                'weight_transfer': self._analyze_weight_transfer(pose_data),
                'timing_analysis': self._analyze_timing(pose_data, racket_data)
            })
        
        elif angle == AnalysisAngle.FRONT:
            analysis.update({
                'stance_stability': self._analyze_stance_stability(pose_data),
                'body_balance': self._analyze_body_balance(pose_data),
                'foot_positioning': self._analyze_foot_positioning(pose_data)
            })
        
        return analysis
    
    def _generate_recommendations(self, swing_analysis: Dict[str, any], 
                                angle: AnalysisAngle) -> List[str]:
        """軟式テニス初心者向け改善提案を生成"""
        recommendations = []
        
        if angle == AnalysisAngle.SIDE:
            # 側面からの改善提案
            if swing_analysis.get('swing_speed', 0) < 10:  # m/s
                recommendations.append("ラケットスピードが遅いです。体重移動を意識してスイングしましょう。")
            
            if swing_analysis.get('weight_transfer', {}).get('score', 0) < 0.7:
                recommendations.append("体重移動が不十分です。後ろ足から前足へしっかり体重を移しましょう。")
                
            recommendations.append("軟式ボールは変形しやすいので、インパクトの瞬間は面を安定させましょう。")
        
        elif angle == AnalysisAngle.FRONT:
            # 正面からの改善提案
            if swing_analysis.get('stance_stability', {}).get('score', 0) < 0.7:
                recommendations.append("スタンスが不安定です。足を肩幅に開き、安定した構えを作りましょう。")
            
            recommendations.append("軟式テニスでは低いバウンドに対応するため、膝を曲げた低い姿勢を保ちましょう。")
        
        # 共通の軟式テニス改善提案
        recommendations.extend([
            "軟式ボールは回転がかかりやすいので、トップスピンを意識したスイングを練習しましょう。",
            "インパクト後のフォロースルーで、ラケット面を下向きに向けてトップスピンをかけましょう。"
        ])
        
        return recommendations
    
    # その他のヘルパーメソッド（簡略化）
    def _calculate_swing_speed(self, racket_data: List[Dict]) -> float:
        """スイング速度計算"""
        if len(racket_data) < 2:
            return 0.0
        
        # 簡単な速度計算
        speeds = []
        for i in range(1, len(racket_data)):
            prev = racket_data[i-1]['position']
            curr = racket_data[i]['position']
            dt = racket_data[i]['timestamp'] - racket_data[i-1]['timestamp']
            
            if dt > 0:
                distance = prev.distance_to(curr)
                speed = distance / dt  # pixel/second
                speeds.append(speed)
        
        return np.mean(speeds) if speeds else 0.0
    
    def _analyze_swing_path(self, racket_data: List[Dict]) -> Dict[str, any]:
        """スイング軌道解析"""
        return {"path_smoothness": 0.8, "path_length": 150}
    
    def _analyze_weight_transfer(self, pose_data: List[Dict]) -> Dict[str, any]:
        """体重移動解析"""
        return {"score": 0.75, "transfer_time": 0.3}
    
    def _analyze_timing(self, pose_data: List[Dict], racket_data: List[Dict]) -> Dict[str, any]:
        """タイミング解析"""
        return {"preparation_time": 0.8, "contact_timing": 0.9}
    
    def _analyze_stance_stability(self, pose_data: List[Dict]) -> Dict[str, any]:
        """スタンス安定性解析"""
        return {"score": 0.8, "foot_distance": 0.6}
    
    def _analyze_body_balance(self, pose_data: List[Dict]) -> Dict[str, any]:
        """体バランス解析"""
        return {"left_right_balance": 0.85, "forward_backward_balance": 0.9}
    
    def _analyze_foot_positioning(self, pose_data: List[Dict]) -> Dict[str, any]:
        """足の位置解析"""
        return {"stance_width": 0.7, "foot_angle": 45}
    
    # 以下、その他のヘルパーメソッドも同様に実装...