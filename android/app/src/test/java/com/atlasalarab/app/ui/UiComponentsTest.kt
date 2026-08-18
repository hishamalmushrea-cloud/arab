package com.atlasalarab.app.ui

import androidx.compose.ui.semantics.SemanticsProperties
import androidx.compose.ui.test.SemanticsMatcher
import androidx.compose.ui.test.assertHasClickAction
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import com.atlasalarab.app.data.CountrySummary
import com.atlasalarab.app.data.LibraryDocumentSummary
import com.atlasalarab.app.ui.components.ContentBadge
import com.atlasalarab.app.ui.components.ContentKind
import com.atlasalarab.app.ui.components.CountryCard
import com.atlasalarab.app.ui.components.LibraryDocumentRow
import com.atlasalarab.app.ui.components.MarkdownBlock
import com.atlasalarab.app.ui.components.MarkdownBlockView
import com.atlasalarab.app.ui.components.SectionTitle
import com.atlasalarab.app.ui.theme.AtlasTheme
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import org.robolectric.annotation.GraphicsMode

@RunWith(RobolectricTestRunner::class)
@GraphicsMode(GraphicsMode.Mode.NATIVE)
@Config(sdk = [35])
class UiComponentsTest {
    @get:Rule
    val compose = createComposeRule()

    @Test
    fun sectionTitle_isExposedAsAccessibleHeading() {
        compose.setContent { AtlasTheme { SectionTitle("المعلومات الموثقة", "تفاصيل مرتبطة بالمصدر") } }

        compose.onNodeWithText("المعلومات الموثقة").assertIsDisplayed()
        compose.onNode(SemanticsMatcher.keyIsDefined(SemanticsProperties.Heading)).assertIsDisplayed()
    }

    @Test
    fun contentBadge_explainsEncyclopedicMaterialToTalkBack() {
        compose.setContent { AtlasTheme { ContentBadge(ContentKind.Encyclopedic) } }

        compose.onNodeWithContentDescription(
            "مادة موسوعية. مادة مرجعية من ملفات الموسوعة وقد تتضمن فجوات أو تقديرات",
        ).assertIsDisplayed()
    }

    @Test
    fun countryCard_displaysMetricsAndHasClickAction() {
        val country = CountrySummary(
            code = "JO", nameAr = "الأردن", nameEn = "Jordan",
            entityCount = 134, aliasCount = 40, relationshipCount = 90,
            claimCount = 25, sourceCount = 12, coverageCount = 8, completeLayers = 6,
        )
        compose.setContent { AtlasTheme { CountryCard(country, onClick = {}) } }

        compose.onNodeWithText("الأردن").assertIsDisplayed()
        compose.onNodeWithText("كيان", substring = true).assertIsDisplayed()
        compose.onNodeWithText("مصدر", substring = true).assertIsDisplayed()
        compose.onNodeWithText("الأردن").assertHasClickAction()
    }

    @Test
    fun libraryRow_presentsReadableMetadataWithoutTechnicalPath() {
        val document = LibraryDocumentSummary(
            id = "LIB-JO-ECONOMY", collection = "الدول", countryCode = "JO",
            countryName = "الأردن", category = "الاقتصاد",
            title = "المملكة الأردنية الهاشمية — الاقتصاد والعمل",
            relativePath = "الدول/الأردن/الاقتصاد.md", fileType = "markdown", byteSize = 4233,
        )
        compose.setContent { AtlasTheme { LibraryDocumentRow(document, onClick = {}) } }

        compose.onNodeWithText(document.title).assertIsDisplayed().assertHasClickAction()
        compose.onNodeWithText("الأردن  •  الاقتصاد").assertIsDisplayed()
    }

    @Test
    fun markdownTable_rendersCellsAndOpensEmbeddedLink() {
        var opened = ""
        val table = MarkdownBlock.Table(
            listOf(
                "| المدينة | الملف |",
                "|---|---|",
                "| إربد | [فتح ملف إربد](المدن/إربد/إربد.md) |",
            ),
        )
        compose.setContent {
            AtlasTheme {
                MarkdownBlockView(table, onLinkClick = { opened = it })
            }
        }

        compose.onNodeWithText("المدينة").assertIsDisplayed()
        compose.onNodeWithText("إربد").assertIsDisplayed()
        compose.onNodeWithText("فتح ملف إربد").assertIsDisplayed().performClick()
        compose.runOnIdle { assertEquals("المدن/إربد/إربد.md", opened) }
    }
}
