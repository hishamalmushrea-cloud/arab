package com.atlasalarab.app.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.ClickableText
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.semantics.heading
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.dp

sealed interface MarkdownBlock {
    data class Heading(val level: Int, val text: String) : MarkdownBlock
    data class Paragraph(val text: String) : MarkdownBlock
    data class Quote(val text: String) : MarkdownBlock
    data class Bullet(val text: String, val depth: Int, val numbered: Boolean) : MarkdownBlock
    data class Table(val lines: List<String>) : MarkdownBlock
    data class Code(val text: String) : MarkdownBlock
    data object Divider : MarkdownBlock
}

fun parseMarkdown(content: String): List<MarkdownBlock> {
    val lines = content.replace("\r\n", "\n").split('\n')
    val blocks = mutableListOf<MarkdownBlock>()
    val paragraph = mutableListOf<String>()
    var index = 0

    fun flushParagraph() {
        if (paragraph.isNotEmpty()) {
            blocks += MarkdownBlock.Paragraph(paragraph.joinToString(" ").trim())
            paragraph.clear()
        }
    }

    while (index < lines.size) {
        val line = lines[index]
        val trimmed = line.trim()
        when {
            trimmed.isEmpty() -> flushParagraph()
            trimmed.startsWith("```") -> {
                flushParagraph()
                val code = mutableListOf<String>()
                index++
                while (index < lines.size && !lines[index].trim().startsWith("```")) {
                    code += lines[index]
                    index++
                }
                blocks += MarkdownBlock.Code(code.joinToString("\n"))
            }
            trimmed.matches(Regex("^#{1,6}\\s+.+")) -> {
                flushParagraph()
                val level = trimmed.takeWhile { it == '#' }.length
                blocks += MarkdownBlock.Heading(level, trimmed.drop(level).trim())
            }
            trimmed.matches(Regex("^[-*_]{3,}$")) -> {
                flushParagraph()
                blocks += MarkdownBlock.Divider
            }
            trimmed.startsWith("|") && trimmed.endsWith("|") -> {
                flushParagraph()
                val table = mutableListOf<String>()
                while (index < lines.size) {
                    val candidate = lines[index].trim()
                    if (!candidate.startsWith("|") || !candidate.endsWith("|")) break
                    table += candidate
                    index++
                }
                blocks += MarkdownBlock.Table(table)
                index--
            }
            trimmed.startsWith(">") -> {
                flushParagraph()
                val quote = mutableListOf<String>()
                while (index < lines.size && lines[index].trim().startsWith(">")) {
                    quote += lines[index].trim().removePrefix(">").trim()
                    index++
                }
                blocks += MarkdownBlock.Quote(quote.joinToString("\n"))
                index--
            }
            line.matches(Regex("^\\s*[-*+]\\s+.+")) -> {
                flushParagraph()
                val depth = line.takeWhile { it.isWhitespace() }.length / 2
                blocks += MarkdownBlock.Bullet(line.trimStart().drop(2).trim(), depth, false)
            }
            line.matches(Regex("^\\s*\\d+[.)]\\s+.+")) -> {
                flushParagraph()
                val depth = line.takeWhile { it.isWhitespace() }.length / 2
                val text = line.trimStart().replaceFirst(Regex("^\\d+[.)]\\s+"), "")
                blocks += MarkdownBlock.Bullet(text, depth, true)
            }
            else -> paragraph += trimmed
        }
        index++
    }
    flushParagraph()
    return blocks
}

fun markdownBlockText(block: MarkdownBlock): String = when (block) {
    is MarkdownBlock.Heading -> block.text
    is MarkdownBlock.Paragraph -> block.text
    is MarkdownBlock.Quote -> block.text
    is MarkdownBlock.Bullet -> block.text
    is MarkdownBlock.Table -> block.lines.joinToString(" ")
    is MarkdownBlock.Code -> block.text
    MarkdownBlock.Divider -> ""
}

