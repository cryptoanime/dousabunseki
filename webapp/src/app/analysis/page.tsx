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
  LinearProgress,
  Paper,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Alert,
} from '@mui/material'
import {
  ArrowBack,
  TrendingUp,
  TrendingDown,
  CheckCircle,
  Warning,
  Info,
  FitnessCenter,
  Assessment,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useRouter, useSearchParams } from 'next/navigation'

const MotionCard = motion(Card)
const MotionBox = motion(Box)

// 模擬的な解析結果データ
const mockAnalysisResult = {
  sessionId: 'analysis_123456',
  overallScore: 75.5,
  categoryScores: {
    stance: { score: 80.0, percentage: 80.0, details: { foot_distance: 85, knee_bend: 75 } },
    swing_path: { score: 70.0, percentage: 70.0, details: { swing_speed: 65, swing_arc: 75 } },
    timing: { score: 78.0, percentage: 78.0, details: { preparation_time: 80 } },
    balance: { score: 72.0, percentage: 72.0, details: { left_right_balance: 70, stability: 74 } },
  },
  strengths: [
    '安定したスタンスができています',
    'タイミングが適切です',
    '基本的なフォームの土台ができつつあります'
  ],
  weaknesses: [
    'スイングスピードの向上が必要',
    'バランスの安定性',
  ],
  improvementPoints: [
    {
      category: 'swing_path',
      priority: 'high',
      title: 'スイングスピードの向上',
      description: 'ラケットの振りが遅く、ボールに十分な威力が伝わっていません',
      advice: '体重移動を使って、よりダイナミックにスイングしましょう。腰の回転から肩、腕の順番で力を伝える運動連鎖を意識してください。',
      trainingFocus: ['素振り練習', '体重移動練習', 'シャドースイング']
    },
    {
      category: 'balance',
      priority: 'medium',
      title: 'バランスの安定性向上',
      description: '打球時に体が左右に揺れています',
      advice: '軸足をしっかり固定し、安定したスイングを心がけましょう。',
      trainingFocus: ['片足立ち練習', 'バランスボール練習']
    }
  ],
  recommendedTraining: [
    '素振り練習',
    '体重移動練習',
    'シャドースイング',
    '片足立ち練習',
    '壁打ち練習（軟式ボール専用）',
    'トップスピン練習'
  ]
}

