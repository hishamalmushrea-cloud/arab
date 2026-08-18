package com.atlasalarab.app.ui.screens

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
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AutoStories
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.LocalLibrary
import androidx.compose.material.icons.filled.Public
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.produceState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.CountrySummary
import com.atlasalarab.app.data.ProjectStats
import com.atlasalarab.app.data.ReadingItem
import com.atlasalarab.app.data.ReadingStore
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.CountryCard
import com.atlasalarab.app.ui.components.ErrorPane
import com.atlasalarab.app.ui.components.LibraryDocumentRow
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.LoadingPane
import com.atlasalarab.app.ui.components.NoticeCard
import com.atlasalarab.app.ui.components.SectionTitle
import com.atlasalarab.app.ui.components.StatCard
import com.atlasalarab.app.ui.theme.AtlasGold
import com.atlasalarab.app.ui.theme.AtlasNavy

@Composable
fun HomeScreen(
    repository: AtlasRepository,
    readingStore: ReadingStore,
    onContinueReading: (String) -> Unit,
    onOpenSearch: () -> Unit,
    onOpenCountries: () -> Unit,
    onOpenLibrary: () -> Unit,
    onOpenCountry: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    val recent by readingStore.recent.collectAsStateWithLifecycle()
    val state = produceState<LoadState<Pair<ProjectStats, List<CountrySummary>>>>(LoadState.Loading, repository) {
        value = try {
            LoadState.Ready(repository.projectStats() to repository.countries())
        } catch (error: Exception) {
            LoadState.Failed(error.message ?: "خطأ غير معروف")
        }
    }.value

    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> HomeContent(
            stats = state.value.first,
            countries = state.value.second,
            lastRead = recent.firstOrNull(),
            onContinueReading = onContinueReading,
            onOpenSearch = onOpenSearch,
            onOpenCountries = onOpenCountries,
            onOpenLibrary = onOpenLibrary,
            onOpenCountry = onOpenCountry,
            modifier = modifier,
        )
    }
}

@Composable
private fun HomeContent(
    stats: ProjectStats,
    countries: List<CountrySummary>,
    lastRead: ReadingItem?,
    onContinueReading: (String) -> Unit,
    onOpenSearch: () -> Unit,
    onOpenCountries: () -> Unit,
    onOpenLibrary: () -> Unit,
    onOpenCountry: (String) -> Unit,
    modifier: Modifier,
) {
    LazyColumn(
        modifier = modifier,
        contentPadding = PaddingValues(start = 18.dp, end = 18.dp, top = 16.dp, bottom = 28.dp),
        verticalArrangement = Arrangement.spacedBy(20.dp),
    ) {
        item {
            Card(
                shape = RoundedCornerShape(28.dp),
                colors = CardDefaults.cardColors(containerColor = AtlasNavy),
            ) {
                Column(Modifier.padding(23.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.AutoStories, null, tint = AtlasGold)
                        Spacer(Modifier.width(9.dp))
                        Text("موسوعة جغرافية عربية موثّقة", color = MaterialTheme.colorScheme.inverseOnSurface, style = MaterialTheme.typography.labelLarge)
                    }
                    Spacer(Modifier.height(18.dp))
                    Text("اكتشف العالم العربي\nمن المصدر إلى المكان", style = MaterialTheme.typography.displaySmall, color = MaterialTheme.colorScheme.inverseOnSurface)
                    Spacer(Modifier.height(10.dp))
                    Text(
                        "ابحث في الدول والتقسيمات الإدارية والأماكن والمواقع الثقافية، مع مصدر كل معلومة وحدود تغطيتها.",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.inverseOnSurface.copy(alpha = .8f),
                    )
                    Spacer(Modifier.height(20.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        Button(onClick = onOpenSearch) {
                            Icon(Icons.Default.Search, null)
                            Spacer(Modifier.width(7.dp))
                            Text("ابدأ البحث")
                        }
                        OutlinedButton(onClick = onOpenCountries) {
                            Icon(Icons.Default.Public, null)
                            Spacer(Modifier.width(7.dp))
                            Text("الدول")
                        }
                    }
                    Spacer(Modifier.height(10.dp))
                    OutlinedButton(onClick = onOpenLibrary, modifier = Modifier.fillMaxWidth()) {
                        Icon(Icons.Default.LocalLibrary, null)
                        Spacer(Modifier.width(7.dp))
                        Text("تصفّح المكتبة الموسوعية الكاملة")
                    }
                }
            }
        }

        item { NoticeCard(stats.notice) }

        if (lastRead != null) {
            item {
                SectionTitle("تابع القراءة", "ارجع مباشرة إلى آخر ملف فتحته")
            }
            item {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.History, null, tint = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(8.dp))
                    Text("حُفظ موضعك تلقائيًا", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                }
            }
            item {
                LibraryDocumentRow(lastRead.asSummary(), onClick = { onContinueReading(lastRead.id) })
            }
        }

        item { SectionTitle("المشروع في أرقام", "بيانات Schema ${stats.schemaVersion} المتاحة كاملة داخل التطبيق") }

        item {
            Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    StatCard("دولة عربية", ArabicLabels.number(stats.countries), Modifier.weight(1f))
                    StatCard("كيان موثّق", ArabicLabels.number(stats.entities), Modifier.weight(1f), AtlasGold)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    StatCard("ادعاء موثّق", ArabicLabels.number(stats.claims), Modifier.weight(1f))
                    StatCard("مصدر ذري", ArabicLabels.number(stats.sources), Modifier.weight(1f), AtlasGold)
                }
                StatCard(
                    "ملف موسوعي كامل • ${ArabicLabels.fileSize(stats.libraryBytes)}",
                    ArabicLabels.number(stats.libraryDocuments),
                    Modifier.fillMaxWidth(),
                )
            }
        }

        item { SectionTitle("استكشف الدول", "الدول الأعلى من حيث عدد السجلات المنظمة") }

        item {
            LazyRow(
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                contentPadding = PaddingValues(vertical = 2.dp),
            ) {
                items(countries.sortedByDescending { it.entityCount }.take(8), key = { it.code }) { country ->
                    CountryCard(country, onClick = { onOpenCountry(country.code) }, modifier = Modifier.width(245.dp))
                }
            }
        }

        item {
            OutlinedButton(onClick = onOpenCountries, modifier = Modifier.fillMaxWidth()) {
                Text("عرض جميع الدول الـ${ArabicLabels.number(stats.countries)}", fontWeight = FontWeight.SemiBold)
            }
        }

        item {
            Text(
                "نسخة البيانات: ${stats.datasetVersion} • آخر لقطة: ${stats.asOf}",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.fillMaxWidth().padding(top = 4.dp),
            )
        }
    }
}
