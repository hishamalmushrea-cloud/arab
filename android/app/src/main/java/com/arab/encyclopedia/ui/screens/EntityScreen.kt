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
fun EntityScreen(entityId: String, iso2: String, onNavigateToEntity: (String, String) -> Unit) {
    val context = LocalContext.current
    val db = remember { ArabDatabase.getDatabase(context) }
    var entity by remember { mutableStateOf<com.arab.encyclopedia.data.EntityRoom?>(null) }
    var aliases by remember { mutableStateOf<List<com.arab.encyclopedia.data.AliasRoom>>(emptyList()) }
    var claims by remember { mutableStateOf<List<com.arab.encyclopedia.data.ClaimRoom>>(emptyList()) }
    var relationships by remember { mutableStateOf<List<com.arab.encyclopedia.data.RelationshipRoom>>(emptyList()) }
    var sources by remember { mutableStateOf<List<com.arab.encyclopedia.data.SourceRoom>>(emptyList()) }
    var parent by remember { mutableStateOf<com.arab.encyclopedia.data.EntityRoom?>(null) }
    var children by remember { mutableStateOf<List<com.arab.encyclopedia.data.EntityRoom>>(emptyList()) }
    var selectedTab by remember { mutableStateOf(0) }
    val tabs = listOf("الهوية", "الأسماء", "المعلومات", "العلاقات", "المصادر", "الخريطة", "الخام")

    LaunchedEffect(entityId) {
        val ent = db.entityDao().getById(entityId)
        entity = ent
        if (ent != null) {
            aliases = db.aliasDao().getByEntity(ent.id)
            claims = db.claimDao().getBySubject(ent.id)
            relationships = db.relationshipDao().getRelated(ent.id)
            val parentRel = db.relationshipDao().getParent(ent.id)
            if (parentRel != null) {
                parent = db.entityDao().getById(parentRel.parentId)
            }
            val childRels = db.relationshipDao().getChildren(ent.id)
            children = childRels.mapNotNull { db.entityDao().getById(it.childId) }

            // Sources
            val sourceIds = mutableSetOf<String>()
            sourceIds.add(ent.canonicalSourceId)
            aliases.forEach { sourceIds.add(it.sourceId) }
            relationships.forEach { sourceIds.add(it.sourceId) }
            claims.forEach { sourceIds.add(it.sourceId); it.secondSourceId?.let { id -> sourceIds.add(id) } }
            val allSources = db.sourceDao().getAll()
            sources = allSources.filter { it.id in sourceIds }
        }
    }

    if (entity == null) {
        Box(modifier = Modifier.fillMaxSize().padding(16.dp)) {
            Text("جاري تحميل الكيان $entityId...")
        }
        return
    }

    val ent = entity!!

    Column(modifier = Modifier.fillMaxSize()) {
        Card(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(ent.canonicalName, style = MaterialTheme.typography.headlineMedium)
                Text("${ent.id} — ${ent.entityType} — ${ent.status}", style = MaterialTheme.typography.labelSmall)
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    AssistChip(onClick = {}, label = { Text(ent.status) })
                    AssistChip(onClick = {}, label = { Text(ent.verificationStatus) })
                    AssistChip(onClick = {}, label = { Text(ent.confidence) })
                }
                Text("الدولة: ${ent.countryCode} — الوالد: ${parent?.canonicalName ?: "— (جذر)"} — الأبناء: ${children.size}", style = MaterialTheme.typography.bodySmall)
                Text("الإحداثيات: ${if (ent.latitude != null) "${ent.latitude}, ${ent.longitude}" else "غير متوفرة (لا نخترع)"}", style = MaterialTheme.typography.bodySmall)
                Text("الفترة: ${ent.validFrom ?: "—"} → ${ent.validTo ?: "حتى الآن"}", style = MaterialTheme.typography.bodySmall)
            }
        }

        TabRow(selectedTabIndex = selectedTab) {
            tabs.forEachIndexed { idx, title ->
                Tab(selected = selectedTab == idx, onClick = { selectedTab = idx }, text = { Text(title, maxLines = 1) })
            }
        }

        LazyColumn(modifier = Modifier.fillMaxSize().padding(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            when (selectedTab) {
                0 -> {
                    item {
                        Card(modifier = Modifier.fillMaxWidth()) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text("الهوية — كل الحقول محفوظة", style = MaterialTheme.typography.titleSmall)
                                Text("canonical_name: ${ent.canonicalName}\ncanonical_name_language: ${ent.canonicalNameLanguage}\ncanonical_source_id: ${ent.canonicalSourceId}\nsource_locator: ${ent.sourceLocator}\ncountry_code: ${ent.countryCode}\nentity_type: ${ent.entityType}\nstatus: ${ent.status}\nvalid_from: ${ent.validFrom}\nvalid_to: ${ent.validTo}\nverification_status: ${ent.verificationStatus}\nconfidence: ${ent.confidence}\nlegacy_ids: ${ent.legacyIdsJson}\nnotes: ${ent.notes}\nschema_version: ${ent.schemaVersion}", style = MaterialTheme.typography.bodySmall)
                            }
                        }
                    }
                    item {
                        Text("الوالد الإداري", style = MaterialTheme.typography.titleSmall)
                        if (parent != null) {
                            Card(modifier = Modifier.fillMaxWidth(), onClick = { onNavigateToEntity(parent!!.countryCode, parent!!.id) }) {
                                Text("${parent!!.canonicalName} — ${parent!!.id}", modifier = Modifier.padding(12.dp))
                            }
                        } else {
                            Text("— (دولة أو جذر)", modifier = Modifier.padding(8.dp))
                        }
                    }
                    item {
                        Text("الأبناء (${children.size})", style = MaterialTheme.typography.titleSmall)
                    }
                    items(children.take(50)) { child ->
                        Card(modifier = Modifier.fillMaxWidth(), onClick = { onNavigateToEntity(child.countryCode, child.id) }) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text(child.canonicalName, style = MaterialTheme.typography.titleSmall)
                                Text("${child.id} — ${child.entityType}", style = MaterialTheme.typography.labelSmall)
                            }
                        }
                    }
                }
                1 -> {
                    if (aliases.isEmpty()) {
                        item { Text("لا توجد أسماء بديلة — طبيعي", modifier = Modifier.padding(8.dp)) }
                    } else {
                        items(aliases) { alias ->
                            Card(modifier = Modifier.fillMaxWidth()) {
                                Column(modifier = Modifier.padding(12.dp)) {
                                    Text(alias.name, style = MaterialTheme.typography.titleSmall)
                                    Text("${alias.id} — language: ${alias.language} — script: ${alias.script} — kind: ${alias.kind} — status: ${alias.status}", style = MaterialTheme.typography.labelSmall)
                                    Text("valid: ${alias.validFrom ?: "—"} → ${alias.validTo ?: "—"} — source: ${alias.sourceId} — locator: ${alias.sourceLocator}", style = MaterialTheme.typography.bodySmall)
                                }
                            }
                        }
                    }
                }
                2 -> {
                    if (claims.isEmpty()) {
                        item { Text("لا توجد Claims — طبيعي للكيانات الإدارية الصرفة", modifier = Modifier.padding(8.dp)) }
                    } else {
                        items(claims) { claim ->
                            Card(modifier = Modifier.fillMaxWidth(), colors = if (claim.status == "disputed") CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer) else CardDefaults.cardColors()) {
                                Column(modifier = Modifier.padding(12.dp)) {
                                    Text("${claim.predicate} — ${claim.valueType}: ${claim.valueDataJson.take(200)}", style = MaterialTheme.typography.titleSmall)
                                    Text("${claim.id} — ${claim.status} — ${claim.classification} — ${claim.confidence} — ${claim.verificationStatus}", style = MaterialTheme.typography.labelSmall)
                                    Text("source: ${claim.sourceId} — locator: ${claim.sourceLocator} — second: ${claim.secondSourceId ?: "—"}", style = MaterialTheme.typography.bodySmall)
                                    claim.lexicalContextJson?.let {
                                        Text("lexical_context: ${it.take(200)}", style = MaterialTheme.typography.bodySmall)
                                    }
                                }
                            }
                        }
                    }
                }
                3 -> {
                    items(relationships) { rel ->
                        Card(modifier = Modifier.fillMaxWidth(), colors = if (rel.relationshipType == "boundary_intersects") CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer) else CardDefaults.cardColors()) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text("${rel.relationshipType} — ${rel.status}", style = MaterialTheme.typography.titleSmall)
                                Text("${rel.id}: ${rel.childId} → ${rel.parentId}", style = MaterialTheme.typography.labelSmall)
                                Text("valid: ${rel.validFrom ?: "—"}→${rel.validTo ?: "—"} — confidence: ${rel.confidence}", style = MaterialTheme.typography.bodySmall)
                                Text("source: ${rel.sourceId} — locator: ${rel.sourceLocator}", style = MaterialTheme.typography.bodySmall)
                                if (rel.relationshipType == "boundary_intersects") {
                                    Text("تنبيه: تقاطع حدودي وليس والد إداري", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.primary)
                                }
                            }
                        }
                    }
                }
                4 -> {
                    items(sources) { src ->
                        Card(modifier = Modifier.fillMaxWidth()) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text(src.title, style = MaterialTheme.typography.titleSmall)
                                Text("${src.id} — ${src.qualityTier} — ${src.sourceType}", style = MaterialTheme.typography.labelSmall)
                                Text("license: ${src.license?.take(100) ?: "—"}", style = MaterialTheme.typography.bodySmall)
                                Text("url: ${src.url ?: "—"} — archive: ${src.archiveUrl ?: "—"}", style = MaterialTheme.typography.bodySmall)
                                Text("locator: ${src.locator ?: "—"} — checksum: ${src.checksum?.take(16) ?: "—"}", style = MaterialTheme.typography.labelSmall)
                            }
                        }
                    }
                }
                5 -> {
                    item {
                        if (ent.latitude != null) {
                            Card(modifier = Modifier.fillMaxWidth()) {
                                Column(modifier = Modifier.padding(12.dp)) {
                                    Text("الإحداثيات الموثقة", style = MaterialTheme.typography.titleSmall)
                                    Text("${ent.latitude}, ${ent.longitude}", style = MaterialTheme.typography.bodySmall)
                                    Text("افتح في OpenStreetMap يتطلب إنترنت", style = MaterialTheme.typography.labelSmall)
                                }
                            }
                        } else {
                            Card(modifier = Modifier.fillMaxWidth()) {
                                Column(modifier = Modifier.padding(12.dp)) {
                                    Text("لا توجد إحداثيات موثقة لهذا الكيان في هذه اللقطة", style = MaterialTheme.typography.titleSmall)
                                    Text("حسب schema_v2.md: الإحداثيات اختيارية لا تخمينية — لا نعرض موقعاً وهمياً", style = MaterialTheme.typography.bodySmall)
                                }
                            }
                        }
                    }
                }
                6 -> {
                    item {
                        Card(modifier = Modifier.fillMaxWidth()) {
                            Column(modifier = Modifier.padding(12.dp)) {
                                Text("Entity Raw JSON — كل الحقول محفوظة", style = MaterialTheme.typography.titleSmall)
                                Text(ent.rawJson.take(2000), style = MaterialTheme.typography.bodySmall)
                            }
                        }
                    }
                }
            }
        }
    }
}
