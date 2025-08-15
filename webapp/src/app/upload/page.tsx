'use client'

import React, { useState, useCallback } from 'react'
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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  LinearProgress,
  Chip,
  Paper,
  Grid,
} from '@mui/material'
import {
  ArrowBack,
  CloudUpload,
  VideoFile,
  CheckCircle,
  Info,
} from '@mui/icons-material'
import { useDropzone } from 'react-dropzone'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'

const MotionCard = motion(Card)
const MotionBox = motion(Box)

export default function VideoUploadPage() {
  const router = useRouter()
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [selectedAngle, setSelectedAngle] = useState<string>('')
  const [showAngleDialog, setShowAngleDialog] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      // 動画ファイルの検証
      if (file.type.startsWith('video/')) {
        // ファイルサイズチェック (30MB以下)
        if (file.size <= 30 * 1024 * 1024) {
          setSelectedFile(file)
          setShowAngleDialog(true)
        } else {
          alert('ファイルサイズが大きすぎます。30MB以下の動画を選択してください。')
        }
      } else {
        alert('動画ファイルを選択してください。')
      }
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.mov', '.avi', '.mkv']
    },
    multiple: false
  })

  const handleAngleSelect = (angle: string) => {
    setSelectedAngle(angle)
    setShowAngleDialog(false)
  }

  const handleUpload = async () => {
    if (!selectedFile || !selectedAngle) return

    setIsUploading(true)
    setUploadProgress(0)

    // 模擬的なアップロード進捗
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval)
          return 90
        }
        return prev + 10
      })
    }, 200)

    try {
      const formData = new FormData()
      formData.append('video', selectedFile)
      formData.append('angle', selectedAngle)

      // APIエンドポイントへの送信（実装時）
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/analyze/video`, {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        setUploadProgress(100)
        setTimeout(() => {
          router.push('/analysis?session=' + Date.now())
        }, 1000)
      } else {
        throw new Error('アップロードに失敗しました')
      }
    } catch (error) {
      console.error('Upload error:', error)
      alert('アップロードに失敗しました。もう一度お試しください。')
    } finally {
      setIsUploading(false)
      clearInterval(progressInterval)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDuration = (file: File) => {
    // 実際の実装では動画の長さを取得
    return '約15秒' // プレースホルダー
  }

  return (
    <>
      {/* ヘッダー */}
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <IconButton 
            edge="start" 
            color="inherit" 
            onClick={() => router.back()}
            sx={{ mr: 2 }}
          >
            <ArrowBack />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            動画をアップロード
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ py: 4 }}>
        {/* 動画要件の説明 */}
        <MotionCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          sx={{ mb: 4, background: 'linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%)' }}
        >
          <CardContent>
            <Typography 
              variant="h6" 
              component="h2" 
              sx={{ 
                mb: 2, 
                color: '#2E7D32',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: 1,
              }}
            >
              📹 動画の要件
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Chip label="長さ" size="small" sx={{ mr: 1, minWidth: 60 }} />
                  <Typography variant="body2">10〜30秒</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Chip label="形式" size="small" sx={{ mr: 1, minWidth: 60 }} />
                  <Typography variant="body2">MP4, MOV, AVI</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Chip label="角度" size="small" sx={{ mr: 1, minWidth: 60 }} />
                  <Typography variant="body2">正面または側面</Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  <Chip label="照明" size="small" sx={{ mr: 1, minWidth: 60 }} />
                  <Typography variant="body2">明るい場所で撮影</Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </MotionCard>

        {/* ドラッグ&ドロップエリア */}
        <MotionCard
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          sx={{ mb: 4 }}
        >
          <CardContent>
            <Box
              {...getRootProps()}
              sx={{
                border: '2px dashed',
                borderColor: isDragActive ? 'primary.main' : 'grey.300',
                borderRadius: 2,
                p: 6,
                textAlign: 'center',
                cursor: 'pointer',
                backgroundColor: isDragActive ? 'action.hover' : 'transparent',
                transition: 'all 0.3s ease',
                '&:hover': {
                  borderColor: 'primary.main',
                  backgroundColor: 'action.hover',
                },
              }}
            >
              <input {...getInputProps()} />
              <CloudUpload sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" sx={{ mb: 1 }}>
                {isDragActive ? 
                  '動画ファイルをここにドロップ' : 
                  '動画ファイルをドラッグ&ドロップ'
                }
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                または
              </Typography>
              <Button variant="outlined" color="primary">
                ファイルを選択
              </Button>
            </Box>
          </CardContent>
        </MotionCard>

        {/* 選択されたファイル情報 */}
        {selectedFile && (
          <MotionCard
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3 }}
            sx={{ mb: 4, background: 'linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%)' }}
          >
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <CheckCircle sx={{ color: '#1565C0', mr: 2 }} />
                <Typography variant="h6" sx={{ color: '#1565C0', fontWeight: 600 }}>
                  動画が選択されました
                </Typography>
              </Box>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    <strong>ファイル名:</strong> {selectedFile.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    <strong>サイズ:</strong> {formatFileSize(selectedFile.size)}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    <strong>形式:</strong> {selectedFile.type}
                  </Typography>
                  {selectedAngle && (
                    <Typography variant="body2" color="text.secondary">
                      <strong>撮影角度:</strong> {selectedAngle}
                    </Typography>
                  )}
                </Grid>
              </Grid>
            </CardContent>
          </MotionCard>
        )}

        {/* アップロード進捗 */}
        {isUploading && (
          <MotionCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            sx={{ mb: 4 }}
          >
            <CardContent>
              <Typography variant="h6" sx={{ mb: 2 }}>
                動画を解析中...
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={uploadProgress} 
                sx={{ mb: 1, height: 8, borderRadius: 4 }}
              />
              <Typography variant="body2" color="text.secondary">
                {uploadProgress}% 完了
              </Typography>
            </CardContent>
          </MotionCard>
        )}

        {/* アップロードボタン */}
        <Button
          variant="contained"
          size="large"
          fullWidth
          onClick={handleUpload}
          disabled={!selectedFile || !selectedAngle || isUploading}
          sx={{
            py: 2,
            fontSize: '1.1rem',
            background: selectedFile && selectedAngle ? 
              'linear-gradient(45deg, #4CAF50 30%, #66BB6A 90%)' : 
              undefined,
          }}
          startIcon={<VideoFile />}
        >
          {isUploading ? '解析中...' : 'フォーム解析を開始'}
        </Button>

        {/* 注意事項 */}
        <Alert severity="info" sx={{ mt: 3 }}>
          <Typography variant="body2">
            <strong>解析のコツ:</strong> 明るい場所で、プレイヤー全体が映るように撮影してください。
            側面からの動画はスイング軌道、正面からの動画はスタンスの分析に適しています。
          </Typography>
        </Alert>
      </Container>

      {/* アングル選択ダイアログ */}
      <Dialog 
        open={showAngleDialog} 
        onClose={() => setShowAngleDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Typography variant="h6" fontWeight={600}>
            撮影アングルを選択
          </Typography>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <Card 
                sx={{ 
                  cursor: 'pointer',
                  '&:hover': { bgcolor: 'action.hover' }
                }}
                onClick={() => handleAngleSelect('正面')}
              >
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" sx={{ mb: 1 }}>👤</Typography>
                  <Typography variant="h6" fontWeight={600}>正面</Typography>
                  <Typography variant="body2" color="text.secondary">
                    体の向きや足の位置を分析
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Card 
                sx={{ 
                  cursor: 'pointer',
                  '&:hover': { bgcolor: 'action.hover' }
                }}
                onClick={() => handleAngleSelect('側面')}
              >
                <CardContent sx={{ textAlign: 'center' }}>
                  <Typography variant="h3" sx={{ mb: 1 }}>📐</Typography>
                  <Typography variant="h6" fontWeight={600}>側面</Typography>
                  <Typography variant="body2" color="text.secondary">
                    スイング軌道や体重移動を分析
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAngleDialog(false)}>
            キャンセル
          </Button>
        </DialogActions>
      </Dialog>
    </>
  )
}