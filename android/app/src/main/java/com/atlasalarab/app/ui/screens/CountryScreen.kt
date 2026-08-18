package com.atlasalarab.app.ui.screens

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.LocalLibrary
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.CountryDetails
import com.atlasalarab.app.data.EntitySummary
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.ContentBadge
import com.atlasalarab.app.ui.components.ContentKind
import com.atlasalarab.app.ui.components.EmptyState
import com.atlasalarab.app.ui.components.EntityRow
import com.atlasalarab.app.ui.components.ErrorPane
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.LoadingPane
import com.atlasalarab.app.ui.components.NoticeCard
import com.atlasalarab.app.ui.components.SearchField
import com.atlasalarab.app.ui.components.SectionTitle
import com.atlasalarab.app.ui.components.SourceCard
import com.atlasalarab.app.ui.components.StatCard
import kotlinx.coroutines.delay

@Composable
fun CountryScreen(
    code: String,
    repository: AtlasRepository,
    onOpenEntity: (String) -> Unit,
    onOpenSource: (String) -> Unit,
    onOpenDocument: (String) -> Unit,
    onOpenLibrary: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    val state = produceState<LoadState<CountryDetails?>>(LoadState.Loading, code, repository) {
        value = try { LoadState.Ready(repository.countryDetails(code)) }
        catch (error: Exception) { LoadState.Failed(error.message ?: "خطأ غير معروف") }
    }.value
    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> state.value?.let {
            CountryContent(it, repository, onOpenEntity, onOpenSource, onOpenDocument, onOpenLibrary, modifier)
        } ?: ErrorPane("لم نجد الدولة المطلوبة", modifier)
    }
}

