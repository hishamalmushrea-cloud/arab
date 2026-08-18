package com.atlasalarab.app.ui.screens

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ContentCopy
import androidx.compose.material.icons.filled.Link
import androidx.compose.material.icons.filled.Source
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.FilledTonalButton
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.produceState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.EntityDetails
import com.atlasalarab.app.data.RelationDirection
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.ContentBadge
import com.atlasalarab.app.ui.components.ContentKind
import com.atlasalarab.app.ui.components.EntityRow
import com.atlasalarab.app.ui.components.ErrorPane
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.LoadingPane
import com.atlasalarab.app.ui.components.SectionTitle
import com.atlasalarab.app.ui.components.StatusPill

@Composable
fun EntityScreen(
    id: String,
    repository: AtlasRepository,
    onOpenEntity: (String) -> Unit,
    onOpenSource: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    val state = produceState<LoadState<EntityDetails?>>(LoadState.Loading, id, repository) {
        value = try { LoadState.Ready(repository.entityDetails(id)) }
        catch (error: Exception) { LoadState.Failed(error.message ?: "خطأ غير معروف") }
    }.value
    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> state.value?.let {
            EntityContent(it, onOpenEntity, onOpenSource, modifier)
        } ?: ErrorPane("لم نجد الكيان المطلوب", modifier)
    }
}

