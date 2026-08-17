package com.arab.encyclopedia.ui.theme

import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF15803D),
    onPrimary = Color.White,
    primaryContainer = Color(0xFFDCFCE7),
    secondary = Color(0xFF4D6357),
    background = Color(0xFFFFFEFB),
    surface = Color.White,
    error = Color(0xFFBA1A1A)
)

@Composable
fun ArabEncyclopediaTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = LightColorScheme,
        typography = Typography(),
        content = content
    )
}
