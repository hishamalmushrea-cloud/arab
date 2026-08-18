package com.atlasalarab.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import com.atlasalarab.app.R

val AtlasNavy = Color(0xFF12343B)
val AtlasEmerald = Color(0xFF087F70)
val AtlasEmeraldDark = Color(0xFF055E54)
val AtlasGold = Color(0xFFC99A3D)
val AtlasSand = Color(0xFFF6F2E8)
val AtlasIvory = Color(0xFFFFFDF8)
val AtlasInk = Color(0xFF172B30)
val AtlasMuted = Color(0xFF607277)

val NotoSansArabicFamily = FontFamily(
    Font(R.font.noto_sans_arabic, FontWeight.Normal),
    Font(R.font.noto_sans_arabic, FontWeight.Medium),
    Font(R.font.noto_sans_arabic, FontWeight.SemiBold),
    Font(R.font.noto_sans_arabic, FontWeight.Bold),
)

val NotoKufiArabicFamily = FontFamily(
    Font(R.font.noto_kufi_arabic, FontWeight.Medium),
    Font(R.font.noto_kufi_arabic, FontWeight.SemiBold),
    Font(R.font.noto_kufi_arabic, FontWeight.Bold),
)

private val LightColors = lightColorScheme(
    primary = AtlasEmerald,
    onPrimary = Color.White,
    primaryContainer = Color(0xFFD9F1EB),
    onPrimaryContainer = Color(0xFF073E38),
    secondary = AtlasGold,
    onSecondary = Color(0xFF322400),
    secondaryContainer = Color(0xFFFFEBC0),
    onSecondaryContainer = Color(0xFF4A3600),
    tertiary = Color(0xFF426B88),
    onTertiary = Color.White,
    tertiaryContainer = Color(0xFFD2E7F8),
    onTertiaryContainer = Color(0xFF16384F),
    background = AtlasSand,
    onBackground = AtlasInk,
    surface = AtlasIvory,
    onSurface = AtlasInk,
    surfaceVariant = Color(0xFFE8EFEC),
    onSurfaceVariant = Color(0xFF435B60),
    outline = Color(0xFF71868A),
    outlineVariant = Color(0xFFCCD8D5),
    error = Color(0xFFBA1A1A),
    errorContainer = Color(0xFFFFDAD6),
)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF72D8C6),
    onPrimary = Color(0xFF003730),
    primaryContainer = Color(0xFF005047),
    onPrimaryContainer = Color(0xFF91F5E1),
    secondary = Color(0xFFE8C476),
    onSecondary = Color(0xFF3D2E00),
    secondaryContainer = Color(0xFF584500),
    onSecondaryContainer = Color(0xFFFFE49A),
    tertiary = Color(0xFF9CCCF0),
    onTertiary = Color(0xFF00344F),
    tertiaryContainer = Color(0xFF244D68),
    onTertiaryContainer = Color(0xFFCDE8FF),
    background = Color(0xFF091C21),
    onBackground = Color(0xFFDCE5E4),
    surface = Color(0xFF10272C),
    onSurface = Color(0xFFDCE5E4),
    surfaceVariant = Color(0xFF334B50),
    onSurfaceVariant = Color(0xFFBBCAC9),
    outline = Color(0xFF849795),
    outlineVariant = Color(0xFF3E5458),
    errorContainer = Color(0xFF8C1D18),
)

private val AtlasTypography = Typography(
    displaySmall = TextStyle(
        fontFamily = NotoKufiArabicFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 32.sp,
        lineHeight = 47.sp,
    ),
    headlineLarge = TextStyle(
        fontFamily = NotoKufiArabicFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 29.sp,
        lineHeight = 43.sp,
    ),
    headlineMedium = TextStyle(
        fontFamily = NotoKufiArabicFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 25.sp,
        lineHeight = 39.sp,
    ),
    headlineSmall = TextStyle(
        fontFamily = NotoKufiArabicFamily,
        fontWeight = FontWeight.SemiBold,
        fontSize = 22.sp,
        lineHeight = 34.sp,
    ),
    titleLarge = TextStyle(
        fontFamily = NotoKufiArabicFamily,
        fontWeight = FontWeight.SemiBold,
        fontSize = 20.sp,
        lineHeight = 32.sp,
    ),
    titleMedium = TextStyle(
        fontFamily = NotoSansArabicFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 17.sp,
        lineHeight = 28.sp,
    ),
    titleSmall = TextStyle(
        fontFamily = NotoSansArabicFamily,
        fontWeight = FontWeight.SemiBold,
        fontSize = 15.sp,
        lineHeight = 24.sp,
    ),
    bodyLarge = TextStyle(
        fontFamily = NotoSansArabicFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 16.5f.sp,
        lineHeight = 29.sp,
    ),
    bodyMedium = TextStyle(
        fontFamily = NotoSansArabicFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 14.5f.sp,
        lineHeight = 24.sp,
    ),
    bodySmall = TextStyle(
        fontFamily = NotoSansArabicFamily,
        fontWeight = FontWeight.Normal,
        fontSize = 12.5f.sp,
        lineHeight = 20.sp,
    ),
    labelLarge = TextStyle(
        fontFamily = NotoSansArabicFamily,
        fontWeight = FontWeight.Bold,
        fontSize = 14.sp,
        lineHeight = 21.sp,
    ),
    labelMedium = TextStyle(
        fontFamily = NotoSansArabicFamily,
        fontWeight = FontWeight.SemiBold,
        fontSize = 12.5f.sp,
        lineHeight = 19.sp,
    ),
    labelSmall = TextStyle(
        fontFamily = NotoSansArabicFamily,
        fontWeight = FontWeight.Medium,
        fontSize = 11.sp,
        lineHeight = 17.sp,
    ),
)

@Composable
fun AtlasTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = if (isSystemInDarkTheme()) DarkColors else LightColors,
        typography = AtlasTypography,
        content = content,
    )
}
