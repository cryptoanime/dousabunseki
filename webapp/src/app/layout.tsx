'use client'

import React from 'react'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Box } from '@mui/material'

// 軟式テニス専用テーマ
const softTennisTheme = createTheme({
  palette: {
    primary: {
      main: '#1565C0',      // テニスブルー
      light: '#E3F2FD',
      dark: '#0D47A1',
    },
    secondary: {
      main: '#4CAF50',      // テニスグリーン
      light: '#E8F5E8',
      dark: '#1B5E20',
    },
    warning: {
      main: '#FF9800',      // エネルギッシュオレンジ
    },
    background: {
      default: '#FAFAFA',
      paper: '#FFFFFF',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
    h1: {
      fontWeight: 700,
      fontSize: '2.5rem',
    },
    h2: {
      fontWeight: 600,
      fontSize: '2rem',
    },
    h3: {
      fontWeight: 600,
      fontSize: '1.75rem',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          textTransform: 'none',
          fontWeight: 600,
          padding: '12px 24px',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
        },
      },
    },
  },
})

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5分
      cacheTime: 10 * 60 * 1000, // 10分
    },
  },
})

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ja">
      <head>
        <title>🎾 SoftTennis AI Coach</title>
        <meta name="description" content="軟式テニス専用AI動作分析アプリ - 初心者向けフォーム改善とトレーニングメニュー生成" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body>
        <QueryClientProvider client={queryClient}>
          <ThemeProvider theme={softTennisTheme}>
            <CssBaseline />
            <Box
              sx={{
                minHeight: '100vh',
                backgroundColor: 'background.default',
              }}
            >
              {children}
            </Box>
          </ThemeProvider>
        </QueryClientProvider>
      </body>
    </html>
  )
}