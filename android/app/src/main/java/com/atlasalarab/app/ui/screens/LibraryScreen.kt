package com.atlasalarab.app.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.FolderOpen
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.Icon
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
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.CountrySummary
import com.atlasalarab.app.data.LibraryDocumentSummary
import com.atlasalarab.app.data.LibraryOverview
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.EmptyState
import com.atlasalarab.app.ui.components.ErrorPane
import com.atlasalarab.app.ui.components.LibraryDocumentRow
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.LoadingPane
import com.atlasalarab.app.ui.components.NoticeCard
import com.atlasalarab.app.ui.components.SearchField
import com.atlasalarab.app.ui.components.SectionTitle
import kotlinx.coroutines.delay

@Composable
fun LibraryScreen(
    repository: AtlasRepository,
    initialCountryCode: String? = null,
    onOpenDocument: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    if (initialCountryCode != null) {
        CountryLibraryScreen(
            countryCode = initialCountryCode,
            repository = repository,
            onOpenDocument = onOpenDocument,
            modifier = modifier,
        )
    } else {
        GlobalLibraryScreen(repository, onOpenDocument, modifier)
    }
}

@Composable
private fun CountryLibraryScreen(
    countryCode: String,
    repository: AtlasRepository,
    onOpenDocument: (String) -> Unit,
    modifier: Modifier,
) {
    val state = produceState<LoadState<Pair<LibraryOverview, CountrySummary?>>>(
        LoadState.Loading,
        countryCode,
        repository,
    ) {
        value = try {
            LoadState.Ready(
                repository.libraryOverview(countryCode) to
                    repository.countries().firstOrNull { it.code == countryCode },
            )
        } catch (error: Exception) {
            LoadState.Failed(error.message ?: "خطأ غير معروف")
        }
    }.value
    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> state.value.second?.let { country ->
            CountryLibraryContent(
                overview = state.value.first,
                country = country,
                repository = repository,
                onOpenDocument = onOpenDocument,
                modifier = modifier,
            )
        } ?: ErrorPane("لم نجد الدولة المطلوبة", modifier)
    }
}