@Composable
fun MarkdownBlockView(
    block: MarkdownBlock,
    modifier: Modifier = Modifier,
    highlightQuery: String = "",
    onLinkClick: (String) -> Unit = {},
) {
    when (block) {
        is MarkdownBlock.Heading -> RichMarkdownText(
            raw = block.text,
            modifier = modifier.fillMaxWidth().semantics { heading() }.padding(top = if (block.level <= 2) 12.dp else 6.dp),
            style = (when (block.level) {
                1 -> MaterialTheme.typography.headlineMedium
                2 -> MaterialTheme.typography.titleLarge
                else -> MaterialTheme.typography.titleMedium
            }).copy(
                color = if (block.level <= 2) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface,
                fontWeight = FontWeight.Bold,
            ),
            highlightQuery = highlightQuery,
            onLinkClick = onLinkClick,
        )
        is MarkdownBlock.Paragraph -> RichMarkdownText(
            raw = block.text,
            modifier = modifier.fillMaxWidth(),
            style = MaterialTheme.typography.bodyLarge.copy(color = MaterialTheme.colorScheme.onSurface),
            highlightQuery = highlightQuery,
            onLinkClick = onLinkClick,
        )
        is MarkdownBlock.Quote -> Surface(
            modifier = modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp),
            color = MaterialTheme.colorScheme.primaryContainer,
        ) {
            Row(Modifier.padding(13.dp), verticalAlignment = Alignment.Top) {
                Box(
                    Modifier
                        .width(4.dp)
                        .clip(RoundedCornerShape(4.dp))
                        .background(MaterialTheme.colorScheme.primary)
                        .padding(vertical = 18.dp),
                )
                Spacer(Modifier.width(10.dp))
                RichMarkdownText(
                    raw = block.text,
                    modifier = Modifier.weight(1f),
                    style = MaterialTheme.typography.bodyMedium.copy(color = MaterialTheme.colorScheme.onPrimaryContainer),
                    highlightQuery = highlightQuery,
                    onLinkClick = onLinkClick,
                )
            }
        }
        is MarkdownBlock.Bullet -> Row(
            modifier.fillMaxWidth().padding(start = (block.depth * 14).dp),
            verticalAlignment = Alignment.Top,
        ) {
            Text(if (block.numbered) "◈" else "•", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
            Spacer(Modifier.width(8.dp))
            RichMarkdownText(
                raw = block.text,
                modifier = Modifier.weight(1f),
                style = MaterialTheme.typography.bodyLarge.copy(color = MaterialTheme.colorScheme.onSurface),
                highlightQuery = highlightQuery,
                onLinkClick = onLinkClick,
            )
        }
        is MarkdownBlock.Table -> MarkdownTable(
            lines = block.lines,
            modifier = modifier,
            highlightQuery = highlightQuery,
            onLinkClick = onLinkClick,
        )
        is MarkdownBlock.Code -> Surface(
            modifier = modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp),
            color = MaterialTheme.colorScheme.surfaceVariant,
        ) {
            SelectionContainer {
                Text(
                    block.text,
                    Modifier.padding(12.dp).horizontalScroll(rememberScrollState()),
                    fontFamily = FontFamily.Monospace,
                    style = MaterialTheme.typography.bodyMedium,
                )
            }
        }
        MarkdownBlock.Divider -> HorizontalDivider(modifier.padding(vertical = 5.dp))
    }
}