export default function AnalysisResultPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [isLoading, setIsLoading] = useState(true)
  const [analysisResult, setAnalysisResult] = useState(mockAnalysisResult)

  useEffect(() => {
    // 模擬的なローディング
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 2000)

    return () => clearTimeout(timer)
  }, [])

  const getScoreColor = (score: number) => {
    if (score >= 80) return '#4CAF50'
    if (score >= 60) return '#FF9800'
    return '#F44336'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 80) return '良好'
    if (score >= 60) return '改善の余地あり'
    return '要改善'
  }

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'high': return <Warning color="error" />
      case 'medium': return <Info color="warning" />
      default: return <CheckCircle color="success" />
    }
  }

  if (isLoading) {
    return (
      <>
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <IconButton edge="start" color="inherit" onClick={() => router.back()}>
              <ArrowBack />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              解析中...
            </Typography>
          </Toolbar>
        </AppBar>
        <Container maxWidth="md" sx={{ py: 4 }}>
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 6 }}>
              <Typography variant="h5" sx={{ mb: 3 }}>
                🎾 フォームを解析中...
              </Typography>
              <LinearProgress sx={{ mb: 2 }} />
              <Typography variant="body2" color="text.secondary">
                AIが動画を詳細に分析しています。しばらくお待ちください。
              </Typography>
            </CardContent>
          </Card>
        </Container>
      </>
    )
  }

  return (
    <>
      {/* ヘッダー */}
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <IconButton edge="start" color="inherit" onClick={() => router.back()}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            解析結果
          </Typography>
          <Chip 
            label={`総合スコア: ${analysisResult.overallScore}点`} 
            color="primary" 
            variant="filled"
          />
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* 総合スコア */}
        <MotionCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          sx={{ mb: 4, textAlign: 'center' }}
        >
          <CardContent sx={{ py: 4 }}>
            <Typography variant="h3" component="h1" sx={{ mb: 2, fontWeight: 700 }}>
              {analysisResult.overallScore}
              <Typography component="span" variant="h5" color="text.secondary">
                /100
              </Typography>
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ mb: 3 }}>
              総合フォームスコア
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={analysisResult.overallScore} 
              sx={{ 
                height: 12, 
                borderRadius: 6,
                bgcolor: 'grey.200',
                '& .MuiLinearProgress-bar': {
                  bgcolor: getScoreColor(analysisResult.overallScore),
                  borderRadius: 6,
                }
              }} 
            />
          </CardContent>
        </MotionCard>

        <Grid container spacing={4}>
          {/* カテゴリ別スコア */}
          <Grid item xs={12} md={8}>
            <MotionCard
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              sx={{ mb: 4 }}
            >
              <CardContent>
                <Typography variant="h6" component="h2" sx={{ mb: 3, fontWeight: 600 }}>
                  📊 カテゴリ別評価
                </Typography>
                <Grid container spacing={3}>
                  {Object.entries(analysisResult.categoryScores).map(([category, data]) => {
                    const categoryNames: { [key: string]: string } = {
                      stance: 'スタンス',
                      swing_path: 'スイング軌道',
                      timing: 'タイミング',
                      balance: 'バランス',
                    }
                    
                    return (
                      <Grid item xs={12} sm={6} key={category}>
                        <Paper sx={{ p: 3 }}>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                            <Typography variant="h6" fontWeight={600}>
                              {categoryNames[category]}
                            </Typography>
                            <Chip 
                              label={`${data.score}点`}
                              size="small"
                              sx={{ 
                                bgcolor: getScoreColor(data.score),
                                color: 'white',
                                fontWeight: 600,
                              }}
                            />
                          </Box>
                          <LinearProgress 
                            variant="determinate" 
                            value={data.percentage} 
                            sx={{ 
                              mb: 1,
                              height: 8,
                              borderRadius: 4,
                              '& .MuiLinearProgress-bar': {
                                bgcolor: getScoreColor(data.score),
                                borderRadius: 4,
                              }
                            }}
                          />
                          <Typography variant="body2" color="text.secondary">
                            {getScoreLabel(data.score)}
                          </Typography>
                        </Paper>
                      </Grid>
                    )
                  })}
                </Grid>
              </CardContent>
            </MotionCard>

            {/* 改善ポイント */}
            <MotionCard
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <CardContent>
                <Typography variant="h6" component="h2" sx={{ mb: 3, fontWeight: 600 }}>
                  🎯 改善ポイント
                </Typography>
                {analysisResult.improvementPoints.map((point, index) => (
                  <Card key={index} variant="outlined" sx={{ mb: 3 }}>
                    <CardContent>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        {getPriorityIcon(point.priority)}
                        <Typography variant="h6" sx={{ ml: 1, fontWeight: 600 }}>
                          {point.title}
                        </Typography>
                        <Chip 
                          label={point.priority === 'high' ? '高優先度' : '中優先度'}
                          size="small"
                          color={point.priority === 'high' ? 'error' : 'warning'}
                          sx={{ ml: 'auto' }}
                        />
                      </Box>
                      <Typography variant="body1" sx={{ mb: 2 }}>
                        {point.description}
                      </Typography>
                      <Alert severity="info" sx={{ mb: 2 }}>
                        <Typography variant="body2">
                          <strong>改善アドバイス:</strong> {point.advice}
                        </Typography>
                      </Alert>
                      <Typography variant="body2" color="text.secondary">
                        <strong>重点練習:</strong> {point.trainingFocus.join(', ')}
                      </Typography>
                    </CardContent>
                  </Card>
                ))}
              </CardContent>
            </MotionCard>
          </Grid>

          {/* サイドバー */}
          <Grid item xs={12} md={4}>
            {/* 長所 */}
            <MotionCard
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              sx={{ mb: 3, background: 'linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%)' }}
            >
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, color: '#2E7D32', fontWeight: 600 }}>
                  ✅ あなたの長所
                </Typography>
                <List dense>
                  {analysisResult.strengths.map((strength, index) => (
                    <ListItem key={index} disablePadding>
                      <ListItemIcon>
                        <TrendingUp color="success" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={strength}
                        primaryTypographyProps={{ variant: 'body2' }}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </MotionCard>

            {/* 弱点 */}
            <MotionCard
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              sx={{ mb: 3, background: 'linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%)' }}
            >
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, color: '#E65100', fontWeight: 600 }}>
                  📈 改善エリア
                </Typography>
                <List dense>
                  {analysisResult.weaknesses.map((weakness, index) => (
                    <ListItem key={index} disablePadding>
                      <ListItemIcon>
                        <TrendingDown color="warning" />
                      </ListItemIcon>
                      <ListItemText 
                        primary={weakness}
                        primaryTypographyProps={{ variant: 'body2' }}
                      />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </MotionCard>

            {/* 推奨トレーニング */}
            <MotionCard
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
            >
              <CardContent>
                <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                  💪 推奨トレーニング
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {analysisResult.recommendedTraining.map((training, index) => (
                    <Chip 
                      key={index}
                      label={training}
                      size="small"
                      variant="outlined"
                      color="primary"
                    />
                  ))}
                </Box>
              </CardContent>
            </MotionCard>
          </Grid>
        </Grid>

        {/* アクションボタン */}
        <Box sx={{ mt: 4, display: 'flex', gap: 2, justifyContent: 'center' }}>
          <Button
            variant="contained"
            size="large"
            startIcon={<FitnessCenter />}
            onClick={() => router.push('/training')}
            sx={{
              background: 'linear-gradient(45deg, #FF9800 30%, #FFB74D 90%)',
              minWidth: 200,
            }}
          >
            トレーニングを開始
          </Button>
          <Button
            variant="outlined"
            size="large"
            startIcon={<Assessment />}
            onClick={() => router.push('/progress')}
          >
            進捗を確認
          </Button>
        </Box>
      </Container>
    </>
  )
}