@Composable
private fun EntityContent(
    details: EntityDetails,
    onOpenEntity: (String) -> Unit,
    onOpenSource: (String) -> Unit,
    modifier: Modifier,
) {
    val clipboard = LocalClipboardManager.current
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
                Column(Modifier.fillMaxWidth().padding(22.dp)) {
                    Text("${ArabicLabels.flag(details.entity.countryCode)} ${details.entity.countryName}", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.height(7.dp))
                    Text(details.entity.name, style = MaterialTheme.typography.headlineMedium)
                    Spacer(Modifier.height(6.dp))
                    Text(ArabicLabels.entityType(details.entity.type), style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.height(12.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                        StatusPill(details.entity.status)
                        ContentBadge(
                            if (details.entity.status == "historical") ContentKind.Historical else ContentKind.Authoritative,
                            compact = true,
                        )
                    }
                }
            }
        }

        item {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(9.dp)) {
                EntityMetric("معلومة", details.claims.size, Modifier.weight(1f))
                EntityMetric("اسم بديل", details.aliases.size, Modifier.weight(1f))
                EntityMetric("علاقة", details.relations.size, Modifier.weight(1f))
            }
        }

        if (details.relations.isNotEmpty()) {
            item { SectionTitle("الموقع والعلاقات", "التسلسل الإداري والعلاقات الموثقة للمكان") }
            items(details.relations, key = { it.relationshipId }) { relation ->
                val direction = if (relation.direction == RelationDirection.Parent) "يتبع" else "يتبع له"
                EntityRow(
                    relation.entity,
                    onClick = { onOpenEntity(relation.entity.id) },
                    secondary = "$direction • ${ArabicLabels.relationship(relation.relationshipType)}",
                )
            }
        }

        if (details.aliases.isNotEmpty()) {
            item { SectionTitle("الأسماء البديلة", "أسماء رسمية ومحلية وتاريخية تشير إلى الكيان نفسه") }
            item {
                LazyRow(horizontalArrangement = Arrangement.spacedBy(9.dp)) {
                    items(details.aliases, key = { "${it.name}-${it.language}-${it.kind}" }) { alias ->
                        Surface(shape = RoundedCornerShape(15.dp), color = MaterialTheme.colorScheme.secondaryContainer) {
                            Column(Modifier.padding(horizontal = 15.dp, vertical = 11.dp)) {
                                Text(alias.name, style = MaterialTheme.typography.titleMedium)
                                Text("${alias.language} • ${ArabicLabels.status(alias.status)}", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                }
            }
        }

        if (details.claims.isNotEmpty()) {
            item { SectionTitle("المعلومات الموثّقة", "كل معلومة مرتبطة بمصدر ومحدد داخله") }
            items(details.claims, key = { it.id }) { claim ->
                Card(
                    shape = RoundedCornerShape(18.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                ) {
                    Column(Modifier.padding(17.dp)) {
                        Text(ArabicLabels.predicate(claim.predicate), style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                        Spacer(Modifier.height(7.dp))
                        Text(
                            buildString {
                                append(claim.value)
                                claim.unit?.let { append(" ").append(it) }
                            },
                            style = MaterialTheme.typography.titleMedium,
                        )
                        if (claim.classification != null || claim.confidence != null) {
                            Spacer(Modifier.height(9.dp))
                            Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                                claim.classification?.let { ClaimBadge(ArabicLabels.classification(it)) }
                                claim.confidence?.let { ClaimBadge(ArabicLabels.status(it)) }
                            }
                        }
                        Spacer(Modifier.height(10.dp))
                        HorizontalDivider()
                        Spacer(Modifier.height(9.dp))
                        Text(claim.sourceTitle, style = MaterialTheme.typography.bodyMedium, maxLines = 2, overflow = TextOverflow.Ellipsis)
                        Text(claim.sourceLocator, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, maxLines = 2, overflow = TextOverflow.Ellipsis)
                        TextButton(onClick = { onOpenSource(claim.sourceId) }) {
                            Icon(Icons.Default.Source, null)
                            Spacer(Modifier.width(6.dp))
                            Text("فتح المصدر")
                        }
                    }
                }
            }
        }

        item { SectionTitle("المصدر المرجعي", "المصدر الذي يثبت وجود الكيان واسمه الأساسي") }
        item {
            Card(
                onClick = { onOpenSource(details.canonicalSourceId) },
                shape = RoundedCornerShape(18.dp),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
            ) {
                Column(Modifier.fillMaxWidth().padding(17.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Link, null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(Modifier.width(9.dp))
                        Text(details.canonicalSourceTitle, style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
                    }
                    Spacer(Modifier.height(8.dp))
                    Text(details.sourceLocator, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }

        if (details.validFrom != null || details.validTo != null || details.coordinatesJson != null || details.notes != null) {
            item { SectionTitle("تفاصيل إضافية") }
            item {
                Card(
                    shape = RoundedCornerShape(18.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
                ) {
                    Column(Modifier.padding(17.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        details.validFrom?.let { DetailLine("صالح من", it) }
                        details.validTo?.let { DetailLine("صالح إلى", it) }
                        details.coordinatesJson?.let { DetailLine("الإحداثيات", it) }
                        details.notes?.let { DetailLine("ملاحظات التوثيق", it) }
                    }
                }
            }
        }

        item {
            Surface(shape = RoundedCornerShape(15.dp), color = MaterialTheme.colorScheme.surfaceVariant) {
                Column(Modifier.fillMaxWidth().padding(14.dp)) {
                    Text("المعرّف التقني الدائم", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    SelectionContainer {
                        Text(details.entity.id, fontFamily = FontFamily.Monospace, style = MaterialTheme.typography.bodySmall)
                    }
                    TextButton(onClick = { clipboard.setText(AnnotatedString(details.entity.id)) }) {
                        Icon(Icons.Default.ContentCopy, null)
                        Spacer(Modifier.width(6.dp))
                        Text("نسخ المعرّف")
                    }
                }
            }
        }
    }
}

@Composable
private fun ClaimBadge(text: String) {
    Surface(shape = RoundedCornerShape(8.dp), color = MaterialTheme.colorScheme.primaryContainer) {
        Text(
            text,
            Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onPrimaryContainer,
        )
    }
}

@Composable
private fun EntityMetric(label: String, value: Int, modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier,
        shape = RoundedCornerShape(15.dp),
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Column(Modifier.padding(horizontal = 9.dp, vertical = 12.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(ArabicLabels.number(value), style = MaterialTheme.typography.titleLarge, color = MaterialTheme.colorScheme.primary)
            Text(label, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

@Composable
private fun DetailLine(label: String, value: String) {
    Column {
        Text(label, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
        Text(value, style = MaterialTheme.typography.bodyMedium)
    }
}