@Composable
private fun MarkdownTable(
    lines: List<String>,
    modifier: Modifier,
    highlightQuery: String,
    onLinkClick: (String) -> Unit,
) {
    val rows = lines
        .filterNot { it.matches(Regex("^\\|[\\s:|\\-]+\\|$")) }
        .map { line -> line.trim().trim('|').split('|').map { it.trim() } }
    val columnCount = rows.maxOfOrNull { it.size } ?: 0
    Surface(
        modifier = modifier.fillMaxWidth(),
        shape = RoundedCornerShape(15.dp),
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outlineVariant),
    ) {
        Column(Modifier.horizontalScroll(rememberScrollState()).padding(vertical = 4.dp)) {
            rows.forEachIndexed { rowIndex, cells ->
                Row(
                    Modifier.background(
                        when {
                            rowIndex == 0 -> MaterialTheme.colorScheme.primaryContainer
                            rowIndex % 2 == 0 -> MaterialTheme.colorScheme.surfaceVariant.copy(alpha = .45f)
                            else -> MaterialTheme.colorScheme.surface
                        },
                    ),
                ) {
                    repeat(columnCount) { columnIndex ->
                        Box(Modifier.width(if (columnIndex == 0) 170.dp else 205.dp).padding(11.dp)) {
                            RichMarkdownText(
                                raw = cells.getOrElse(columnIndex) { "" },
                                modifier = Modifier.fillMaxWidth(),
                                style = (if (rowIndex == 0) MaterialTheme.typography.labelLarge else MaterialTheme.typography.bodyMedium).copy(
                                    color = if (rowIndex == 0) MaterialTheme.colorScheme.onPrimaryContainer else MaterialTheme.colorScheme.onSurface,
                                ),
                                highlightQuery = highlightQuery,
                                onLinkClick = onLinkClick,
                            )
                        }
                    }
                }
                if (rowIndex < rows.lastIndex) HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant)
            }
        }
    }
}

@Composable
private fun RichMarkdownText(
    raw: String,
    modifier: Modifier,
    style: TextStyle,
    highlightQuery: String,
    onLinkClick: (String) -> Unit,
) {
    val text = inlineMarkdown(raw, highlightQuery)
    val hasLinks = text.getStringAnnotations(LINK_TAG, 0, text.length).isNotEmpty()
    if (hasLinks) {
        ClickableText(
            text = text,
            modifier = modifier,
            style = style,
            onClick = { offset ->
                text.getStringAnnotations(LINK_TAG, offset, offset).firstOrNull()?.let { onLinkClick(it.item) }
            },
        )
    } else {
        SelectionContainer { Text(text = text, modifier = modifier, style = style) }
    }
}

fun inlineMarkdown(raw: String, highlightQuery: String = ""): AnnotatedString {
    val text = decodeEntities(raw)
    val token = Regex("(\\*\\*[^*]+\\*\\*|`[^`]+`|\\[[^\\]]+\\]\\([^)]+\\))")
    val formatted = buildAnnotatedString {
        var position = 0
        token.findAll(text).forEach { match ->
            append(text.substring(position, match.range.first))
            val value = match.value
            when {
                value.startsWith("**") -> {
                    val start = length
                    append(value.removePrefix("**").removeSuffix("**"))
                    addStyle(SpanStyle(fontWeight = FontWeight.Bold), start, length)
                }
                value.startsWith("`") -> {
                    val start = length
                    append(value.removeSurrounding("`"))
                    addStyle(
                        SpanStyle(
                            fontFamily = FontFamily.Monospace,
                            background = Color(0x1A087F70),
                            color = Color(0xFF087F70),
                        ),
                        start,
                        length,
                    )
                }
                value.startsWith("[") -> {
                    val label = value.substringAfter('[').substringBefore(']')
                    val target = value.substringAfter("](").removeSuffix(")")
                    val start = length
                    append(label)
                    addStyle(
                        SpanStyle(color = Color(0xFF087F70), textDecoration = TextDecoration.Underline),
                        start,
                        length,
                    )
                    addStringAnnotation(LINK_TAG, target, start, length)
                }
            }
            position = match.range.last + 1
        }
        append(text.substring(position))
    }
    if (highlightQuery.isBlank()) return formatted
    return buildAnnotatedString {
        append(formatted)
        val needle = highlightQuery.trim()
        val visibleText = formatted.text
        var start = visibleText.indexOf(needle, ignoreCase = true)
        while (start >= 0) {
            addStyle(
                SpanStyle(background = Color(0xFFFFD66B), color = Color(0xFF17282D)),
                start,
                (start + needle.length).coerceAtMost(length),
            )
            start = visibleText.indexOf(needle, start + needle.length, ignoreCase = true)
        }
    }
}

private fun decodeEntities(value: String): String = value
    .replace("&lt;", "<")
    .replace("&gt;", ">")
    .replace("&amp;", "&")
    .replace("&quot;", "\"")
    .replace("&#39;", "'")

private const val LINK_TAG = "markdown-link"
