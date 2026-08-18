package com.atlasalarab.app.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bookmark
import androidx.compose.material.icons.filled.History
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.atlasalarab.app.data.ReadingStore
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.EmptyState
import com.atlasalarab.app.ui.components.LibraryDocumentRow
import com.atlasalarab.app.ui.components.SectionTitle

@Composable
fun SavedScreen(
    readingStore: ReadingStore,
    onOpenDocument: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    val favorites by readingStore.favorites.collectAsStateWithLifecycle()
    val recent by readingStore.recent.collectAsStateWithLifecycle()
    var showFavorites by remember { mutableStateOf(true) }
    val shown = if (showFavorites) favorites else recent

    Column(modifier.fillMaxSize().padding(horizontal = 18.dp)) {
        SectionTitle(
            title = "مكتبتي",
            subtitle = "محفوظاتك وسجل قراءتك على هذا الجهاز فقط",
            modifier = Modifier.padding(top = 16.dp, bottom = 10.dp),
        )
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            FilterChip(
                selected = showFavorites,
                onClick = { showFavorites = true },
                label = { Text("المفضلة (${ArabicLabels.number(favorites.size)})") },
                leadingIcon = { Icon(Icons.Default.Bookmark, null) },
            )
            FilterChip(
                selected = !showFavorites,
                onClick = { showFavorites = false },
                label = { Text("قرئ مؤخرًا (${ArabicLabels.number(recent.size)})") },
                leadingIcon = { Icon(Icons.Default.History, null) },
            )
        }
        if (!showFavorites && recent.isNotEmpty()) {
            TextButton(onClick = readingStore::clearRecent) { Text("مسح سجل القراءة") }
        }
        if (shown.isEmpty()) {
            EmptyState(
                title = if (showFavorites) "لا توجد ملفات محفوظة" else "لم تفتح ملفًا بعد",
                message = if (showFavorites) "اضغط علامة الحفظ أثناء القراءة" else "ابدأ من مكتبة إحدى الدول",
                modifier = Modifier.weight(1f),
            )
        } else {
            LazyColumn(
                modifier = Modifier.weight(1f),
                contentPadding = PaddingValues(top = 10.dp, bottom = 28.dp),
                verticalArrangement = Arrangement.spacedBy(9.dp),
            ) {
                items(shown, key = { it.id }) { item ->
                    LibraryDocumentRow(item.asSummary(), onClick = { onOpenDocument(item.id) })
                }
            }
        }
    }
}