@Composable
private fun CountryLibraryContent(
    overview: LibraryOverview,
    country: CountrySummary,
    repository: AtlasRepository,
    onOpenDocument: (String) -> Unit,
    modifier: Modifier,
) {
    var query by remember(country.code) { mutableStateOf("") }
    var selectedCategory by remember(country.code) { mutableStateOf<String?>(null) }
    var searchResults by remember(country.code) { mutableStateOf<List<LibraryDocumentSummary>?>(null) }
    var searching by remember { mutableStateOf(false) }

    val documents = overview.documents
    val topicDocuments = remember(documents) {
        CORE_TOPIC_ORDER.mapNotNull { category ->
            documents.firstOrNull { it.collection == "الدول" && it.category == category }
        }.distinctBy { it.id }
    }
    val topicIds = remember(topicDocuments) { topicDocuments.mapTo(hashSetOf()) { it.id } }
    val groupedCategories = remember(documents, topicIds) {
        documents
            .filterNot { it.id in topicIds }
            .groupBy { it.category }
            .filter { (category, values) -> values.size > 1 || ADMINISTRATIVE_WORDS.any(category::contains) }
            .entries
            .sortedWith(compareByDescending<Map.Entry<String, List<LibraryDocumentSummary>>> { it.value.size }.thenBy { it.key })
    }
    val groupedNames = remember(groupedCategories) { groupedCategories.mapTo(hashSetOf()) { it.key } }
    val extraDocuments = remember(documents, topicIds, groupedNames) {
        documents.filterNot { it.id in topicIds || it.category in groupedNames }
    }

    LaunchedEffect(query, selectedCategory, country.code) {
        if (query.trim().length < 2) {
            searchResults = null
            searching = false
        } else {
            searching = true
            delay(280)
            searchResults = repository.searchLibrary(
                query = query,
                countryCode = country.code,
                category = selectedCategory,
            )
            searching = false
        }
    }

    val selectedDocuments = selectedCategory?.let { category -> documents.filter { it.category == category } }.orEmpty()
    val showingList = selectedCategory != null || query.trim().length >= 2
    val visibleDocuments = searchResults ?: selectedDocuments

    LazyColumn(
        modifier = modifier,
        contentPadding = PaddingValues(start = 18.dp, end = 18.dp, top = 16.dp, bottom = 30.dp),
        verticalArrangement = Arrangement.spacedBy(14.dp),
    ) {
        item {
            CountryLibraryHero(country, overview)
        }
        item {
            SearchField(
                value = query,
                onValueChange = { query = it },
                placeholder = "ابحث في تاريخ وثقافة ومدن ${country.nameAr}…",
            )
        }

        if (showingList) {
            item {
                Row(Modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
                    FilledTonalButton(onClick = { selectedCategory = null; query = "" }) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, null)
                        Spacer(Modifier.width(6.dp))
                        Text("العودة إلى الأقسام")
                    }
                    Spacer(Modifier.weight(1f))
                    if (searching) CircularProgressIndicator(Modifier.width(28.dp))
                }
            }
            item {
                SectionTitle(
                    title = selectedCategory ?: "نتائج البحث",
                    subtitle = if (searching) "نبحث داخل النصوص…" else "${ArabicLabels.number(visibleDocuments.size)} ملفًا",
                )
            }
            if (!searching && visibleDocuments.isEmpty()) {
                item { EmptyState("لا توجد نتائج", "جرّب كلمة أخرى أو ارجع إلى أقسام الدولة") }
            } else {
                items(visibleDocuments, key = { it.id }) { document ->
                    LibraryDocumentRow(document, onClick = { onOpenDocument(document.id) })
                }
            }
        } else {
            item {
                NoticeCard("اختر موضوعًا للقراءة أو افتح أحد أقسام الأماكن والتقسيمات. جميع الملفات محفوظة بالنص الكامل وتعمل دون إنترنت.")
            }

            if (topicDocuments.isNotEmpty()) {
                item { SectionTitle("ملف الدولة الموسوعي", "الموضوعات الأساسية مرتبة للقراءة السريعة") }
                items(topicDocuments.chunked(2)) { rowDocuments ->
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(11.dp)) {
                        rowDocuments.forEach { document ->
                            CountryTopicCard(
                                document = document,
                                onClick = { onOpenDocument(document.id) },
                                modifier = Modifier.weight(1f),
                            )
                        }
                        if (rowDocuments.size == 1) Spacer(Modifier.weight(1f))
                    }
                }
            }

            if (groupedCategories.isNotEmpty()) {
                item { SectionTitle("الأماكن والتقسيمات", "افتح القسم ثم اختر المدينة أو المحافظة أو الوحدة المحلية") }
                items(groupedCategories.chunked(2)) { rowCategories ->
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(11.dp)) {
                        rowCategories.forEach { category ->
                            CountryCategoryCard(
                                category = category.key,
                                count = category.value.size,
                                onClick = { selectedCategory = category.key },
                                modifier = Modifier.weight(1f),
                            )
                        }
                        if (rowCategories.size == 1) Spacer(Modifier.weight(1f))
                    }
                }
            }

            if (extraDocuments.isNotEmpty()) {
                item { SectionTitle("ملفات مرتبطة", "العاصمة وجداول البيانات والمواد المحلية الإضافية") }
                items(extraDocuments, key = { it.id }) { document ->
                    LibraryDocumentRow(document, onClick = { onOpenDocument(document.id) })
                }
            }
        }
    }
}

