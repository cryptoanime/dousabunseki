package com.softtennis.aicoach

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import androidx.navigation.NavHostController
import com.softtennis.aicoach.ui.theme.SoftTennisAITheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VideoUploadScreen(navController: NavHostController) {
    var selectedVideoUri by remember { mutableStateOf<Uri?>(null) }
    var selectedAngle by remember { mutableStateOf<String?>(null) }
    var isUploading by remember { mutableStateOf(false) }
    var showAngleDialog by remember { mutableStateOf(false) }
    
    val context = LocalContext.current
    
    // 動画選択用のランチャー
    val videoPickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            selectedVideoUri = uri
            showAngleDialog = true
        }
    }
    
    // カメラ撮影用のランチャー
    val cameraLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        // カメラ結果の処理（実装予定）
    }
    
    // 権限リクエスト用のランチャー
    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        if (isGranted) {
            videoPickerLauncher.launch("video/*")
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        // タイトル
        Text(
            "動画をアップロード",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(bottom = 8.dp)
        )
        
        // 説明
        Card(
            colors = CardDefaults.cardColors(containerColor = Color(0xFFE8F5E8))
        ) {
            Column(
                modifier = Modifier.padding(16.dp)
            ) {
                Text(
                    "📹 動画の要件",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF2E7D32)
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text("• 長さ: 10〜30秒", fontSize = 14.sp)
                Text("• フォーマット: MP4, MOV", fontSize = 14.sp)
                Text("• アングル: 正面または側面", fontSize = 14.sp)
                Text("• 照明: 明るい場所で撮影", fontSize = 14.sp)
            }
        }

        // 動画選択ボタン
        VideoSelectionCard(
            title = "ギャラリーから選択",
            subtitle = "既存の動画をアップロード",
            icon = Icons.Default.VideoLibrary,
            onClick = {
                when (PackageManager.PERMISSION_GRANTED) {
                    ContextCompat.checkSelfPermission(
                        context,
                        Manifest.permission.READ_EXTERNAL_STORAGE
                    ) -> {
                        videoPickerLauncher.launch("video/*")
                    }
                    else -> {
                        permissionLauncher.launch(Manifest.permission.READ_EXTERNAL_STORAGE)
                    }
                }
            }
        )

        VideoSelectionCard(
            title = "新しく撮影",
            subtitle = "カメラで新しい動画を撮影",
            icon = Icons.Default.Videocam,
            onClick = {
                // カメラ撮影の実装（後で追加）
            }
        )

        // 選択した動画の情報表示
        selectedVideoUri?.let { uri ->
            Card(
                colors = CardDefaults.cardColors(containerColor = Color(0xFFE3F2FD))
            ) {
                Column(
                    modifier = Modifier.padding(16.dp)
                ) {
                    Text(
                        "✅ 動画が選択されました",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF1565C0)
                    )
                    Text(
                        "URI: ${uri.lastPathSegment}",
                        fontSize = 12.sp,
                        color = Color.Gray
                    )
                    selectedAngle?.let { angle ->
                        Text(
                            "アングル: $angle",
                            fontSize = 14.sp,
                            color = Color(0xFF1565C0)
                        )
                    }
                }
            }
        }

        Spacer(modifier = Modifier.weight(1f))

        // アップロードボタン
        Button(
            onClick = {
                selectedVideoUri?.let { uri ->
                    selectedAngle?.let { angle ->
                        isUploading = true
                        // TODO: 実際のアップロード処理
                        // uploadVideoForAnalysis(uri, angle)
                    }
                }
            },
            enabled = selectedVideoUri != null && selectedAngle != null && !isUploading,
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = Color(0xFF4CAF50)
            )
        ) {
            if (isUploading) {
                CircularProgressIndicator(
                    color = Color.White,
                    modifier = Modifier.size(20.dp)
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text("解析中...")
            } else {
                Icon(Icons.Default.CloudUpload, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("フォーム解析を開始", fontSize = 16.sp)
            }
        }
    }

    // アングル選択ダイアログ
    if (showAngleDialog) {
        AngleSelectionDialog(
            onAngleSelected = { angle ->
                selectedAngle = angle
                showAngleDialog = false
            },
            onDismiss = {
                showAngleDialog = false
                selectedVideoUri = null
            }
        )
    }
}

@Composable
fun VideoSelectionCard(
    title: String,
    subtitle: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(80.dp)
            .clickable { onClick() },
        colors = CardDefaults.cardColors(containerColor = Color(0xFFFFF3E0)),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                imageVector = icon,
                contentDescription = title,
                tint = Color(0xFFE65100),
                modifier = Modifier.size(32.dp)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    title,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFFE65100)
                )
                Text(
                    subtitle,
                    fontSize = 14.sp,
                    color = Color.Gray
                )
            }
        }
    }
}

@Composable
fun AngleSelectionDialog(
    onAngleSelected: (String) -> Unit,
    onDismiss: () -> Unit
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = {
            Text(
                "撮影アングルを選択",
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )
        },
        text = {
            Column(
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                AngleOptionCard(
                    title = "正面",
                    description = "体の向きや足の位置を分析",
                    emoji = "👤",
                    onClick = { onAngleSelected("正面") }
                )
                
                AngleOptionCard(
                    title = "側面",
                    description = "スイング軌道や体重移動を分析",
                    emoji = "📐",
                    onClick = { onAngleSelected("側面") }
                )
            }
        },
        confirmButton = {},
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("キャンセル")
            }
        }
    )
}

@Composable
fun AngleOptionCard(
    title: String,
    description: String,
    emoji: String,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        colors = CardDefaults.cardColors(containerColor = Color(0xFFF5F5F5))
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                emoji,
                fontSize = 24.sp,
                modifier = Modifier.size(32.dp),
                textAlign = TextAlign.Center
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(
                    title,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    description,
                    fontSize = 12.sp,
                    color = Color.Gray
                )
            }
        }
    }
}