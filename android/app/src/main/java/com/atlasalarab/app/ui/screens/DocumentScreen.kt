package com.atlasalarab.app.ui.screens

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.produceState
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.ProjectDocument
import com.atlasalarab.app.ui.ArabicLabels
import com.atlasalarab.app.ui.components.ErrorPane
import com.atlasalarab.app.ui.components.LoadState
import com.atlasalarab.app.ui.components.LoadingPane
import com.atlasalarab.app.ui.components.SectionTitle
import org.json.JSONObject

@Composable
fun DocumentScreen(id: String, repository: AtlasRepository, modifier: Modifier = Modifier) {
    val state = produceState<LoadState<ProjectDocument?>>(LoadState.Loading, id, repository) {
        value = try { LoadState.Ready(repository.document(id)) }
        catch (error: Exception) { LoadState.Failed(error.message ?: "خطأ غير معروف") }
    }.value
    when (state) {
        LoadState.Loading -> LoadingPane(modifier)
        is LoadState.Failed -> ErrorPane(state.message, modifier)
        is LoadState.Ready -> state.value?.let { DocumentContent(it, modifier) } ?: ErrorPane("لم نجد الوثيقة المطلوبة", modifier)
    }
}

@Composable
private fun DocumentContent(document: ProjectDocument, modifier: Modifier) {
    val formatted = if (document.contentType == "application/json") {
        runCatching { JSONObject(document.content).toString(2) }.getOrDefault(document.content)
    } else document.content
    Column(modifier.fillMaxSize().padding(PaddingValues(18.dp))) {
        SectionTitle(document.title, ArabicLabels.documentKind(document.kind))
        Text(
            "هذه وثيقة تقنية أصلية محفوظة داخل قاعدة التطبيق دون اختصار.",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
            modifier = Modifier.padding(vertical = 12.dp),
        )
        CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Ltr) {
            SelectionContainer {
                Text(
                    formatted,
                    modifier = Modifier
                        .weight(1f)
                        .verticalScroll(rememberScrollState())
                        .horizontalScroll(rememberScrollState()),
                    fontFamily = FontFamily.Monospace,
                    style = MaterialTheme.typography.bodyMedium,
                )
            }
        }
    }
}
