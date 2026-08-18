package com.atlasalarab.app.ui.screens

import android.content.Intent
import android.net.Uri
import android.widget.Toast
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.ScrollState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.NavigateBefore
import androidx.compose.material.icons.automirrored.filled.NavigateNext
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.TableChart
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.FilterChip
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.produceState
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.runtime.snapshotFlow
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Density
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.LibraryDocument
import com.atlasalarab.app.data.ReadingStore
import com.atlasalarab.app.data.normalizeArabic
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.ContentBadge
import com.atlasalarab.app.ui.components.ContentKind
import com.atlasalarab.app.ui.components.ErrorPane
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.LoadingPane
import com.atlasalarab.app.ui.components.MarkdownBlock
import com.atlasalarab.app.ui.components.MarkdownBlockView
import com.atlasalarab.app.ui.components.NoticeCard
import com.atlasalarab.app.ui.components.inlineMarkdown
import com.atlasalarab.app.ui.components.markdownBlockText
import com.atlasalarab.app.ui.components.parseMarkdown
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.flow.distinctUntilChanged
import kotlinx.coroutines.launch

@Composable
fun LibraryDocumentScreen(
    id: String,
    repository: AtlasRepository,
    readingStore: ReadingStore,
    onOpenDocument: (String) -> Unit,
    onOpenCountryLibrary: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    val state = produceState<LoadState<LibraryDocument?>>(LoadState.Loading, id, repository) {
        value = try { LoadState.Ready(repository.libraryDocument(id)) }
        catch (error: Exception) { LoadState.Failed(error.message ?: "خطأ غير معروف") }
    }.value
    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> state.value?.let {
            LibraryDocumentContent(
                document = it,
                repository = repository,
                readingStore = readingStore,
                onOpenDocument = onOpenDocument,
                onOpenCountryLibrary = onOpenCountryLibrary,
                modifier = modifier,
            )
        } ?: ErrorPane("لم نجد الملف المطلوب", modifier)
    }
}

