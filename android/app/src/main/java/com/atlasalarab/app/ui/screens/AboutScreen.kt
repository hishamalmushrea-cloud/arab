package com.atlasalarab.app.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CloudOff
import androidx.compose.material.icons.filled.DataObject
import androidx.compose.material.icons.filled.TextFields
import androidx.compose.material.icons.filled.Verified
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.produceState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.ProjectStats
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.ErrorPane
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.LoadingPane
import com.atlasalarab.app.ui.components.NoticeCard
import com.atlasalarab.app.ui.components.SectionTitle
import com.atlasalarab.app.ui.components.StatCard

@Composable
fun AboutScreen(repository: AtlasRepository, modifier: Modifier = Modifier) {
    val state = produceState<LoadState<ProjectStats>>(LoadState.Loading, repository) {
        value = try { LoadState.Ready(repository.projectStats()) }
        catch (error: Exception) { LoadState.Failed(error.message ?: "خطأ غير معروف") }
    }.value
    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> AboutContent(state.value, modifier)
    }
}

@Composable
private fun AboutContent(stats: ProjectStats, modifier: Modifier) {
    LazyColumn(
        modifier = modifier,
        contentPadding = PaddingValues(18.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        item { SectionTitle("عن أطلس العرب", "تطبيق عربي لاستكشاف البيانات الجغرافية والثقافية الموثقة") }
        item {
            Card(shape = RoundedCornerShape(24.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)) {
                Column(Modifier.padding(21.dp)) {
                    Text("البيانات قبل الزينة", style = MaterialTheme.typography.headlineMedium)
                    Spacer(Modifier.height(8.dp))
                    Text(
                        "يعرض التطبيق المصدر والحالة الزمنية وحدود التغطية مع كل سجل. لا يملأ الفراغات بالتخمين، ولا يحوّل العينة المحدودة إلى ادعاء وطني.",
                        style = MaterialTheme.typography.bodyLarge,
                    )
                }
            }
        }
        item { NoticeCard(stats.notice) }
        item { SectionTitle("قاعدة البيانات الكاملة") }
        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    StatCard("كيانات", ArabicLabels.number(stats.entities), Modifier.weight(1f))
                    StatCard("أسماء بديلة", ArabicLabels.number(stats.aliases), Modifier.weight(1f))
                }
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    StatCard("علاقات", ArabicLabels.number(stats.relationships), Modifier.weight(1f))
                    StatCard("لقطات", ArabicLabels.number(stats.snapshots), Modifier.weight(1f))
                }
                StatCard(
                    "ملفات الموسوعة المرجعية • ${ArabicLabels.fileSize(stats.libraryBytes)}",
                    ArabicLabels.number(stats.libraryDocuments),
                    Modifier.fillMaxWidth(),
                )
            }
        }
        item { SectionTitle("مزايا النسخة") }
        item { FeatureCard(Icons.Default.CloudOff, "يعمل دون إنترنت", "كل البيانات السلطوية والمصادر والفهارس مضمنة في التطبيق.") }
        item { FeatureCard(Icons.Default.Verified, "مصدر لكل معلومة", "يمكن فتح المصدر وقراءة الترخيص والمحدد داخل الوثيقة.") }
        item { FeatureCard(Icons.Default.TextFields, "خط عربي مخصص", "Noto Kufi Arabic للعناوين وNoto Sans Arabic للقراءة، ويعملان دون إنترنت بترخيص OFL 1.1.") }
        item { FeatureCard(Icons.Default.DataObject, "Schema ${stats.schemaVersion}", "تُولّد قاعدة التطبيق آليًا من البيانات المنظمة وتُفحص قبل الإصدار.") }
        item {
            Text(
                "نسخة البيانات ${stats.datasetVersion}\nتاريخ البيانات ${stats.asOf}\nسجلات التغطية ${ArabicLabels.number(stats.coverageRecords)}",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.fillMaxWidth().padding(top = 6.dp),
            )
        }
    }
}

@Composable
private fun FeatureCard(icon: androidx.compose.ui.graphics.vector.ImageVector, title: String, body: String) {
    Card(shape = RoundedCornerShape(17.dp), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)) {
        Row(Modifier.fillMaxWidth().padding(17.dp), verticalAlignment = Alignment.Top) {
            Icon(icon, null, tint = MaterialTheme.colorScheme.primary)
            Column(Modifier.padding(start = 12.dp)) {
                Text(title, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                Text(body, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}
