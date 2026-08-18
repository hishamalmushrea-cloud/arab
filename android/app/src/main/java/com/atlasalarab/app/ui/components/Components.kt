package com.atlasalarab.app.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Article
import androidx.compose.material.icons.filled.AutoStories
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Science
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.TableChart
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material.icons.filled.WarningAmber
import androidx.compose.material3.AssistChip
import androidx.compose.material3.AssistChipDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.clearAndSetSemantics
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.atlasalarab.app.data.CountrySummary
import com.atlasalarab.app.data.EntitySummary
import com.atlasalarab.app.data.LibraryDocumentSummary
import com.atlasalarab.app.data.SourceItem
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.theme.AtlasGold

sealed interface LoadState<out T> {
    data object Loading : LoadState<Nothing>
    data class Ready<T>(val value: T) : LoadState<T>
    data class Failed(val message: String) : LoadState<Nothing>
}

enum class ContentKind(val label: String, val description: String) {
    Authoritative("موثّق سلطويًا", "بيانات منظمة ومراجعة مرتبطة بمصدر"),
    Encyclopedic("مادة موسوعية", "مادة مرجعية من ملفات الموسوعة وقد تتضمن فجوات أو تقديرات"),
    Historical("بيانات تاريخية", "معلومة مرتبطة بفترة تاريخية وليست وصفًا للوضع الحالي"),
    Partial("تغطية جزئية", "البيانات المتاحة لا تمثل الطبقة كاملة"),
    Pilot("نطاق تجريبي", "عينة محدودة لا تمثل تغطية وطنية كاملة"),
}