@Composable
private fun LibraryDocumentContent(
    document: LibraryDocument,
    repository: AtlasRepository,
    readingStore: ReadingStore,
    onOpenDocument: (String) -> Unit,
    onOpenCountryLibrary: (String) -> Unit,
    modifier: Modifier,
) {
    val clipboard = LocalClipboardManager.current
    val context = LocalContext.current
    val summary = document.summary
    val listState = rememberLazyListState()
    val csvHorizontalScroll = rememberScrollState()
    val scope = rememberCoroutineScope()
    val favorites by readingStore.favorites.collectAsStateWithLifecycle()
    val isFavorite = favorites.any { it.id == summary.id }
    var readerScale by remember { mutableFloatStateOf(1f) }
    var showTechnicalDetails by remember { mutableStateOf(false) }
    var showSearch by remember { mutableStateOf(false) }
    var documentQuery by remember { mutableStateOf("") }
    var currentMatch by remember { mutableIntStateOf(0) }

    val markdownBlocks = remember(document.content, summary.fileType) {
        if (summary.fileType != "markdown") emptyList()
        else parseMarkdown(document.content).let { blocks ->
            if (blocks.firstOrNull() is MarkdownBlock.Heading &&
                (blocks.first() as MarkdownBlock.Heading).level == 1
            ) blocks.drop(1) else blocks
        }
    }
    val headings = remember(markdownBlocks) {
        markdownBlocks.mapIndexedNotNull { index, block ->
            (block as? MarkdownBlock.Heading)?.takeIf { it.level <= 3 }?.let { index to it }
        }
    }
    val csvLines = remember(document.content, summary.fileType) {
        if (summary.fileType == "csv") document.content.replace("\r\n", "\n").lines() else emptyList()
    }
    val normalizedQuery = normalizeArabic(documentQuery)
    val matchingContentIndices = remember(markdownBlocks, csvLines, normalizedQuery, summary.fileType) {
        if (normalizedQuery.length < 2) emptyList()
        else if (summary.fileType == "markdown") {
            markdownBlocks.mapIndexedNotNull { index, block ->
                index.takeIf { normalizeArabic(markdownBlockText(block)).contains(normalizedQuery) }
            }
        } else {
            csvLines.mapIndexedNotNull { index, line -> index.takeIf { normalizeArabic(line).contains(normalizedQuery) } }
        }
    }
    val hasContents = headings.isNotEmpty()
    val contentStartIndex = 3 + (if (showSearch) 1 else 0) + (if (hasContents) 1 else 0)
    val searchResultStartIndex = contentStartIndex + (if (summary.fileType == "csv") 1 else 0)
    val baseDensity = LocalDensity.current

    LaunchedEffect(summary.id) {
        readingStore.recordOpen(summary)
        val savedPosition = readingStore.position(summary.id)
        val maximumPosition = (if (summary.fileType == "csv") csvLines.size else markdownBlocks.size) + 6
        if (savedPosition > 0) listState.scrollToItem(savedPosition.coerceAtMost(maximumPosition))
    }
    LaunchedEffect(listState, summary.id) {
        snapshotFlow { listState.firstVisibleItemIndex }
            .distinctUntilChanged()
            .collect { readingStore.savePosition(summary.id, it) }
    }
    LaunchedEffect(documentQuery) { currentMatch = 0 }
    LaunchedEffect(currentMatch, matchingContentIndices, searchResultStartIndex) {
        matchingContentIndices.getOrNull(currentMatch)?.let { blockIndex ->
            listState.animateScrollToItem(searchResultStartIndex + blockIndex)
        }
    }

    fun openMarkdownLink(target: String) {
        when {
            target.startsWith("#") -> {
                val wanted = normalizeArabic(Uri.decode(target.removePrefix("#")).replace('-', ' '))
                val heading = headings.firstOrNull { (_, item) -> normalizeArabic(item.text).contains(wanted) }
                if (heading != null) scope.launch { listState.animateScrollToItem(contentStartIndex + heading.first) }
            }
            target.startsWith("http://") || target.startsWith("https://") -> {
                runCatching { context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(target))) }
            }
            else -> scope.launch {
                val linkedId = repository.resolveLibraryLink(summary.relativePath, target)
                if (linkedId != null) onOpenDocument(linkedId)
                else Toast.makeText(context, "هذا الرابط غير متوفر داخل المكتبة", Toast.LENGTH_SHORT).show()
            }
        }
    }

    Box(modifier.fillMaxSize(), contentAlignment = Alignment.TopCenter) {
        LazyColumn(
            state = listState,
            modifier = Modifier.widthIn(max = 860.dp).fillMaxSize(),
            contentPadding = PaddingValues(start = 18.dp, end = 18.dp, top = 16.dp, bottom = 36.dp),
            verticalArrangement = Arrangement.spacedBy(11.dp),
        ) {
            item {
                DocumentHero(document, onOpenCountryLibrary)
            }
            item {
                NoticeCard("مادة موسوعية من الملف الأصلي، معروضة كاملة دون اختصار. راجع الملاحظات والمصادر داخل النص عند وجود تقديرات أو فجوات.")
            }
            item {
                ReaderToolbar(
                    selectedScale = readerScale,
                    onScaleChange = { readerScale = it },
                    fileType = summary.fileType,
                    lineCount = if (summary.fileType == "csv") csvLines.size else markdownBlocks.size,
                    isFavorite = isFavorite,
                    onToggleFavorite = { readingStore.toggleFavorite(summary) },
                    onToggleSearch = { showSearch = !showSearch },
                )
            }

            if (showSearch) {
                item {
                    DocumentSearchBar(
                        query = documentQuery,
                        onQueryChange = { documentQuery = it },
                        currentResult = if (matchingContentIndices.isEmpty()) 0 else currentMatch + 1,
                        resultCount = matchingContentIndices.size,
                        onPrevious = {
                            if (matchingContentIndices.isNotEmpty()) {
                                currentMatch = (currentMatch - 1 + matchingContentIndices.size) % matchingContentIndices.size
                            }
                        },
                        onNext = {
                            if (matchingContentIndices.isNotEmpty()) currentMatch = (currentMatch + 1) % matchingContentIndices.size
                        },
                        onClose = { showSearch = false; documentQuery = "" },
                    )
                }
            }

            if (hasContents) {
                item {
                    Column {
                        Text("في هذا الملف", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.height(7.dp))
                        LazyRow(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                            items(headings, key = { it.first }) { (blockIndex, heading) ->
                                FilterChip(
                                    selected = false,
                                    onClick = { scope.launch { listState.animateScrollToItem(contentStartIndex + blockIndex) } },
                                    label = { Text(inlineMarkdown(heading.text)) },
                                )
                            }
                        }
                    }
                }
            }

            if (summary.fileType == "markdown") {
                itemsIndexed(markdownBlocks) { _, block ->
                    CompositionLocalProvider(
                        LocalDensity provides Density(baseDensity.density, baseDensity.fontScale * readerScale),
                    ) {
                        MarkdownBlockView(
                            block = block,
                            highlightQuery = documentQuery.takeIf { normalizedQuery.length >= 2 }.orEmpty(),
                            onLinkClick = ::openMarkdownLink,
                        )
                    }
                }
            } else {
                item {
                    Text(
                        "جدول كامل — ${ArabicLabels.number(csvLines.size)} صفًا",
                        style = MaterialTheme.typography.titleLarge,
                        color = MaterialTheme.colorScheme.primary,
                        fontWeight = FontWeight.Bold,
                    )
                }
                itemsIndexed(csvLines) { index, line ->
                    CsvLine(index, line, readerScale, baseDensity, documentQuery, csvHorizontalScroll)
                }
            }

            item {
                HorizontalDivider(Modifier.padding(top = 12.dp))
                TextButton(onClick = { showTechnicalDetails = !showTechnicalDetails }) {
                    Icon(Icons.Default.Info, null)
                    Spacer(Modifier.width(7.dp))
                    Text(if (showTechnicalDetails) "إخفاء تفاصيل الملف" else "عرض تفاصيل الملف والمصدر")
                }
            }
            if (showTechnicalDetails) {
                item {
                    Surface(shape = RoundedCornerShape(16.dp), color = MaterialTheme.colorScheme.surfaceVariant) {
                        Column(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(9.dp)) {
                            Text("مسار الملف الأصلي", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                            SelectionContainer {
                                Text(summary.relativePath, fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodyMedium)
                            }
                            TextButton(onClick = { clipboard.setText(AnnotatedString(summary.relativePath)) }) {
                                Icon(Icons.Default.ContentCopy, null)
                                Spacer(Modifier.width(7.dp))
                                Text("نسخ المسار")
                            }
                            Text("بصمة المحتوى", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                            SelectionContainer {
                                Text(document.contentSha256, fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodyMedium)
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun DocumentHero(document: LibraryDocument, onOpenCountryLibrary: (String) -> Unit) {
    val summary = document.summary
    Card(
        shape = RoundedCornerShape(27.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer),
    ) {
        Column(Modifier.fillMaxWidth().padding(22.dp)) {
            Row(
                Modifier.horizontalScroll(rememberScrollState()),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text("المكتبة", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Text("  ‹  ", color = MaterialTheme.colorScheme.outline)
                summary.countryName?.let { countryName ->
                    TextButton(onClick = { summary.countryCode?.let(onOpenCountryLibrary) }) { Text(countryName) }
                    Text("‹", color = MaterialTheme.colorScheme.outline)
                }
                Text(summary.category, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.primary)
            }
            Spacer(Modifier.height(10.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Surface(shape = RoundedCornerShape(13.dp), color = MaterialTheme.colorScheme.surface) {
                    Icon(
                        if (summary.fileType == "csv") Icons.Default.TableChart else Icons.Default.Description,
                        null,
                        tint = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.padding(10.dp),
                    )
                }
                Spacer(Modifier.width(10.dp))
                Text(
                    ArabicLabels.libraryCollection(summary.collection),
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary,
                )
                Spacer(Modifier.weight(1f))
                ContentBadge(ContentKind.Encyclopedic, compact = true)
            }
            Spacer(Modifier.height(14.dp))
            Text(summary.title, style = MaterialTheme.typography.headlineMedium)
            Spacer(Modifier.height(9.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(7.dp)) {
                MetadataPill(if (summary.fileType == "csv") "جدول بيانات" else "مقال موسوعي")
                MetadataPill(ArabicLabels.fileSize(summary.byteSize.toLong()))
            }
        }
    }
}

@Composable
private fun MetadataPill(text: String) {
    Surface(shape = RoundedCornerShape(10.dp), color = MaterialTheme.colorScheme.surface.copy(alpha = .9f)) {
        Text(text, Modifier.padding(horizontal = 10.dp, vertical = 5.dp), style = MaterialTheme.typography.bodyMedium)
    }
}

@Composable
private fun ReaderToolbar(
    selectedScale: Float,
    onScaleChange: (Float) -> Unit,
    fileType: String,
    lineCount: Int,
    isFavorite: Boolean,
    onToggleFavorite: () -> Unit,
    onToggleSearch: () -> Unit,
) {
    Surface(shape = RoundedCornerShape(17.dp), color = MaterialTheme.colorScheme.surface) {
        Column(Modifier.fillMaxWidth().padding(horizontal = 14.dp, vertical = 10.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text("وضع القراءة", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold)
                    Text(
                        if (fileType == "csv") "${ArabicLabels.number(lineCount)} صفًا" else "${ArabicLabels.number(lineCount)} مقطعًا",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                IconButton(onClick = onToggleSearch) { Icon(Icons.Default.Search, "البحث داخل الملف") }
                IconButton(onClick = onToggleFavorite) {
                    Icon(
                        if (isFavorite) Icons.Default.Bookmark else Icons.Default.BookmarkBorder,
                        if (isFavorite) "إزالة من المفضلة" else "إضافة إلى المفضلة",
                        tint = MaterialTheme.colorScheme.primary,
                    )
                }
            }
            Row(horizontalArrangement = Arrangement.spacedBy(5.dp)) {
                listOf(.9f to "أ−", 1f to "أ", 1.18f to "أ+").forEach { (scale, label) ->
                    FilterChip(
                        selected = selectedScale == scale,
                        onClick = { onScaleChange(scale) },
                        label = { Text(label, fontWeight = FontWeight.Bold) },
                    )
                }
            }
        }
    }
}

@Composable
private fun DocumentSearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    currentResult: Int,
    resultCount: Int,
    onPrevious: () -> Unit,
    onNext: () -> Unit,
    onClose: () -> Unit,
) {
    Surface(shape = RoundedCornerShape(17.dp), color = MaterialTheme.colorScheme.secondaryContainer) {
        Column(Modifier.fillMaxWidth().padding(12.dp)) {
            OutlinedTextField(
                value = query,
                onValueChange = onQueryChange,
                modifier = Modifier.fillMaxWidth(),
                singleLine = true,
                shape = RoundedCornerShape(14.dp),
                placeholder = { Text("ابحث داخل هذا الملف…") },
                leadingIcon = { Icon(Icons.Default.Search, null) },
                trailingIcon = { IconButton(onClick = onClose) { Icon(Icons.Default.Close, "إغلاق البحث") } },
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    when {
                        query.trim().length < 2 -> "اكتب حرفين على الأقل"
                        resultCount == 0 -> "لا توجد نتيجة"
                        else -> "$currentResult من ${ArabicLabels.number(resultCount)}"
                    },
                    style = MaterialTheme.typography.bodyMedium,
                    modifier = Modifier.weight(1f),
                )
                IconButton(onClick = onPrevious, enabled = resultCount > 0) {
                    Icon(Icons.AutoMirrored.Filled.NavigateBefore, "النتيجة السابقة")
                }
                IconButton(onClick = onNext, enabled = resultCount > 0) {
                    Icon(Icons.AutoMirrored.Filled.NavigateNext, "النتيجة التالية")
                }
            }
        }
    }
}

@Composable
private fun CsvLine(
    index: Int,
    line: String,
    readerScale: Float,
    baseDensity: Density,
    highlightQuery: String,
    horizontalScroll: ScrollState,
) {
    val cells = remember(line) { parseCsvLine(line) }
    Surface(
        shape = RoundedCornerShape(9.dp),
        color = if (index == 0) MaterialTheme.colorScheme.primaryContainer
        else if (index % 2 == 0) MaterialTheme.colorScheme.surfaceVariant.copy(alpha = .45f)
        else MaterialTheme.colorScheme.surface,
    ) {
        Row(Modifier.fillMaxWidth().padding(vertical = 2.dp), verticalAlignment = Alignment.Top) {
            Text(
                ArabicLabels.number(index + 1),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.outline,
                modifier = Modifier.width(42.dp).padding(horizontal = 8.dp, vertical = 10.dp),
            )
            Row(Modifier.horizontalScroll(horizontalScroll)) {
                cells.forEachIndexed { cellIndex, cell ->
                    CompositionLocalProvider(
                        LocalDensity provides Density(baseDensity.density, baseDensity.fontScale * readerScale),
                    ) {
                        SelectionContainer {
                            Text(
                                inlineMarkdown(cell, highlightQuery.takeIf { normalizeArabic(it).length >= 2 }.orEmpty()),
                                modifier = Modifier.width(if (cellIndex == 0) 165.dp else 210.dp).padding(9.dp),
                                style = if (index == 0) MaterialTheme.typography.labelLarge else MaterialTheme.typography.bodyMedium,
                                fontWeight = if (index == 0) FontWeight.Bold else FontWeight.Normal,
                                color = if (index == 0) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface,
                            )
                        }
                    }
                }
            }
        }
    }
}

private fun parseCsvLine(line: String): List<String> {
    val cells = mutableListOf<String>()
    val current = StringBuilder()
    var quoted = false
    var index = 0
    while (index < line.length) {
        val char = line[index]
        when {
            char == '"' && quoted && index + 1 < line.length && line[index + 1] == '"' -> {
                current.append('"')
                index++
            }
            char == '"' -> quoted = !quoted
            char == ',' && !quoted -> {
                cells += current.toString()
                current.clear()
            }
            else -> current.append(char)
        }
        index++
    }
    cells += current.toString()
    return cells
}
