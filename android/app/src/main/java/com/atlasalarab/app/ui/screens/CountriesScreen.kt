package com.atlasalarab.app.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
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
import com.atlasalarab.app.data.CountrySummary
import com.atlasalarab.app.data.normalizeArabic
import com.atlasalarab.app.ui.components.CountryCard
import com.atlasalarab.app.ui.components.ErrorPane
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.LoadingPane
import com.atlasalarab.app.ui.components.SearchField
import com.atlasalarab.app.ui.components.SectionTitle

@Composable
fun CountriesScreen(
    repository: AtlasRepository,
    onOpenCountry: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    val state = produceState<LoadState<List<CountrySummary>>>(LoadState.Loading, repository) {
        value = try { LoadState.Ready(repository.countries()) }
        catch (error: Exception) { LoadState.Failed(error.message ?: "خطأ غير معروف") }
    }.value

    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> CountriesContent(state.value, onOpenCountry, modifier)
    }
}

@Composable
private fun CountriesContent(
    countries: List<CountrySummary>,
    onOpenCountry: (String) -> Unit,
    modifier: Modifier,
) {
    var query by remember { mutableStateOf("") }
    val normalized = normalizeArabic(query)
    val filtered = remember(countries, normalized) {
        if (normalized.isBlank()) countries
        else countries.filter {
            normalizeArabic(it.nameAr).contains(normalized) ||
                it.nameEn.lowercase().contains(query.trim().lowercase()) ||
                it.code.lowercase().contains(query.trim().lowercase())
        }
    }

    Column(modifier.fillMaxSize().padding(horizontal = 18.dp)) {
        SectionTitle("الدول العربية", "${filtered.size} من ${countries.size} دولة", Modifier.padding(top = 16.dp, bottom = 14.dp))
        SearchField(query, { query = it }, placeholder = "ابحث عن دولة…")
        Text(
            "اضغط على أي دولة لعرض طبقاتها وكياناتها ومصادرها.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(vertical = 12.dp),
        )
        LazyVerticalGrid(
            columns = GridCells.Adaptive(minSize = 175.dp),
            modifier = Modifier.weight(1f),
            contentPadding = PaddingValues(bottom = 24.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            items(filtered, key = { it.code }) { country ->
                CountryCard(country, onClick = { onOpenCountry(country.code) })
            }
        }
    }
}
