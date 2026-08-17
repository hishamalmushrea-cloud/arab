package com.arab.encyclopedia.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.arab.encyclopedia.data.ArabDatabase
import kotlinx.coroutines.launch

@Composable
fun SearchScreen(onNavigateToEntity: (String, String) -> Unit) {
    val context = LocalContext.current
    val db = remember { ArabDatabase.getDatabase(context) }
    var query by remember { mutableStateOf("") }
    var results by remember { mutableStateOf<List<com.arab.encyclopedia.data.SearchIndexRoom>>(emptyList()) }
    val scope = rememberCoroutineScope()

    fun doSearch(q: String) {
        scope.launch {
            if (q.isBlank()) {
                // show recent or all
                val all = db.entityDao().getAll().take(50)
                // map to search items loosely
                results = all.map {
                    com.arab.encyclopedia.data.SearchIndexRoom(
                        entityId = it.id,
                        canonicalName = it.canonicalName,
                        normalizedName = it.canonicalName,
                        countryCode = it.countryCode,
                        entityType = it.entityType,
                        status = it.status,
                        aliasesConcatenated = "",
                        normalizedAliases = ""
                    )
                }
            } else {
                val normalized = q.lowercase()
                    .replace(Regex("[\\u064B-\\u065F]"), "")
                    .replace(Regex("[إأآا]"), "ا")
                results = db.searchDao().search(q, normalized)
            }
        }
    }

    LaunchedEffect(Unit) {
        // preload with empty to show something
        doSearch("")
    }

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("البحث الشامل", style = MaterialTheme.typography.headlineMedium)
        Text("يبحث في: الاسم الرسمي، الاسم البديل (عربي/إنجليزي/تاريخي/محلي)، النوع، الدولة. مثال: مقشن", style = MaterialTheme.typography.bodySmall)
        Spacer(Modifier.height(12.dp))
        OutlinedTextField(
            value = query,
            onValueChange = { query = it; doSearch(it) },
            label = { Text("ابحث مثل: مقشن، الرياض، حلبجة") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(Modifier.height(8.dp))
        Text("${results.size} نتيجة", style = MaterialTheme.typography.labelSmall)

        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.fillMaxSize()) {
            items(results) { item ->
                Card(modifier = Modifier.fillMaxWidth(), onClick = {
                    // need to fetch actual entity country
                    scope.launch {
                        val ent = db.entityDao().getById(item.entityId)
                        val iso = ent?.countryCode ?: item.countryCode
                        onNavigateToEntity(iso, item.entityId)
                    }
                }) {
                    Column(modifier = Modifier.padding(12.dp)) {
                        Text(item.canonicalName, style = MaterialTheme.typography.titleMedium)
                        Text("${item.entityId} — ${item.countryCode} — ${item.entityType} — ${item.status}", style = MaterialTheme.typography.labelSmall)
                        if (item.aliasesConcatenated.isNotBlank()) {
                            Text("أسماء بديلة: ${item.aliasesConcatenated.take(80)}", style = MaterialTheme.typography.bodySmall)
                        }
                    }
                }
            }
        }
    }
}