@Composable
fun ContentBadge(kind: ContentKind, modifier: Modifier = Modifier, compact: Boolean = false) {
    val colors = when (kind) {
        ContentKind.Authoritative -> MaterialTheme.colorScheme.primaryContainer to MaterialTheme.colorScheme.onPrimaryContainer
        ContentKind.Encyclopedic -> MaterialTheme.colorScheme.secondaryContainer to MaterialTheme.colorScheme.onSecondaryContainer
        ContentKind.Historical -> MaterialTheme.colorScheme.tertiaryContainer to MaterialTheme.colorScheme.onTertiaryContainer
        ContentKind.Partial -> MaterialTheme.colorScheme.errorContainer to MaterialTheme.colorScheme.onErrorContainer
        ContentKind.Pilot -> MaterialTheme.colorScheme.surfaceVariant to MaterialTheme.colorScheme.onSurfaceVariant
    }
    val icon = when (kind) {
        ContentKind.Authoritative -> Icons.Default.Verified
        ContentKind.Encyclopedic -> Icons.Default.AutoStories
        ContentKind.Historical -> Icons.Default.History
        ContentKind.Partial -> Icons.Default.WarningAmber
        ContentKind.Pilot -> Icons.Default.Science
    }
    Surface(
        modifier = modifier.clearAndSetSemantics {
            contentDescription = "${kind.label}. ${kind.description}"
        },
        shape = RoundedCornerShape(9.dp),
        color = colors.first,
    ) {
        Row(
            Modifier.padding(horizontal = if (compact) 7.dp else 10.dp, vertical = if (compact) 3.dp else 5.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Icon(icon, contentDescription = null, modifier = Modifier.size(if (compact) 14.dp else 17.dp), tint = colors.second)
            Spacer(Modifier.width(5.dp))
            Text(kind.label, style = if (compact) MaterialTheme.typography.labelSmall else MaterialTheme.typography.labelMedium, color = colors.second)
        }
    }
}

@Composable
fun LoadingPane(modifier: Modifier = Modifier) {
    Box(
        modifier.fillMaxSize().semantics { liveRegion = LiveRegionMode.Polite },
        contentAlignment = Alignment.Center,
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            CircularProgressIndicator()
            Spacer(Modifier.height(14.dp))
            Text("نجهّز البيانات المحلية…", color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(
                "قد يستغرق التشغيل الأول لحظات لنسخ المكتبة دون إنترنت",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.outline,
            )
        }
    }
}

@Composable
fun ErrorPane(message: String, modifier: Modifier = Modifier) {
    Box(
        modifier.fillMaxSize().semantics { liveRegion = LiveRegionMode.Assertive },
        contentAlignment = Alignment.Center,
    ) {
        Card(colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)) {
            Column(Modifier.padding(20.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                Text("تعذر فتح البيانات", style = MaterialTheme.typography.titleMedium)
                Spacer(Modifier.height(6.dp))
                Text(message, style = MaterialTheme.typography.bodyMedium)
            }
        }
    }
}

@Composable
fun SectionTitle(title: String, subtitle: String? = null, modifier: Modifier = Modifier) {
    Column(modifier.fillMaxWidth().semantics { heading() }) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Box(
                Modifier
                    .size(width = 5.dp, height = 24.dp)
                    .clip(CircleShape)
                    .background(MaterialTheme.colorScheme.primary),
            )
            Spacer(Modifier.width(10.dp))
            Text(title, style = MaterialTheme.typography.titleLarge)
        }
        if (subtitle != null) {
            Spacer(Modifier.height(4.dp))
            Text(subtitle, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
fun StatCard(label: String, value: String, modifier: Modifier = Modifier, accent: Color = MaterialTheme.colorScheme.primary) {
    Card(
        modifier = modifier,
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Column(Modifier.padding(17.dp)) {
            Box(Modifier.size(width = 32.dp, height = 4.dp).clip(CircleShape).background(accent))
            Spacer(Modifier.height(9.dp))
            Text(value, style = MaterialTheme.typography.headlineMedium, color = accent, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(2.dp))
            Text(label, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
fun StatusPill(status: String, modifier: Modifier = Modifier) {
    val historical = status == "historical"
    val proposed = status == "proposed" || status == "claimed"
    val color = when {
        historical -> MaterialTheme.colorScheme.secondaryContainer
        proposed -> MaterialTheme.colorScheme.errorContainer
        else -> MaterialTheme.colorScheme.primaryContainer
    }
    val icon = if (historical) Icons.Default.History else Icons.Default.CheckCircle
    AssistChip(
        modifier = modifier,
        onClick = {},
        enabled = false,
        label = { Text(ArabicLabels.status(status)) },
        leadingIcon = { Icon(icon, null, Modifier.size(16.dp)) },
        colors = AssistChipDefaults.assistChipColors(
            disabledContainerColor = color,
            disabledLabelColor = MaterialTheme.colorScheme.onSurface,
            disabledLeadingIconContentColor = MaterialTheme.colorScheme.onSurfaceVariant,
        ),
        border = null,
    )
}

@Composable
fun SearchField(
    value: String,
    onValueChange: (String) -> Unit,
    placeholder: String = "ابحث باسم المكان…",
    modifier: Modifier = Modifier,
) {
    OutlinedTextField(
        value = value,
        onValueChange = onValueChange,
        modifier = modifier.fillMaxWidth(),
        singleLine = true,
        shape = RoundedCornerShape(18.dp),
        label = { Text("بحث") },
        placeholder = { Text(placeholder) },
        leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
        trailingIcon = if (value.isNotEmpty()) {
            { IconButton(onClick = { onValueChange("") }) { Icon(Icons.Default.Clear, "مسح البحث") } }
        } else null,
        colors = OutlinedTextFieldDefaults.colors(
            focusedContainerColor = MaterialTheme.colorScheme.surface,
            unfocusedContainerColor = MaterialTheme.colorScheme.surface,
        ),
    )
}

@Composable
fun EntityRow(entity: EntitySummary, onClick: () -> Unit, modifier: Modifier = Modifier, secondary: String? = null) {
    Card(
        modifier = modifier.fillMaxWidth(),
        onClick = onClick,
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Row(
            Modifier.padding(horizontal = 16.dp, vertical = 14.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Surface(
                shape = RoundedCornerShape(12.dp),
                color = MaterialTheme.colorScheme.primaryContainer,
                modifier = Modifier.size(46.dp),
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Text(entity.name.take(1), style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary)
                }
            }
            Spacer(Modifier.width(13.dp))
            Column(Modifier.weight(1f)) {
                Text(entity.name, style = MaterialTheme.typography.titleMedium, maxLines = 1, overflow = TextOverflow.Ellipsis)
                Text(
                    secondary ?: "${ArabicLabels.entityType(entity.type)} • ${entity.countryName}",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
            Spacer(Modifier.width(8.dp))
            Surface(shape = RoundedCornerShape(8.dp), color = MaterialTheme.colorScheme.surfaceVariant) {
                Text(
                    ArabicLabels.status(entity.status),
                    Modifier.padding(horizontal = 7.dp, vertical = 3.dp),
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Spacer(Modifier.width(6.dp))
            Icon(Icons.Default.ArrowBack, contentDescription = "فتح", tint = MaterialTheme.colorScheme.primary)
        }
    }
}

@Composable
fun CountryCard(country: CountrySummary, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier,
        onClick = onClick,
        shape = RoundedCornerShape(22.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Column(Modifier.padding(18.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(ArabicLabels.flag(country.code), style = MaterialTheme.typography.headlineMedium)
                Spacer(Modifier.weight(1f))
                Text(country.code, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.outline)
            }
            Spacer(Modifier.height(13.dp))
            Text(country.nameAr, style = MaterialTheme.typography.titleLarge)
            Text(
                "${ArabicLabels.number(country.entityCount)} كيان • ${ArabicLabels.number(country.sourceCount)} مصدر",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Spacer(Modifier.height(13.dp))
            val coverageProgress = if (country.coverageCount > 0) country.completeLayers.toFloat() / country.coverageCount else 0f
            LinearProgressIndicator(
                progress = { coverageProgress.coerceIn(0f, 1f) },
                modifier = Modifier.fillMaxWidth().height(6.dp).clip(CircleShape),
                color = MaterialTheme.colorScheme.primary,
                trackColor = MaterialTheme.colorScheme.surfaceVariant,
            )
            Spacer(Modifier.height(8.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.CheckCircle, null, Modifier.size(17.dp), tint = MaterialTheme.colorScheme.primary)
                Spacer(Modifier.width(5.dp))
                Text(
                    "${ArabicLabels.number(country.completeLayers)} طبقات مكتملة من ${ArabicLabels.number(country.coverageCount)}",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.primary,
                    maxLines = 1,
                )
            }
        }
    }
}

@Composable
fun LibraryDocumentRow(document: LibraryDocumentSummary, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.fillMaxWidth(),
        onClick = onClick,
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Surface(
                shape = RoundedCornerShape(14.dp),
                color = if (document.fileType == "csv") MaterialTheme.colorScheme.secondaryContainer else MaterialTheme.colorScheme.primaryContainer,
                modifier = Modifier.size(50.dp),
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Icon(
                        if (document.fileType == "csv") Icons.Default.TableChart else Icons.Default.Article,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.primary,
                    )
                }
            }
            Spacer(Modifier.width(13.dp))
            Column(Modifier.weight(1f)) {
                Text(document.title, style = MaterialTheme.typography.titleMedium, maxLines = 2, overflow = TextOverflow.Ellipsis)
                Spacer(Modifier.height(3.dp))
                Text(
                    buildString {
                        document.countryName?.let { append(it).append("  •  ") }
                        append(document.category)
                    },
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Spacer(Modifier.height(7.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Surface(shape = RoundedCornerShape(7.dp), color = MaterialTheme.colorScheme.surfaceVariant) {
                        Text(
                            if (document.fileType == "csv") "جدول CSV" else "مقال",
                            Modifier.padding(horizontal = 7.dp, vertical = 2.dp),
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                    Text(
                        ArabicLabels.fileSize(document.byteSize.toLong()),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.outline,
                    )
                    ContentBadge(ContentKind.Encyclopedic, compact = true)
                }
            }
            Spacer(Modifier.width(7.dp))
            Icon(Icons.Default.ArrowBack, "فتح الملف", tint = MaterialTheme.colorScheme.primary)
        }
    }
}

@Composable
fun SourceCard(source: SourceItem, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.fillMaxWidth(),
        onClick = onClick,
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Column(Modifier.padding(16.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Surface(shape = CircleShape, color = if (source.qualityTier == "A") MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.secondaryContainer) {
                    Text(source.qualityTier, Modifier.padding(horizontal = 10.dp, vertical = 5.dp), fontWeight = FontWeight.Bold)
                }
                Spacer(Modifier.width(10.dp))
                Text(source.publisher, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary, maxLines = 1, overflow = TextOverflow.Ellipsis)
            }
            Spacer(Modifier.height(9.dp))
            Text(source.title, style = MaterialTheme.typography.titleMedium, maxLines = 2, overflow = TextOverflow.Ellipsis)
            Spacer(Modifier.height(4.dp))
            Text(
                "${ArabicLabels.sourceType(source.sourceType)}  •  ${source.language.uppercase()}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            source.publicationDate?.let {
                Spacer(Modifier.height(5.dp))
                Text("تاريخ النشر: $it", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
fun NoticeCard(text: String, modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier.fillMaxWidth(),
        color = MaterialTheme.colorScheme.primaryContainer,
        shape = RoundedCornerShape(18.dp),
    ) {
        Row(Modifier.padding(16.dp), verticalAlignment = Alignment.Top) {
            Box(Modifier.size(10.dp).clip(CircleShape).background(AtlasGold))
            Spacer(Modifier.width(10.dp))
            Text(text, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onPrimaryContainer)
        }
    }
}

@Composable
fun EmptyState(title: String, message: String, modifier: Modifier = Modifier) {
    Column(
        modifier.fillMaxWidth().padding(vertical = 36.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {
        Icon(Icons.Default.Search, null, Modifier.size(44.dp), tint = MaterialTheme.colorScheme.outline)
        Spacer(Modifier.height(12.dp))
        Text(title, style = MaterialTheme.typography.titleMedium)
        Text(message, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    }
}
