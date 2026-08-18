package com.atlasalarab.app.ui.screens

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.OpenInNew
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.produceState
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.SourceItem
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.ErrorPane
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.LoadingPane
import com.atlasalarab.app.ui.components.SectionTitle

@Composable
fun SourceDetailScreen(id: String, repository: AtlasRepository, modifier: Modifier = Modifier) {
    val state = produceState<LoadState<SourceItem?>>(LoadState.Loading, id, repository) {
        value = try { LoadState.Ready(repository.source(id)) }
        catch (error: Exception) { LoadState.Failed(error.message ?: "خطأ غير معروف") }
    }.value
    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> state.value?.let { SourceContent(it, modifier) } ?: ErrorPane("لم نجد المصدر المطلوب", modifier)
    }
}

@Composable
private fun SourceContent(source: SourceItem, modifier: Modifier) {
    val context = LocalContext.current
    LazyColumn(
        modifier = modifier,
        contentPadding = PaddingValues(18.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Card(shape = RoundedCornerShape(26.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)) {
                Column(Modifier.fillMaxWidth().padding(22.dp)) {
                    Surface(shape = RoundedCornerShape(12.dp), color = MaterialTheme.colorScheme.surface) {
                        Text(source.qualityTier, Modifier.padding(horizontal = 13.dp, vertical = 7.dp), style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    }
                    Spacer(Modifier.height(15.dp))
                    Text(source.title, style = MaterialTheme.typography.headlineMedium)
                    Spacer(Modifier.height(8.dp))
                    Text(source.publisher, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
                }
            }
        }
        item {
            Button(
                onClick = { context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(source.url))) },
                modifier = Modifier.fillMaxWidth(),
            ) {
                Icon(Icons.Default.OpenInNew, null)
                Spacer(Modifier.width(8.dp))
                Text("فتح المصدر الأصلي")
            }
        }
        item { SectionTitle("بيانات المصدر") }
        item {
            Card(shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                Column(Modifier.padding(17.dp), verticalArrangement = Arrangement.spacedBy(11.dp)) {
                    SourceLine("مستوى الجودة", ArabicLabels.sourceTier(source.qualityTier))
                    SourceLine("نوع المصدر", ArabicLabels.sourceType(source.sourceType))
                    SourceLine("اللغة", source.language)
                    source.publicationDate?.let { SourceLine("تاريخ النشر", it) }
                    SourceLine("تاريخ الاسترجاع", source.retrievedAt)
                    source.organization?.let { SourceLine("المنظمة", it) }
                    source.author?.let { SourceLine("المؤلف", it) }
                    SourceLine("المحدد داخل المصدر", source.locator)
                }
            }
        }
        item { SectionTitle("الترخيص والاستخدام") }
        item {
            Card(shape = RoundedCornerShape(18.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
                Column(Modifier.padding(17.dp)) {
                    Row {
                        Icon(Icons.Default.Language, null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(Modifier.width(9.dp))
                        Text(source.license, style = MaterialTheme.typography.bodyLarge)
                    }
                    source.notes?.let {
                        Spacer(Modifier.height(12.dp))
                        Text(it, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
        item {
            SelectionContainer {
                Text(source.id, fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.outline)
            }
        }
    }
}

@Composable
private fun SourceLine(label: String, value: String) {
    Column {
        Text(label, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
        Text(value, style = MaterialTheme.typography.bodyLarge)
    }
}
