'use client'

import React from 'react'
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  Button,
  Grid,
  AppBar,
  Toolbar,
  Paper,
  Chip,
} from '@mui/material'
import {
  VideoCall,
  FitnessCenter,
  TrendingUp,
  EmojiEvents,
  Speed,
  Assessment,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'

const MotionCard = motion(Card)
const MotionBox = motion(Box)

export default function HomePage() {
  const router = useRouter()

  const features = [
    {
      icon: <VideoCall sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: '動画解析',
      subtitle: 'フォームを分析して改善提案を受ける',
      description: '10-30秒の動画をアップロードするだけで、AIが詳細なフォーム分析を行います',
      color: '#4CAF50',
      href: '/upload',
    },
    {
      icon: <FitnessCenter sx={{ fontSize: 40, color: 'warning.main' }} />,
      title: 'トレーニング',
      subtitle: 'あなた専用の練習メニュー',
      description: '弱点に応じたカスタムトレーニングメニューを自動生成',
      color: '#FF9800',
      href: '/training',
    },
    {
      icon: <TrendingUp sx={{ fontSize: 40, color: 'secondary.main' }} />,
      title: '進捗確認',
      subtitle: '上達の記録を確認',
      description: 'レベルシステムとバッジで上達過程を可視化',
      color: '#9C27B0',
      href: '/progress',
    },
  ]

  const stats = [
    { icon: <EmojiEvents />, label: '解析精度', value: '95%' },
    { icon: <Speed />, label: '解析時間', value: '30秒' },
    { icon: <Assessment />, label: '改善項目', value: '5種類' },
  ]

  return (
    <>
      {/* ヘッダー */}
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 700 }}>
            🎾 SoftTennis AI Coach
          </Typography>
          <Chip 
            label="完全無料" 
            color="secondary" 
            variant="filled"
            sx={{ fontWeight: 600 }}
          />
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ py: 4 }}>
        {/* ヒーロー セクション */}
        <MotionBox
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          sx={{ textAlign: 'center', mb: 6 }}
        >
          <Typography 
            variant="h1" 
            component="h1" 
            sx={{ 
              mb: 2,
              background: 'linear-gradient(45deg, #1565C0 30%, #4CAF50 90%)',
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            軟式テニス上達への道
          </Typography>
          <Typography 
            variant="h5" 
            color="text.secondary" 
            sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}
          >
            動画をアップロードするだけで、AIが詳細なフォーム分析を行い、
            個別の改善提案とトレーニングメニューを提供します
          </Typography>

          {/* 統計情報 */}
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 4, mb: 4 }}>
            {stats.map((stat, index) => (
              <MotionBox
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                sx={{ textAlign: 'center' }}
              >
                <Box sx={{ color: 'primary.main', mb: 1 }}>
                  {stat.icon}
                </Box>
                <Typography variant="h4" fontWeight={700} color="primary">
                  {stat.value}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stat.label}
                </Typography>
              </MotionBox>
            ))}
          </Box>

          <Button
            variant="contained"
            size="large"
            onClick={() => router.push('/upload')}
            sx={{
              fontSize: '1.2rem',
              py: 2,
              px: 4,
              background: 'linear-gradient(45deg, #1565C0 30%, #4CAF50 90%)',
            }}
          >
            今すぐ始める
          </Button>
        </MotionBox>

        {/* 機能カード */}
        <Grid container spacing={4} sx={{ mb: 6 }}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={4} key={feature.title}>
              <MotionCard
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                sx={{ 
                  height: '100%',
                  cursor: 'pointer',
                  transition: 'transform 0.3s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                  },
                }}
                onClick={() => router.push(feature.href)}
              >
                <CardContent sx={{ p: 3, textAlign: 'center' }}>
                  <Box sx={{ mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h5" component="h2" fontWeight={600} sx={{ mb: 1 }}>
                    {feature.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
                    {feature.subtitle}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </MotionCard>
            </Grid>
          ))}
        </Grid>

        {/* 今日のヒント */}
        <MotionCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          sx={{
            background: 'linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%)',
            border: '1px solid #FFB74D',
          }}
        >
          <CardContent sx={{ p: 3 }}>
            <Typography 
              variant="h6" 
              component="h3" 
              sx={{ 
                mb: 2, 
                color: '#E65100',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: 1,
              }}
            >
              💡 今日のヒント
            </Typography>
            <Typography variant="body1" color="text.secondary">
              軟式テニスでは、ボールのバウンドが低いので膝を曲げて低い姿勢を心がけましょう！
              また、軟式ボールは変形しやすいため、インパクトの瞬間はラケット面を安定させることが重要です。
            </Typography>
          </CardContent>
        </MotionCard>

        {/* 特徴 */}
        <Box sx={{ mt: 6, textAlign: 'center' }}>
          <Typography variant="h4" component="h2" sx={{ mb: 4, fontWeight: 600 }}>
            なぜSoftTennis AI Coachなのか？
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <Typography variant="h6" sx={{ mb: 1, color: 'primary.main' }}>
                  🎯 軟式特化
                </Typography>
                <Typography variant="body2">
                  軟式テニス専用に最適化されたAI解析
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <Typography variant="h6" sx={{ mb: 1, color: 'primary.main' }}>
                  🔬 高精度
                </Typography>
                <Typography variant="body2">
                  Kinovea技術を移植した精密な動作追跡
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <Typography variant="h6" sx={{ mb: 1, color: 'primary.main' }}>
                  📱 簡単操作
                </Typography>
                <Typography variant="body2">
                  動画アップロードだけで詳細分析
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <Typography variant="h6" sx={{ mb: 1, color: 'primary.main' }}>
                  🆓 完全無料
                </Typography>
                <Typography variant="body2">
                  すべての機能を無料で利用可能
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        </Box>
      </Container>
    </>
  )
}