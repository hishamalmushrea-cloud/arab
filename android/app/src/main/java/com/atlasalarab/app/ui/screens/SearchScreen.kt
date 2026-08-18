package com.atlasalarab.app.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
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
import androidx.compose.ui.unit.dp
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.CountrySummary
import com.atlasalarab.app.data.LibraryDocumentSummary
import com.atlasalarab.app.data.SearchResult
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.EmptyState
import com.atlasalarab.app.ui.components.EntityRow
import com.atlasalarab.app.ui.components.LibraryDocumentRow
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.SearchField
import com.atlasalarab.app.ui.components.SectionTitle
import kotlinx.coroutines.delay

@Composable
fun SearchScreen(
    repository: AtlasRepository,
    onOpenEntity: (String) -> Unit,
    onOpenLibraryDocument: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    val countryState = produceState<LoadState<List<CountrySummary>>>(LoadState.Loading, repository) {
        value = try { LoadState.Ready(repository.countries()) }
        catch (error: Exception) { LoadState.Failed(error.message ?: "تعذر تحميل الدول") }
    }.value
    val countries = (countryState as? LoadState.Ready)?.value.orEmpty()
    var query by remember { mutableStateOf("") }
    var selectedCountry by remember { mutableStateOf<String?>(null) }
    var results by remember { mutableStateOf<List<SearchResult>>(emptyList()) }
    var libraryResults by remember { mutableStateOf<List<LibraryDocumentSummary>>(emptyList()) }
    var searching by remember { mutableStateOf(false) }
    var searched by remember { mutableStateOf(false) }

    LaunchedEffect(query, selectedCountry) {
        if (query.trim().length < 2) {
            results = emptyList()
            libraryResults = emptyList()
            searching = false
            searched = false
        } else {
            searching = true
            delay(280)
            results = repository.search(query, selectedCountry)
            libraryResults = repository.searchLibrary(query, selectedCountry)
            searching = false
            searched = true
        }
    }

    Column(modifier.fillMaxSize().padding(horizontal = 18.dp)) {
        SectionTitle("البحث الشامل", "يفحص الأماكن والأسماء البديلة ومحتوى 2,740 ملفًا موسوعيًا", Modifier.padding(top = 16.dp, bottom = 14.dp))
        SearchField(query, { query = it }, placeholder = "مكان، اقتصاد، تاريخ، طعام، لهجة…")
        LazyRow(
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            contentPadding = PaddingValues(vertical = 10.dp),
        ) {
            item {
                FilterChip(selected = selectedCountry == null, onClick = { selectedCountry = null }, label = { Text("كل الدول") })
            }
            items(countries, key = { it.code }) { country ->
                FilterChip(
                    selected = selectedCountry == country.code,
                    onClick = { selectedCountry = if (selectedCountry == country.code) null else country.code },
                    label = { Text("${ArabicLabels.flag(country.code)} ${country.nameAr}") },
                )
            }
        }

        when {
            searching -> Box(Modifier.weight(1f).fillMaxWidth(), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    CircularProgressIndicator()
                    Text("نبحث محليًا في الأسماء ومحتوى آلاف الملفات…", Modifier.padding(top = 12.dp), color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            query.trim().length < 2 -> Box(Modifier.weight(1f), contentAlignment = Alignment.Center) {
                EmptyState("اكتب حرفين على الأقل", "جرّب: صنعاء، قرطاج، السلط أو الرياض")
            }
            searched && results.isEmpty() && libraryResults.isEmpty() -> Box(Modifier.weight(1f), contentAlignment = Alignment.Center) {
                EmptyState("لم نعثر على نتيجة", "جرّب تهجئة مختلفة أو اختر كل الدول")
            }
            else -> {
                Row(Modifier.fillMaxWidth().padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Search, null, tint = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(7.dp))
                    Text("${ArabicLabels.number(results.size + libraryResults.size)} نتيجة", style = MaterialTheme.typography.labelLarge)
                }
                LazyColumn(
                    modifier = Modifier.weight(1f),
                    contentPadding = PaddingValues(bottom = 26.dp),
                    verticalArrangement = Arrangement.spacedBy(9.dp),
                ) {
                    if (results.isNotEmpty()) {
                        item {
                            Text(
                                "الأماكن والكيانات (${ArabicLabels.number(results.size)})",
                                style = MaterialTheme.typography.titleMedium,
                                color = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.padding(top = 4.dp),
                            )
                        }
                        items(results, key = { it.entity.id }) { result ->
                            val matched = if (!result.canonicalMatch && result.matchedName != result.entity.name) {
                                "طابق: ${result.matchedName} • ${result.entity.countryName}"
                            } else {
                                "${ArabicLabels.entityType(result.entity.type)} • ${result.entity.countryName}"
                            }
                            EntityRow(result.entity, onClick = { onOpenEntity(result.entity.id) }, secondary = matched)
                        }
                    }
                    if (libraryResults.isNotEmpty()) {
                        item {
                            Text(
                                "ملفات الموسوعة (${ArabicLabels.number(libraryResults.size)})",
                                style = MaterialTheme.typography.titleMedium,
                                color = MaterialTheme.colorScheme.primary,
                                modifier = Modifier.padding(top = 12.dp),
                            )
                        }
                        items(libraryResults, key = { "library-${it.id}" }) { document ->
                            LibraryDocumentRow(document, onClick = { onOpenLibraryDocument(document.id) })
                        }
                    }
                }
            }
        }
    }
}
