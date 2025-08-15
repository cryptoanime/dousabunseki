'use client'

import React, { useState } from 'react'
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
  LinearProgress,
  Avatar,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Badge,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material'
import {
  ArrowBack,
  TrendingUp,
  TrendingDown,
  EmojiEvents,
  CalendarToday,
  Assessment,
  Star,
  Grade,
  LocalFireDepartment,
  Timeline,
  CheckCircle,
  WorkspacePremium,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts'

const MotionCard = motion(Card)
const MotionBox = motion(Box)

// モックデータ
const progressData = [
  { week: '1週目', overall: 65, stance: 70, swing: 60, timing: 68, balance: 62 },
  { week: '2週目', overall: 68, stance: 72, swing: 64, timing: 70, balance: 66 },
  { week: '3週目', overall: 72, stance: 75, swing: 68, timing: 73, balance: 71 },
  { week: '4週目', overall: 76, stance: 78, swing: 72, timing: 76, balance: 75 },
]

const radarData = [
  { category: 'スタンス', current: 78, target: 85 },
  { category: 'スイング軌道', current: 72, target: 80 },
  { category: 'タイミング', current: 76, target: 82 },
  { category: 'バランス', current: 75, target: 80 },
  { category: 'フォロースルー', current: 70, target: 78 },
]

const achievements = [
  {
    id: 'first_analysis',
    title: '初回解析完了',
    description: '最初の動画解析を完了しました',
    icon: '🎯',
    earned: true,
    date: '2024-01-15'
  },
  {
    id: 'week_streak',
    title: '1週間連続練習',
    description: '7日間連続でトレーニングを実施',
    icon: '🔥',
    earned: true,
    date: '2024-01-20'
  },
  {
    id: 'score_improvement',
    title: 'スコア10点向上',
    description: '総合スコアが10点以上向上',
    icon: '📈',
    earned: true,
    date: '2024-01-25'
  },
  {
    id: 'perfect_stance',
    title: 'スタンスマスター',
    description: 'スタンススコア80点以上達成',
    icon: '⚡',
    earned: true,
    date: '2024-01-30'
  },
  {
    id: 'month_training',
    title: '1ヶ月継続',
    description: '1ヶ月間トレーニングを継続',
    icon: '🏆',
    earned: false,
    date: null
  },
  {
    id: 'expert_level',
    title: '上級者レベル',
    description: '総合スコア90点以上達成',
    icon: '👑',
    earned: false,
    date: null
  }
]

const recentActivities = [
  {
    date: '2024-02-01',
    type: 'analysis',
    title: '動画解析実施',
    score: 76,
    improvement: '+4'
  },
  {
    date: '2024-01-31',
    type: 'training',
    title: 'スイング改善トレーニング',
    duration: 30,
    exercises: 3
  },
  {
    date: '2024-01-30',
    type: 'achievement',
    title: 'スタンスマスター獲得',
    badge: 'スタンスマスター'
  },
  {
    date: '2024-01-29',
    type: 'training',
    title: 'バランス向上メニュー',
    duration: 20,
    exercises: 2
  }
]

export default function ProgressPage() {
  const router = useRouter()
  const [selectedTab, setSelectedTab] = useState(0)
  const [selectedAchievement, setSelectedAchievement] = useState<any>(null)

  const currentLevel = 'Bronze'
  const currentXP = 2840
  const nextLevelXP = 3000
  const progressToNext = (currentXP / nextLevelXP) * 100

  const handleAchievementClick = (achievement: any) => {
    setSelectedAchievement(achievement)
  }

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'analysis': return <Assessment color="primary" />
      case 'training': return <LocalFireDepartment color="warning" />
      case 'achievement': return <EmojiEvents color="success" />
      default: return <CheckCircle />
    }
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr)
    return `${date.getMonth() + 1}/${date.getDate()}`
  }

  return (
    <>
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <IconButton edge="start" color="inherit" onClick={() => router.back()}>
            <ArrowBack />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            進捗確認
          </Typography>
          <Chip label="Bronze Lv.8" color="warning" variant="filled" />
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* レベル・経験値 */}
        <MotionCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          sx={{ mb: 4, background: 'linear-gradient(135deg, #FFD54F 0%, #FFC107 100%)' }}
        >
          <CardContent>
            <Grid container spacing={3} alignItems="center">
              <Grid item xs={12} md={3} sx={{ textAlign: 'center' }}>
                <Avatar 
                  sx={{ 
                    width: 80, 
                    height: 80, 
                    mx: 'auto', 
                    mb: 2,
                    bgcolor: '#FF8F00',
                    fontSize: '2rem'
                  }}
                >
                  🎾
                </Avatar>
                <Typography variant="h6" fontWeight={600} sx={{ color: '#E65100' }}>
                  {currentLevel} Level 8
                </Typography>
              </Grid>
              <Grid item xs={12} md={9}>
                <Typography variant="h6" sx={{ mb: 2, color: '#E65100', fontWeight: 600 }}>
                  次のレベルまで: {nextLevelXP - currentXP} XP
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={progressToNext}
                  sx={{
                    height: 12,
                    borderRadius: 6,
                    bgcolor: 'rgba(255,255,255,0.3)',
                    '& .MuiLinearProgress-bar': {
                      bgcolor: '#FF8F00',
                      borderRadius: 6,
                    }
                  }}
                />
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                  <Typography variant="body2" sx={{ color: '#E65100' }}>
                    {currentXP} XP
                  </Typography>
                  <Typography variant="body2" sx={{ color: '#E65100' }}>
                    {nextLevelXP} XP
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </MotionCard>

        {/* タブ */}
        <Paper sx={{ mb: 4 }}>
          <Tabs
            value={selectedTab}
            onChange={(e, newValue) => setSelectedTab(newValue)}
            variant="fullWidth"
            sx={{ borderBottom: 1, borderColor: 'divider' }}
          >
            <Tab icon={<Timeline />} label="スコア推移" iconPosition="start" />
            <Tab icon={<EmojiEvents />} label="実績・バッジ" iconPosition="start" />
            <Tab icon={<CalendarToday />} label="活動履歴" iconPosition="start" />
          </Tabs>
        </Paper>

        {/* スコア推移タブ */}
        {selectedTab === 0 && (
          <Grid container spacing={4}>
            <Grid item xs={12} lg={8}>
              {/* 週別スコア推移 */}
              <MotionCard
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
                sx={{ mb: 4 }}
              >
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    📈 週別スコア推移
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={progressData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="week" />
                      <YAxis domain={[50, 100]} />
                      <Tooltip />
                      <Line 
                        type="monotone" 
                        dataKey="overall" 
                        stroke="#1565C0" 
                        strokeWidth={3}
                        name="総合スコア"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="stance" 
                        stroke="#4CAF50" 
                        strokeWidth={2}
                        name="スタンス"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="swing" 
                        stroke="#FF9800" 
                        strokeWidth={2}
                        name="スイング"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="timing" 
                        stroke="#9C27B0" 
                        strokeWidth={2}
                        name="タイミング"
                      />
                      <Line 
                        type="monotone" 
                        dataKey="balance" 
                        stroke="#F44336" 
                        strokeWidth={2}
                        name="バランス"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </MotionCard>

              {/* レーダーチャート */}
              <MotionCard
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    🎯 現在の能力と目標
                  </Typography>
                  <ResponsiveContainer width="100%" height={400}>
                    <RadarChart data={radarData}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="category" />
                      <PolarRadiusAxis angle={90} domain={[0, 100]} />
                      <Radar
                        name="現在のスコア"
                        dataKey="current"
                        stroke="#1565C0"
                        fill="#1565C0"
                        fillOpacity={0.3}
                        strokeWidth={2}
                      />
                      <Radar
                        name="目標スコア"
                        dataKey="target"
                        stroke="#4CAF50"
                        fill="#4CAF50"
                        fillOpacity={0.1}
                        strokeWidth={2}
                        strokeDasharray="5 5"
                      />
                      <Tooltip />
                    </RadarChart>
                  </ResponsiveContainer>
                </CardContent>
              </MotionCard>
            </Grid>

            <Grid item xs={12} lg={4}>
              {/* 統計サマリー */}
              <MotionCard
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
                sx={{ mb: 3 }}
              >
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    📊 今月の統計
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Paper sx={{ p: 2, textAlign: 'center' }}>
                        <Typography variant="h4" fontWeight={700} color="primary">
                          11
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          総合スコア向上
                        </Typography>
                      </Paper>
                    </Grid>
                    <Grid item xs={6}>
                      <Paper sx={{ p: 2, textAlign: 'center' }}>
                        <Typography variant="h4" fontWeight={700} color="success.main">
                          8
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          解析回数
                        </Typography>
                      </Paper>
                    </Grid>
                    <Grid item xs={6}>
                      <Paper sx={{ p: 2, textAlign: 'center' }}>
                        <Typography variant="h4" fontWeight={700} color="warning.main">
                          12
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          練習セッション
                        </Typography>
                      </Paper>
                    </Grid>
                    <Grid item xs={6}>
                      <Paper sx={{ p: 2, textAlign: 'center' }}>
                        <Typography variant="h4" fontWeight={700} color="error.main">
                          240
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          練習時間（分）
                        </Typography>
                      </Paper>
                    </Grid>
                  </Grid>
                </CardContent>
              </MotionCard>

              {/* 弱点・強化ポイント */}
              <MotionCard
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <CardContent>
                  <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                    💪 重点強化エリア
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemIcon>
                        <TrendingUp color="success" />
                      </ListItemIcon>
                      <ListItemText 
                        primary="スタンス" 
                        secondary="78点 (+8点向上)"
                        primaryTypographyProps={{ fontWeight: 600 }}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon>
                        <TrendingDown color="warning" />
                      </ListItemIcon>
                      <ListItemText 
                        primary="スイング軌道" 
                        secondary="72点 (要改善)"
                        primaryTypographyProps={{ fontWeight: 600 }}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemIcon>
                        <TrendingUp color="primary" />
                      </ListItemIcon>
                      <ListItemText 
                        primary="タイミング" 
                        secondary="76点 (+8点向上)"
                        primaryTypographyProps={{ fontWeight: 600 }}
                      />
                    </ListItem>
                  </List>
                </CardContent>
              </MotionCard>
            </Grid>
          </Grid>
        )}

        {/* 実績・バッジタブ */}
        {selectedTab === 1 && (
          <Grid container spacing={3}>
            {achievements.map((achievement, index) => (
              <Grid item xs={12} sm={6} md={4} key={achievement.id}>
                <MotionCard
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  onClick={() => handleAchievementClick(achievement)}
                  sx={{
                    cursor: 'pointer',
                    opacity: achievement.earned ? 1 : 0.6,
                    background: achievement.earned 
                      ? 'linear-gradient(135deg, #FFD700 0%, #FFA000 100%)'
                      : 'linear-gradient(135deg, #E0E0E0 0%, #BDBDBD 100%)',
                    '&:hover': {
                      transform: 'scale(1.02)',
                    },
                    transition: 'transform 0.2s'
                  }}
                >
                  <CardContent sx={{ textAlign: 'center' }}>
                    <Typography variant="h2" sx={{ mb: 2 }}>
                      {achievement.icon}
                    </Typography>
                    <Typography 
                      variant="h6" 
                      fontWeight={600} 
                      sx={{ 
                        mb: 1,
                        color: achievement.earned ? '#E65100' : '#757575'
                      }}
                    >
                      {achievement.title}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      sx={{ 
                        color: achievement.earned ? '#BF360C' : '#9E9E9E'
                      }}
                    >
                      {achievement.description}
                    </Typography>
                    {achievement.earned && achievement.date && (
                      <Chip 
                        label={`${formatDate(achievement.date)} 獲得`}
                        size="small"
                        sx={{ mt: 2, bgcolor: 'rgba(255,255,255,0.3)' }}
                      />
                    )}
                    {!achievement.earned && (
                      <Chip 
                        label="未獲得"
                        size="small"
                        sx={{ mt: 2, bgcolor: 'rgba(255,255,255,0.3)' }}
                      />
                    )}
                  </CardContent>
                </MotionCard>
              </Grid>
            ))}
          </Grid>
        )}

        {/* 活動履歴タブ */}
        {selectedTab === 2 && (
          <MotionCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 600 }}>
                📅 最近の活動
              </Typography>
              <List>
                {recentActivities.map((activity, index) => (
                  <React.Fragment key={index}>
                    <ListItem>
                      <ListItemIcon>
                        {getActivityIcon(activity.type)}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="body1" fontWeight={600}>
                              {activity.title}
                            </Typography>
                            {activity.type === 'analysis' && activity.improvement && (
                              <Chip 
                                label={activity.improvement}
                                size="small"
                                color="success"
                                variant="outlined"
                              />
                            )}
                          </Box>
                        }
                        secondary={
                          <Box>
                            <Typography variant="body2" color="text.secondary">
                              {formatDate(activity.date)}
                            </Typography>
                            {activity.type === 'analysis' && (
                              <Typography variant="body2">
                                総合スコア: {activity.score}点
                              </Typography>
                            )}
                            {activity.type === 'training' && (
                              <Typography variant="body2">
                                {activity.duration}分間 • {activity.exercises}種類のエクササイズ
                              </Typography>
                            )}
                            {activity.type === 'achievement' && (
                              <Typography variant="body2">
                                バッジ「{activity.badge}」を獲得
                              </Typography>
                            )}
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < recentActivities.length - 1 && <Box sx={{ pl: 7 }}></Box>}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </MotionCard>
        )}
      </Container>

      {/* 実績詳細ダイアログ */}
      <Dialog
        open={!!selectedAchievement}
        onClose={() => setSelectedAchievement(null)}
        maxWidth="sm"
        fullWidth
      >
        {selectedAchievement && (
          <>
            <DialogTitle sx={{ textAlign: 'center' }}>
              <Typography variant="h3" sx={{ mb: 1 }}>
                {selectedAchievement.icon}
              </Typography>
              <Typography variant="h6" fontWeight={600}>
                {selectedAchievement.title}
              </Typography>
            </DialogTitle>
            <DialogContent>
              <Typography variant="body1" sx={{ textAlign: 'center', mb: 2 }}>
                {selectedAchievement.description}
              </Typography>
              {selectedAchievement.earned ? (
                <Chip 
                  label={`${formatDate(selectedAchievement.date)} 獲得`}
                  color="success"
                  sx={{ display: 'block', mx: 'auto', width: 'fit-content' }}
                />
              ) : (
                <Chip 
                  label="まだ獲得していません"
                  color="default"
                  sx={{ display: 'block', mx: 'auto', width: 'fit-content' }}
                />
              )}
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setSelectedAchievement(null)}>
                閉じる
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </>
  )
}