@Composable
private fun CountryContent(
    details: CountryDetails,
    repository: AtlasRepository,
    onOpenEntity: (String) -> Unit,
    onOpenSource: (String) -> Unit,
    onOpenDocument: (String) -> Unit,
    onOpenLibrary: (String) -> Unit,
    modifier: Modifier,
) {
    var selectedType by remember(details.country.code) { mutableStateOf<String?>(null) }
    var query by remember(details.country.code) { mutableStateOf("") }
    var searchResults by remember(details.country.code) { mutableStateOf<List<EntitySummary>?>(null) }
    var searching by remember { mutableStateOf(false) }

    LaunchedEffect(query, details.country.code) {
        if (query.trim().length < 2) {
            searchResults = null
            searching = false
        } else {
            searching = true
            delay(250)
            searchResults = repository.search(query, details.country.code).map { it.entity }
            searching = false
        }
    }

    val baseEntities = searchResults ?: details.entities
    val shownEntities = remember(baseEntities, selectedType) {
        selectedType?.let { type -> baseEntities.filter { it.type == type } } ?: baseEntities
    }

    LazyColumn(
        modifier = modifier,
        contentPadding = PaddingValues(start = 18.dp, end = 18.dp, top = 16.dp, bottom = 30.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            Card(
                shape = RoundedCornerShape(26.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
            ) {
                Row(Modifier.fillMaxWidth().padding(22.dp), verticalAlignment = Alignment.CenterVertically) {
                    Surface(shape = RoundedCornerShape(20.dp), color = MaterialTheme.colorScheme.surface) {
                        Text(
                            ArabicLabels.flag(details.country.code),
                            style = MaterialTheme.typography.displaySmall,
                            modifier = Modifier.padding(14.dp),
                        )
                    }
                    Spacer(Modifier.width(16.dp))
                    Column(Modifier.weight(1f)) {
                        Text(details.country.nameAr, style = MaterialTheme.typography.headlineMedium)
                        Text(details.country.nameEn, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Spacer(Modifier.height(8.dp))
                        ContentBadge(ContentKind.Authoritative, compact = true)
                        Spacer(Modifier.height(6.dp))
                        Text(
                            "${ArabicLabels.number(details.country.completeLayers)} طبقات مكتملة من ${ArabicLabels.number(details.country.coverageCount)}",
                            style = MaterialTheme.typography.labelLarge,
                            color = MaterialTheme.colorScheme.primary,
                        )
                    }
                }
            }
        }

        item {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                item { StatCard("كيان", ArabicLabels.number(details.country.entityCount), Modifier.width(145.dp)) }
                item { StatCard("ادعاء", ArabicLabels.number(details.country.claimCount), Modifier.width(145.dp)) }
                item { StatCard("اسم بديل", ArabicLabels.number(details.country.aliasCount), Modifier.width(145.dp)) }
                item { StatCard("مصدر", ArabicLabels.number(details.country.sourceCount), Modifier.width(145.dp)) }
            }
        }

        item {
            NoticeCard("تعني نسبة الاكتمال اكتمال طبقة محددة بحسب مقام مؤرخ ومصدر ظاهر، ولا تعني اكتمال جميع أماكن الدولة.")
        }

        if (details.libraryDocumentCount > 0) {
            item {
                Card(
                    shape = RoundedCornerShape(22.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer),
                ) {
                    Column(Modifier.fillMaxWidth().padding(18.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.LocalLibrary, null, tint = MaterialTheme.colorScheme.primary)
                            Spacer(Modifier.width(10.dp))
                            Column(Modifier.weight(1f)) {
                                Text("الموسوعة الكاملة", style = MaterialTheme.typography.titleLarge)
                                Text(
                                    "${ArabicLabels.number(details.libraryDocumentCount)} ملفًا عن التاريخ والجغرافيا والاقتصاد والثقافة والتقسيمات والمدن والقرى والأحياء",
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                )
                            }
                        }
                        Spacer(Modifier.height(13.dp))
                        Button(onClick = { onOpenLibrary(details.country.code) }, modifier = Modifier.fillMaxWidth()) {
                            Text("فتح جميع ملفات ${details.country.nameAr}")
                        }
                    }
                }
            }
        }

        item { SectionTitle("التغطية", "حالة كل طبقة وفق المصدر واللقطة الخاصة بها") }

        item {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                items(details.coverage, key = { it.id }) { coverage ->
                    CoverageCard(coverage, Modifier.width(285.dp))
                }
            }
        }

        item { SectionTitle("الكيانات والأماكن", "ابحث بالأسماء الرسمية والبديلة ثم صفِّ النتائج حسب النوع") }

        item { SearchField(query, { query = it }, placeholder = "ابحث داخل ${details.country.nameAr}…") }

        item {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                item {
                    FilterChip(
                        selected = selectedType == null,
                        onClick = { selectedType = null },
                        label = { Text("الكل (${ArabicLabels.number(baseEntities.size)})") },
                    )
                }
                items(details.typeCounts, key = { it.type }) { item ->
                    FilterChip(
                        selected = selectedType == item.type,
                        onClick = { selectedType = if (selectedType == item.type) null else item.type },
                        label = { Text("${ArabicLabels.entityType(item.type)} (${ArabicLabels.number(item.count)})") },
                    )
                }
            }
        }

        if (searching) {
            item {
                Row(Modifier.fillMaxWidth().padding(12.dp), horizontalArrangement = Arrangement.Center) {
                    Icon(Icons.Default.Search, null, tint = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(8.dp))
                    Text("نبحث في الأسماء البديلة…", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        } else if (shownEntities.isEmpty()) {
            item { EmptyState("لا توجد نتائج", "جرّب اسمًا آخر أو أزل مرشح النوع") }
        } else {
            item {
                Text(
                    "${ArabicLabels.number(shownEntities.size)} نتيجة",
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            items(shownEntities, key = { it.id }) { entity ->
                EntityRow(
                    entity = entity,
                    onClick = { onOpenEntity(entity.id) },
                    secondary = "${ArabicLabels.entityType(entity.type)} • ${ArabicLabels.status(entity.status)}",
                )
            }
        }

        item { SectionTitle("المصادر المستخدمة", "${ArabicLabels.number(details.sources.size)} مصدرًا مرتبطًا ببيانات الدولة") }
        items(details.sources.take(8), key = { it.id }) { source ->
            SourceCard(source, onClick = { onOpenSource(source.id) })
        }
        if (details.sources.size > 8) {
            item {
                Text(
                    "تجد بقية المصادر في قسم المصادر الرئيسي.",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    style = MaterialTheme.typography.bodyMedium,
                )
            }
        }

        if (details.documents.isNotEmpty()) {
            item { SectionTitle("وثائق البيانات", "ملفات النطاق والقيود وحالة المجالات محفوظة كاملة") }
            items(details.documents, key = { it.id }) { document ->
                Card(
                    onClick = { onOpenDocument(document.id) },
                    shape = RoundedCornerShape(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                ) {
                    Row(Modifier.fillMaxWidth().padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Description, null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(Modifier.width(12.dp))
                        Column(Modifier.weight(1f)) {
                            Text(document.title, style = MaterialTheme.typography.titleMedium, maxLines = 1, overflow = TextOverflow.Ellipsis)
                            Text(ArabicLabels.documentKind(document.kind), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun CoverageCard(item: com.atlasalarab.app.data.CoverageItem, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier,
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Column(Modifier.padding(18.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    ArabicLabels.layer(item.layer),
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.weight(1f),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                ContentBadge(
                    if (item.complete) ContentKind.Authoritative else ContentKind.Partial,
                    compact = true,
                )
            }
            Spacer(Modifier.height(12.dp))
            val progress = (item.percentage ?: 0.0).toFloat().div(100f).coerceIn(0f, 1f)
            LinearProgressIndicator(
                progress = { progress },
                modifier = Modifier.fillMaxWidth().height(7.dp).clip(RoundedCornerShape(7.dp)),
                trackColor = MaterialTheme.colorScheme.surfaceVariant,
            )
            Spacer(Modifier.height(10.dp))
            Text(
                item.percentage?.let { "${ArabicLabels.decimal(it)}٪ تغطية" } ?: "تغطية بلا مقام وطني",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary,
            )
            Spacer(Modifier.height(8.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                CoverageMetric("مطابق", ArabicLabels.number(item.matched))
                CoverageMetric("المرجع", item.denominator?.let(ArabicLabels::number) ?: "—")
                if (item.missing != null && item.missing > 0) CoverageMetric("مفقود", ArabicLabels.number(item.missing))
            }
            Spacer(Modifier.height(10.dp))
            Text(
                item.definition,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
            )
            item.snapshotDate?.let {
                Spacer(Modifier.height(7.dp))
                Text("تاريخ اللقطة: $it", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}

@Composable
private fun CoverageMetric(label: String, value: String) {
    Surface(shape = RoundedCornerShape(9.dp), color = MaterialTheme.colorScheme.surfaceVariant) {
        Column(Modifier.padding(horizontal = 9.dp, vertical = 5.dp)) {
            Text(value, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
            Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}
