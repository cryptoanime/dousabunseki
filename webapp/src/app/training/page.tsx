'use client'

import React, { useState, useEffect } from 'react'
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Button,
  AppBar,
  Toolbar,
  IconButton,
  Grid,
  Chip,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Tabs,
  Tab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Alert,
} from '@mui/material'
import {
  ArrowBack,
  FitnessCenter,
  Home,
  SportsTennis,
  PlayArrow,
  CheckCircle,
  ExpandMore,
  AccessTime,
  TrendingUp,
  EmojiEvents,
  Schedule,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'

const MotionCard = motion(Card)
const MotionBox = motion(Box)

interface TrainingExercise {
  id: string
  name: string
  duration: number
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  description: string
  instructions: string[]
  equipment?: string[]
  targetAreas: string[]
}

interface TrainingSession {
  id: string
  title: string
  duration: number
  exercises: TrainingExercise[]
  type: 'court' | 'home'
  level: string
}

const mockTrainingSessions: TrainingSession[] = [
  {
    id: 'session1',
    title: 'スイングスピード向上メニュー',
    duration: 30,
    type: 'court',
    level: '初級',
    exercises: [
      {
        id: 'ex1',
        name: '素振り練習（スロー→高速）',
        duration: 10,
        difficulty: 'beginner',
        description: 'ゆっくりとした素振りから徐々にスピードを上げる練習',
        instructions: [
          '正しいフォームで10回ゆっくり素振り',
          '中程度のスピードで10回素振り',
          '最大スピードで10回素振り',
          '各セット間に30秒休憩'
        ],
        equipment: ['ラケット'],
        targetAreas: ['スイングスピード', 'フォーム安定']
      },
      {
        id: 'ex2',
        name: '体重移動練習',
        duration: 15,
        difficulty: 'beginner',
        description: '後足から前足への体重移動を意識した練習',
        instructions: [
          '後足に体重をかけてテイクバック',
          'スイング時に前足に体重移動',
          '左右の足の重心移動を意識',
          '20回繰り返し × 2セット'
        ],
        equipment: ['ラケット'],
        targetAreas: ['体重移動', 'バランス']
      },
      {
        id: 'ex3',
        name: '壁打ち練習',
        duration: 5,
        difficulty: 'beginner',
        description: '軟式ボール専用の壁打ち練習',
        instructions: [
          '壁から3メートル離れて立つ',
          '軟式ボールでコントロール重視の打球',
          '連続で20回壁打ち',
          'ボールのバウンドに合わせてタイミング調整'
        ],
        equipment: ['ラケット', '軟式ボール', '壁'],
        targetAreas: ['タイミング', 'コントロール']
      }
    ]
  },
  {
    id: 'session2',
    title: 'バランス向上ホームトレーニング',
    duration: 20,
    type: 'home',
    level: '初級',
    exercises: [
      {
        id: 'ex4',
        name: '片足立ち練習',
        duration: 8,
        difficulty: 'beginner',
        description: '軸足の安定性を向上させる基礎練習',
        instructions: [
          '右足で30秒間片足立ち',
          '左足で30秒間片足立ち',
          '目を閉じて右足で15秒',
          '目を閉じて左足で15秒',
          '3セット繰り返し'
        ],
        equipment: [],
        targetAreas: ['バランス', '体幹強化']
      },
      {
        id: 'ex5',
        name: 'シャドースイング',
        duration: 12,
        difficulty: 'beginner',
        description: 'ラケットを使った室内でのフォーム練習',
        instructions: [
          '鏡の前で正しいフォームを確認',
          'フォアハンド10回をゆっくり',
          'バックハンド10回をゆっくり',
          '体重移動を意識してスイング',
          '3セット繰り返し'
        ],
        equipment: ['ラケット', '鏡'],
        targetAreas: ['フォーム', 'スイング軌道']
      }
    ]
  }
]

export default function TrainingPage() {
  const router = useRouter()
  const [selectedTab, setSelectedTab] = useState(0)
  const [currentSession, setCurrentSession] = useState<TrainingSession | null>(null)
  const [isTraining, setIsTraining] = useState(false)
  const [completedExercises, setCompletedExercises] = useState<Set<string>>(new Set())
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0)
  const [timer, setTimer] = useState(0)
  const [isTimerRunning, setIsTimerRunning] = useState(false)

  useEffect(() => {
    let interval: NodeJS.Timeout
    if (isTimerRunning) {
      interval = setInterval(() => {
        setTimer(prev => prev + 1)
      }, 1000)
    }
    return () => clearInterval(interval)
  }, [isTimerRunning])

  const courtSessions = mockTrainingSessions.filter(s => s.type === 'court')
  const homeSessions = mockTrainingSessions.filter(s => s.type === 'home')

  const handleStartSession = (session: TrainingSession) => {
    setCurrentSession(session)
    setIsTraining(true)
    setCurrentExerciseIndex(0)
    setCompletedExercises(new Set())
    setTimer(0)
    setIsTimerRunning(true)
  }

  const handleCompleteExercise = (exerciseId: string) => {
    const newCompleted = new Set(completedExercises)
    newCompleted.add(exerciseId)
    setCompletedExercises(newCompleted)

    if (currentSession && currentExerciseIndex < currentSession.exercises.length - 1) {
      setCurrentExerciseIndex(prev => prev + 1)
    } else {
      // セッション完了
      setIsTimerRunning(false)
      setTimeout(() => {
        setIsTraining(false)
        setCurrentSession(null)
      }, 2000)
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return '#4CAF50'
      case 'intermediate': return '#FF9800'
      case 'advanced': return '#F44336'
      default: return '#4CAF50'
    }
  }

  const getDifficultyLabel = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return '初級'
      case 'intermediate': return '中級'
      case 'advanced': return '上級'
      default: return '初級'
    }
  }

  if (isTraining && currentSession) {
    const currentExercise = currentSession.exercises[currentExerciseIndex]
    const progress = ((currentExerciseIndex + 1) / currentSession.exercises.length) * 100

    return (
      <>
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <IconButton edge="start" color="inherit" onClick={() => setIsTraining(false)}>
              <ArrowBack />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
              {currentSession.title}
            </Typography>
            <Chip label={formatTime(timer)} color="primary" variant="filled" />
          </Toolbar>
        </AppBar>

        <Container maxWidth="md" sx={{ py: 4 }}>
          {/* 進捗表示 */}
          <Card sx={{ mb: 4 }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                進捗: {currentExerciseIndex + 1}/{currentSession.exercises.length}
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={progress} 
                sx={{ height: 8, borderRadius: 4, mb: 2 }}
              />
              <Typography variant="body2" color="text.secondary">
                {Math.round(progress)}% 完了
              </Typography>
            </CardContent>
          </Card>

          {/* 現在のエクササイズ */}
          <MotionCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
            sx={{ mb: 4 }}
          >
            <CardContent sx={{ p: 4 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                <FitnessCenter sx={{ mr: 2, color: 'primary.main' }} />
                <Typography variant="h5" fontWeight={600}>
                  {currentExercise.name}
                </Typography>
                <Chip 
                  label={`${currentExercise.duration}分`}
                  size="small"
                  sx={{ ml: 'auto' }}
                />
              </Box>

              <Typography variant="body1" sx={{ mb: 3 }}>
                {currentExercise.description}
              </Typography>

              <Typography variant="h6" sx={{ mb: 2 }}>
                実施手順:
              </Typography>
              <List dense>
                {currentExercise.instructions.map((instruction, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Typography variant="body2" fontWeight={600}>
                        {index + 1}.
                      </Typography>
                    </ListItemIcon>
                    <ListItemText primary={instruction} />
                  </ListItem>
                ))}
              </List>

              {currentExercise.equipment && currentExercise.equipment.length > 0 && (
                <Alert severity="info" sx={{ mt: 2 }}>
                  <Typography variant="body2">
                    <strong>必要な用具:</strong> {currentExercise.equipment.join(', ')}
                  </Typography>
                </Alert>
              )}
            </CardContent>
          </MotionCard>

          {/* 完了ボタン */}
          <Button
            variant="contained"
            size="large"
            fullWidth
            onClick={() => handleCompleteExercise(currentExercise.id)}
            disabled={completedExercises.has(currentExercise.id)}
            sx={{
              py: 2,
              fontSize: '1.1rem',
              background: completedExercises.has(currentExercise.id) 
                ? undefined 
                : 'linear-gradient(45deg, #4CAF50 30%, #66BB6A 90%)',
            }}
            startIcon={completedExercises.has(currentExercise.id) ? <CheckCircle /> : <PlayArrow />}
          >
            {completedExercises.has(currentExercise.id) ? '完了' : 'エクササイズ完了'}
          </Button>
        </Container>
      </>
    )
  }

  return (
    <>
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <IconButton edge="start" color="inherit" onClick={() => router.back()}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            トレーニングメニュー
          </Typography>
          <Chip label="30分メニュー" color="secondary" variant="filled" />
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* 今日のおすすめ */}
        <MotionCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          sx={{ mb: 4, background: 'linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%)' }}
        >
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2, color: '#2E7D32', fontWeight: 600 }}>
              🎯 今日のおすすめトレーニング
            </Typography>
            <Typography variant="body1" sx={{ mb: 2 }}>
              前回の解析結果に基づいて、「スイングスピード向上」を重点的に練習しましょう！
            </Typography>
            <Button
              variant="contained"
              startIcon={<TrendingUp />}
              onClick={() => handleStartSession(courtSessions[0])}
              sx={{ background: 'linear-gradient(45deg, #4CAF50 30%, #66BB6A 90%)' }}
            >
              おすすめメニューを開始
            </Button>
          </CardContent>
        </MotionCard>

        {/* タブ切り替え */}
        <Paper sx={{ mb: 4 }}>
          <Tabs
            value={selectedTab}
            onChange={(e, newValue) => setSelectedTab(newValue)}
            variant="fullWidth"
            sx={{ borderBottom: 1, borderColor: 'divider' }}
          >
            <Tab 
              icon={<SportsTennis />} 
              label="コート練習" 
              iconPosition="start"
            />
            <Tab 
              icon={<Home />} 
              label="自宅練習" 
              iconPosition="start"
            />
          </Tabs>
        </Paper>

        {/* トレーニングセッション一覧 */}
        <Grid container spacing={4}>
          {(selectedTab === 0 ? courtSessions : homeSessions).map((session, index) => (
            <Grid item xs={12} md={6} key={session.id}>
              <MotionCard
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                sx={{ height: '100%' }}
              >
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Typography variant="h6" fontWeight={600} sx={{ flexGrow: 1 }}>
                      {session.title}
                    </Typography>
                    <Chip 
                      label={session.level}
                      size="small"
                      sx={{ 
                        bgcolor: getDifficultyColor('beginner'),
                        color: 'white',
                      }}
                    />
                  </Box>

                  <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
                    <Chip 
                      icon={<AccessTime />}
                      label={`${session.duration}分`}
                      size="small"
                      variant="outlined"
                    />
                    <Chip 
                      icon={session.type === 'court' ? <SportsTennis /> : <Home />}
                      label={session.type === 'court' ? 'コート' : '自宅'}
                      size="small"
                      variant="outlined"
                    />
                  </Box>

                  <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                    {session.exercises.length}種類のエクササイズ
                  </Typography>

                  {/* エクササイズ詳細 */}
                  {session.exercises.map((exercise, exerciseIndex) => (
                    <Accordion key={exercise.id} elevation={0}>
                      <AccordionSummary
                        expandIcon={<ExpandMore />}
                        sx={{ px: 0 }}
                      >
                        <Typography variant="body2" fontWeight={600}>
                          {exerciseIndex + 1}. {exercise.name} ({exercise.duration}分)
                        </Typography>
                      </AccordionSummary>
                      <AccordionDetails sx={{ px: 0 }}>
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                          {exercise.description}
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {exercise.targetAreas.map((area) => (
                            <Chip 
                              key={area}
                              label={area}
                              size="small"
                              variant="outlined"
                              color="primary"
                            />
                          ))}
                        </Box>
                      </AccordionDetails>
                    </Accordion>
                  ))}

                  <Button
                    variant="contained"
                    fullWidth
                    size="large"
                    onClick={() => handleStartSession(session)}
                    sx={{ 
                      mt: 3,
                      background: 'linear-gradient(45deg, #FF9800 30%, #FFB74D 90%)'
                    }}
                    startIcon={<PlayArrow />}
                  >
                    トレーニング開始
                  </Button>
                </CardContent>
              </MotionCard>
            </Grid>
          ))}
        </Grid>

        {/* 成果の可視化 */}
        <MotionCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          sx={{ mt: 4 }}
        >
          <CardContent>
            <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
              📈 今週のトレーニング成果
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} sm={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <EmojiEvents sx={{ fontSize: 40, color: '#FFD700', mb: 1 }} />
                  <Typography variant="h4" fontWeight={700} color="primary">
                    3
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    今週完了セッション
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Schedule sx={{ fontSize: 40, color: '#4CAF50', mb: 1 }} />
                  <Typography variant="h4" fontWeight={700} color="primary">
                    90
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    今週練習時間（分）
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <TrendingUp sx={{ fontSize: 40, color: '#FF9800', mb: 1 }} />
                  <Typography variant="h4" fontWeight={700} color="primary">
                    +5
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    フォームスコア向上
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </CardContent>
        </MotionCard>
      </Container>
    </>
  )
}