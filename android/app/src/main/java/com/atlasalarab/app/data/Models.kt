package com.atlasalarab.app.data

data class ProjectStats(
    val countries: Int,
    val entities: Int,
    val aliases: Int,
    val relationships: Int,
    val claims: Int,
    val sources: Int,
    val snapshots: Int,
    val coverageRecords: Int,
    val schemaVersion: String,
    val datasetVersion: String,
    val asOf: String,
    val notice: String,
    val libraryDocuments: Int,
    val libraryBytes: Long,
    val libraryCollections: Int,
    val libraryNotice: String,
)

data class CountrySummary(
    val code: String,
    val nameAr: String,
    val nameEn: String,
    val entityCount: Int,
    val aliasCount: Int,
    val relationshipCount: Int,
    val claimCount: Int,
    val sourceCount: Int,
    val coverageCount: Int,
    val completeLayers: Int,
)

data class EntityTypeCount(
    val type: String,
    val count: Int,
)

data class EntitySummary(
    val id: String,
    val countryCode: String,
    val countryName: String,
    val name: String,
    val type: String,
    val status: String,
    val confidence: String?,
    val verificationStatus: String?,
)

data class SearchResult(
    val entity: EntitySummary,
    val matchedName: String,
    val matchedLanguage: String,
    val canonicalMatch: Boolean,
)

data class CoverageItem(
    val id: String,
    val layer: String,
    val definition: String,
    val denominator: Int?,
    val matched: Int,
    val unmatched: Int,
    val excluded: Int,
    val missing: Int?,
    val percentage: Double?,
    val complete: Boolean,
    val snapshotDate: String?,
    val sourceId: String,
    val missingReason: String?,
)

data class AliasItem(
    val name: String,
    val language: String,
    val kind: String,
    val status: String,
    val sourceId: String,
)

data class ClaimItem(
    val id: String,
    val predicate: String,
    val value: String,
    val unit: String?,
    val classification: String?,
    val confidence: String?,
    val status: String,
    val sourceId: String,
    val sourceTitle: String,
    val sourceLocator: String,
    val observedAt: String?,
)

data class RelatedEntity(
    val relationshipId: String,
    val relationshipType: String,
    val direction: RelationDirection,
    val entity: EntitySummary,
    val status: String,
    val sourceId: String,
)

enum class RelationDirection { Parent, Child }

data class EntityDetails(
    val entity: EntitySummary,
    val canonicalNameLanguage: String,
    val canonicalSourceId: String,
    val canonicalSourceTitle: String,
    val sourceLocator: String,
    val coordinatesJson: String?,
    val notes: String?,
    val validFrom: String?,
    val validTo: String?,
    val aliases: List<AliasItem>,
    val claims: List<ClaimItem>,
    val relations: List<RelatedEntity>,
)

data class SourceItem(
    val id: String,
    val title: String,
    val publisher: String,
    val organization: String?,
    val author: String?,
    val sourceType: String,
    val url: String,
    val archiveUrl: String?,
    val publicationDate: String?,
    val retrievedAt: String,
    val license: String,
    val language: String,
    val qualityTier: String,
    val locator: String,
    val notes: String?,
)

data class ProjectDocument(
    val id: String,
    val countryCode: String?,
    val kind: String,
    val title: String,
    val contentType: String,
    val content: String,
)

data class CountryDetails(
    val country: CountrySummary,
    val typeCounts: List<EntityTypeCount>,
    val coverage: List<CoverageItem>,
    val entities: List<EntitySummary>,
    val sources: List<SourceItem>,
    val documents: List<ProjectDocument>,
    val libraryDocumentCount: Int,
)

data class LibraryCollectionCount(
    val collection: String,
    val count: Int,
)

data class LibraryCategoryCount(
    val category: String,
    val count: Int,
)

data class LibraryDocumentSummary(
    val id: String,
    val collection: String,
    val countryCode: String?,
    val countryName: String?,
    val category: String,
    val title: String,
    val relativePath: String,
    val fileType: String,
    val byteSize: Int,
)

data class LibraryDocument(
    val summary: LibraryDocumentSummary,
    val content: String,
    val contentSha256: String,
)

data class LibraryOverview(
    val totalCount: Int,
    val totalBytes: Long,
    val collections: List<LibraryCollectionCount>,
    val categories: List<LibraryCategoryCount>,
    val documents: List<LibraryDocumentSummary>,
)
