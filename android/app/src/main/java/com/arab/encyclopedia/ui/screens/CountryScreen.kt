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

@Composable
fun CountryScreen(iso2: String, onNavigateToEntity: (String, String) -> Unit) {
    val context = LocalContext.current
    val db = remember { ArabDatabase.getDatabase(context) }
    var entities by remember { mutableStateOf<List<com.arab.encyclopedia.data.EntityRoom>>(emptyList()) }
    var coverage by remember { mutableStateOf<List<com.arab.encyclopedia.data.CoverageRoom>>(emptyList()) }
    var manifest by remember { mutableStateOf<com.arab.encyclopedia.data.ManifestRoom?>(null) }
    var selectedTab by remember { mutableStateOf(0) }
    val tabs = listOf("نظرة عامة", "التقسيم الإداري", "الطبقات", "الأماكن", "التغطية والقيود", "الخام")

    LaunchedEffect(iso2) {
        entities = db.entityDao().getByCountry(iso2)
        coverage = db.coverageDao().getByCountry(iso2)
        manifest = db.manifestDao().getByIso(iso2)
    }

    Column(modifier = Modifier.fillMaxSize()) {
        // Header
        Card(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("${iso2} — ${entities.firstOrNull { it.entityType == "country" }?.canonicalName ?: iso2}", style = MaterialTheme.typography.headlineMedium)
                Text("كيانات: ${entities.size} — طبقات: ${coverage.size} — مكتملة: ${coverage.count { it.complete }}", style = MaterialTheme.typography.bodySmall)
                manifest?.let {
                    Text("Caveats: ${it.rawJson.take(200)}...", style = MaterialTheme.typography.labelSmall)
                }
            }
        }

        TabRow(selectedTabIndex = selectedTab) {
            tabs.forEachIndexed { idx, title ->
                Tab(selected = selectedTab == idx, onClick = { selectedTab = idx }, text = { Text(title, maxLines = 1) })
            }
        }

        when (selectedTab) {
            0 -> {
                // Overview
                LazyColumn(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    item { Text("أنواع الكيانات في هذه الدولة:", style = MaterialTheme.typography.titleSmall) }
                    val types = entities.groupBy { it.entityType }
                    items(types.entries.toList()) { (type, list) ->
                        Card(modifier = Modifier.fillMaxWidth()) {
                            Text("$type: ${list.size}", modifier = Modifier.padding(8.dp))
                        }
                    }
                }
            }
            1,2 -> {
                LazyColumn(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    items(coverage) { cov ->
                        Card(modifier = Modifier.fillMaxWidth()) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text("${cov.layer} — ${cov.complete.let { if (it) "✅ مكتمل" else "❌ غير مكتمل" }}", style = MaterialTheme.typography.titleSmall)
                                Text("المقام: ${cov.denominator ?: "—"} — مطابق: ${cov.matched} — مستبعد: ${cov.excluded} — ناقص: ${cov.missing ?: "—"}", style = MaterialTheme.typography.bodySmall)
                                Text("النسبة: ${cov.coveragePercentage ?: "— (لا تُحسب)"} ${cov.missingReason ?: ""}", style = MaterialTheme.typography.labelSmall)
                                Text("المصدر: ${cov.sourceId} — اللقطة: ${cov.snapshotId}", style = MaterialTheme.typography.labelSmall)
                                Text(cov.notes ?: "", style = MaterialTheme.typography.bodySmall)
                            }
                        }
                    }
                }
            }
            3 -> {
                LazyColumn(modifier = Modifier.padding(8.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    items(entities.take(200)) { ent ->
                        Card(modifier = Modifier.fillMaxWidth(), onClick = { onNavigateToEntity(ent.countryCode, ent.id) }) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text(ent.canonicalName, style = MaterialTheme.typography.titleSmall)
                                Text("${ent.id} — ${ent.entityType} — ${ent.status}", style = MaterialTheme.typography.labelSmall)
                                Text(ent.notes?.take(80) ?: "", style = MaterialTheme.typography.bodySmall)
                            }
                        }
                    }
                }
            }
            4 -> {
                LazyColumn(modifier = Modifier.padding(16.dp)) {
                    items(coverage.filter { !it.complete }) { cov ->
                        Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text("قيود طبقة ${cov.layer}", style = MaterialTheme.typography.titleSmall)
                                Text("missing_reason: ${cov.missingReason ?: "—"}", style = MaterialTheme.typography.bodySmall)
                                Text(cov.notes ?: "", style = MaterialTheme.typography.bodySmall)
                            }
                        }
                    }
                }
            }
            5 -> {
                LazyColumn(modifier = Modifier.padding(16.dp)) {
                    item {
                        Text("Manifest Raw", style = MaterialTheme.typography.titleSmall)
                        Text(manifest?.rawJson?.take(2000) ?: "—", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }
        }
    }
}