@Composable
private fun CountryLibraryHero(country: CountrySummary, overview: LibraryOverview) {
    Card(
        shape = RoundedCornerShape(28.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
    ) {
        Column(Modifier.fillMaxWidth().padding(22.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Surface(shape = RoundedCornerShape(18.dp), color = MaterialTheme.colorScheme.surface) {
                    Text(
                        ArabicLabels.flag(country.code),
                        style = MaterialTheme.typography.headlineMedium,
                        modifier = Modifier.padding(12.dp),
                    )
                }
                Spacer(Modifier.width(14.dp))
                Column(Modifier.weight(1f)) {
                    Text("موسوعة ${country.nameAr}", style = MaterialTheme.typography.headlineMedium)
                    Text(
                        "المعرفة مرتبة من الموضوع العام إلى المكان المحلي",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
            Spacer(Modifier.height(16.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(9.dp)) {
                LibraryMetric("ملف", ArabicLabels.number(overview.totalCount), Modifier.weight(1f))
                LibraryMetric("موضوع", ArabicLabels.number(overview.categories.size), Modifier.weight(1f))
                LibraryMetric("الحجم", ArabicLabels.fileSize(overview.totalBytes), Modifier.weight(1f))
            }
        }
    }
}

@Composable
private fun LibraryMetric(label: String, value: String, modifier: Modifier = Modifier) {
    Surface(modifier, shape = RoundedCornerShape(14.dp), color = MaterialTheme.colorScheme.surface.copy(alpha = .88f)) {
        Column(Modifier.padding(horizontal = 10.dp, vertical = 9.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(value, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
            Text(label, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun CountryTopicCard(
    document: LibraryDocumentSummary,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Card(
        modifier = modifier.heightIn(min = 132.dp),
        onClick = onClick,
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
    ) {
        Column(Modifier.fillMaxSize().padding(16.dp)) {
            Text(topicEmoji(document.category), style = MaterialTheme.typography.headlineMedium)
            Spacer(Modifier.height(9.dp))
            Text(document.category, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text(
                topicDescription(document.category),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
            )
        }
    }
}

@Composable
private fun CountryCategoryCard(
    category: String,
    count: Int,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Card(
        modifier = modifier.heightIn(min = 112.dp),
        onClick = onClick,
        shape = RoundedCornerShape(19.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer),
    ) {
        Column(Modifier.fillMaxSize().padding(15.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.FolderOpen, null, tint = MaterialTheme.colorScheme.primary)
                Spacer(Modifier.weight(1f))
                Surface(shape = RoundedCornerShape(10.dp), color = MaterialTheme.colorScheme.surface) {
                    Text(ArabicLabels.number(count), Modifier.padding(horizontal = 9.dp, vertical = 4.dp), fontWeight = FontWeight.Bold)
                }
            }
            Spacer(Modifier.height(10.dp))
            Text(category, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
            Text("اضغط لاستعراض الملفات", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun GlobalLibraryScreen(
    repository: AtlasRepository,
    onOpenDocument: (String) -> Unit,
    modifier: Modifier,
) {
    val state = produceState<LoadState<Pair<LibraryOverview, List<CountrySummary>>>>(
        LoadState.Loading,
        repository,
    ) {
        value = try {
            LoadState.Ready(repository.libraryOverview() to repository.countries())
        } catch (error: Exception) {
            LoadState.Failed(error.message ?: "خطأ غير معروف")
        }
    }.value
    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> GlobalLibraryContent(
            overview = state.value.first,
            countries = state.value.second,
            repository = repository,
            onOpenDocument = onOpenDocument,
            modifier = modifier,
        )
    }
}

@Composable
private fun GlobalLibraryContent(
    overview: LibraryOverview,
    countries: List<CountrySummary>,
    repository: AtlasRepository,
    onOpenDocument: (String) -> Unit,
    modifier: Modifier,
) {
    var query by remember { mutableStateOf("") }
    var selectedCountry by remember { mutableStateOf<String?>(null) }
    var selectedCollection by remember { mutableStateOf<String?>(null) }
    var selectedCategory by remember { mutableStateOf<String?>(null) }
    var searchResults by remember { mutableStateOf<List<LibraryDocumentSummary>?>(null) }
    var searching by remember { mutableStateOf(false) }

    val scopedDocuments = remember(overview.documents, selectedCountry, selectedCollection, selectedCategory) {
        overview.documents.filter { document ->
            (selectedCountry == null || document.countryCode == selectedCountry) &&
                (selectedCollection == null || document.collection == selectedCollection) &&
                (selectedCategory == null || document.category == selectedCategory)
        }
    }
    val categoryCounts = remember(overview.documents, selectedCountry, selectedCollection) {
        overview.documents.asSequence()
            .filter { selectedCountry == null || it.countryCode == selectedCountry }
            .filter { selectedCollection == null || it.collection == selectedCollection }
            .groupingBy { it.category }.eachCount().entries
            .sortedWith(compareByDescending<Map.Entry<String, Int>> { it.value }.thenBy { it.key })
    }

    LaunchedEffect(query, selectedCountry, selectedCollection, selectedCategory) {
        if (query.trim().length < 2) {
            searchResults = null
            searching = false
        } else {
            searching = true
            delay(300)
            searchResults = repository.searchLibrary(query, selectedCountry, selectedCollection, selectedCategory)
            searching = false
        }
    }
    val shown = searchResults ?: scopedDocuments

    Column(modifier.fillMaxSize().padding(horizontal = 18.dp)) {
        SectionTitle(
            "المكتبة الموسوعية",
            "${ArabicLabels.number(overview.totalCount)} ملفًا كاملًا • ${ArabicLabels.fileSize(overview.totalBytes)}",
            Modifier.padding(top = 16.dp, bottom = 12.dp),
        )
        SearchField(query, { query = it }, "ابحث داخل عناوين ومحتوى جميع الملفات…")
        LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp), contentPadding = PaddingValues(vertical = 8.dp)) {
            item { FilterChip(selectedCountry == null, { selectedCountry = null; selectedCategory = null }, label = { Text("كل البلدان") }) }
            items(countries, key = { it.code }) { country ->
                FilterChip(
                    selectedCountry == country.code,
                    { selectedCountry = if (selectedCountry == country.code) null else country.code; selectedCategory = null },
                    label = { Text("${ArabicLabels.flag(country.code)} ${country.nameAr}") },
                )
            }
        }
        LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            item { FilterChip(selectedCollection == null, { selectedCollection = null; selectedCategory = null }, label = { Text("كل الأقسام") }) }
            items(overview.collections, key = { it.collection }) { collection ->
                FilterChip(
                    selectedCollection == collection.collection,
                    {
                        selectedCollection = if (selectedCollection == collection.collection) null else collection.collection
                        selectedCategory = null
                    },
                    label = { Text(ArabicLabels.libraryCollection(collection.collection)) },
                )
            }
        }
        if (categoryCounts.isNotEmpty()) {
            LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp), contentPadding = PaddingValues(vertical = 7.dp)) {
                item { FilterChip(selectedCategory == null, { selectedCategory = null }, label = { Text("كل الموضوعات") }) }
                items(categoryCounts, key = { it.key }) { category ->
                    FilterChip(
                        selectedCategory == category.key,
                        { selectedCategory = if (selectedCategory == category.key) null else category.key },
                        label = { Text("${category.key} (${ArabicLabels.number(category.value)})") },
                    )
                }
            }
        }
        Row(Modifier.fillMaxWidth().padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Default.Search, null, tint = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.width(7.dp))
            Text(
                if (searching) "نبحث داخل النصوص…" else "${ArabicLabels.number(shown.size)} ملفًا",
                style = MaterialTheme.typography.labelLarge,
            )
        }
        if (!searching && shown.isEmpty()) {
            EmptyState("لا توجد ملفات مطابقة", "غيّر كلمات البحث أو المرشحات", Modifier.weight(1f))
        } else {
            LazyColumn(
                Modifier.weight(1f),
                contentPadding = PaddingValues(bottom = 26.dp),
                verticalArrangement = Arrangement.spacedBy(9.dp),
            ) {
                items(shown, key = { it.id }) { document ->
                    LibraryDocumentRow(document, onClick = { onOpenDocument(document.id) })
                }
            }
        }
    }
}

private val CORE_TOPIC_ORDER = listOf(
    "الفهرس", "معلومات عامة", "التاريخ", "الجغرافيا", "الاقتصاد",
    "المجتمع والقبائل", "المجتمع والطوائف", "اللهجات", "الطعام", "اللباس",
    "العادات والثقافة", "العادات والتقاليد", "الثقافة الشعبية", "الشخصيات والآثار",
    "بطاقة الخلاصة والفجوات", "التقرير النهائي", "المصادر",
)

private val ADMINISTRATIVE_WORDS = listOf(
    "المحافظ", "الولايات", "المدن", "القرى", "الأحياء", "الحارات", "الألوية",
    "الأقضية", "المديريات", "المناطق", "البلديات", "المراكز", "المعتمديات",
    "العمادات", "الجماعات", "المقاطعات", "الأقاليم", "الإمارات", "الشعبيات",
)

private fun topicEmoji(category: String): String = when (category) {
    "الفهرس" -> "🧭"
    "معلومات عامة" -> "🪪"
    "التاريخ" -> "⌛"
    "الجغرافيا" -> "🗺️"
    "الاقتصاد" -> "📈"
    "المجتمع والقبائل", "المجتمع والطوائف" -> "👥"
    "اللهجات" -> "💬"
    "الطعام" -> "🍲"
    "اللباس" -> "👗"
    "العادات والثقافة", "العادات والتقاليد", "الثقافة الشعبية" -> "🎭"
    "الشخصيات والآثار" -> "🏛️"
    "بطاقة الخلاصة والفجوات", "التقرير النهائي" -> "✅"
    "المصادر" -> "📚"
    else -> "📄"
}

private fun topicDescription(category: String): String = when (category) {
    "الفهرس" -> "مدخل سريع إلى جميع أقسام الدولة"
    "معلومات عامة" -> "بطاقة الدولة والتقسيم الإداري"
    "التاريخ" -> "خط زمني وتحولات تاريخية"
    "الجغرافيا" -> "التضاريس والمناخ والأقاليم"
    "الاقتصاد" -> "العمل والموارد والقطاعات"
    "المجتمع والقبائل", "المجتمع والطوائف" -> "السكان والبنية الاجتماعية"
    "اللهجات" -> "التنوع اللغوي والألفاظ المحلية"
    "الطعام" -> "المطبخ والأطباق والمناطق"
    "اللباس" -> "الأزياء والملابس التقليدية"
    "العادات والثقافة", "العادات والتقاليد" -> "العادات والفنون والمناسبات"
    "الثقافة الشعبية" -> "الأمثال والحكايات والمهرجانات"
    "الشخصيات والآثار" -> "الأعلام والمواقع التاريخية"
    "بطاقة الخلاصة والفجوات" -> "ملخص التغطية وما ينقصها"
    "التقرير النهائي" -> "نتيجة الدراسة الموسوعية"
    "المصادر" -> "المراجع المستخدمة في الملفات"
    else -> "فتح الملف وقراءة محتواه"
}
