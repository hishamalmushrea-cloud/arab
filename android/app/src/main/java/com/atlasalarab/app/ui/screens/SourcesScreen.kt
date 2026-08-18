package com.atlasalarab.app.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.SourceItem
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.EmptyState
import com.atlasalarab.app.ui.components.ErrorPane
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.LoadingPane
import com.atlasalarab.app.ui.components.SearchField
import com.atlasalarab.app.ui.components.SectionTitle
import com.atlasalarab.app.ui.components.SourceCard

@Composable
fun SourcesScreen(
    repository: AtlasRepository,
    onOpenSource: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    val state = produceState<LoadState<List<SourceItem>>>(LoadState.Loading, repository) {
        value = try { LoadState.Ready(repository.sources()) }
        catch (error: Exception) { LoadState.Failed(error.message ?: "خطأ غير معروف") }
    }.value
    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> SourcesContent(state.value, onOpenSource, modifier)
    }
}

@Composable
private fun SourcesContent(sources: List<SourceItem>, onOpenSource: (String) -> Unit, modifier: Modifier) {
    var query by remember { mutableStateOf("") }
    var tier by remember { mutableStateOf<String?>(null) }
    val filtered = remember(sources, query, tier) {
        val needle = query.trim().lowercase()
        sources.filter { source ->
            (tier == null || source.qualityTier == tier) &&
                (needle.isBlank() || source.title.lowercase().contains(needle) ||
                    source.publisher.lowercase().contains(needle) || source.id.lowercase().contains(needle))
        }
    }

    Column(modifier.fillMaxSize().padding(horizontal = 18.dp)) {
        SectionTitle("المصادر", "${ArabicLabels.number(sources.size)} مصدرًا ذريًا محفوظًا مع الترخيص والتاريخ", Modifier.padding(top = 16.dp, bottom = 14.dp))
        SearchField(query, { query = it }, placeholder = "ابحث بعنوان المصدر أو الناشر…")
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            contentPadding = PaddingValues(vertical = 10.dp),
        ) {
            item { FilterChip(tier == null, { tier = null }, label = { Text("الكل") }) }
            items(listOf("A", "B", "C")) { value ->
                FilterChip(tier == value, { tier = if (tier == value) null else value }, label = { Text(ArabicLabels.sourceTier(value)) })
            }
        }
        Row(Modifier.padding(bottom = 9.dp)) {
            Text("${ArabicLabels.number(filtered.size)} مصدر", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        if (filtered.isEmpty()) {
            EmptyState("لا توجد مصادر مطابقة", "غيّر كلمات البحث أو مستوى المصدر", Modifier.weight(1f))
        } else {
            LazyColumn(
                modifier = Modifier.weight(1f),
                contentPadding = PaddingValues(bottom = 26.dp),
                verticalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                items(filtered, key = { it.id }) { source ->
                    SourceCard(source, onClick = { onOpenSource(source.id) })
                }
            }
        }
    }
}
