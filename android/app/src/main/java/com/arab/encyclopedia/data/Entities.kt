package com.arab.encyclopedia.data

import androidx.room.Entity
import androidx.room.PrimaryKey
import androidx.room.TypeConverters
import androidx.room.Converters

/**
 * DATA_CONTRACT — 100% field preservation
 * Every field from Release Dataset is preserved, even if not displayed in Explorer Mode.
 * rawJson column is the ultimate guarantee.
 */

@Entity(tableName = "entities")
data class EntityRoom(
    @PrimaryKey val id: String, // ENT-...
    val canonicalName: String,
    val canonicalNameLanguage: String,
    val canonicalSourceId: String,
    val sourceLocator: String,
    val countryCode: String,
    val entityType: String,
    val status: String,
    val validFrom: String?,
    val validTo: String?,
    val latitude: Double?,
    val longitude: Double?,
    val confidence: String,
    val verificationStatus: String,
    val legacyIdsJson: String, // JSON array string
    val notes: String?,
    val schemaVersion: String,
    val rawJson: String // Full original JSON - 100% preservation guarantee
)

@Entity(tableName = "aliases")
data class AliasRoom(
    @PrimaryKey val id: String,
    val entityId: String,
    val name: String,
    val language: String?,
    val script: String?,
    val kind: String,
    val status: String,
    val validFrom: String?,
    val validTo: String?,
    val sourceId: String,
    val sourceLocator: String,
    val schemaVersion: String,
    val rawJson: String
)

@Entity(tableName = "relationships")
data class RelationshipRoom(
    @PrimaryKey val id: String,
    val childId: String,
    val parentId: String,
    val relationshipType: String,
    val status: String,
    val validFrom: String?,
    val validTo: String?,
    val confidence: String,
    val verificationStatus: String,
    val sourceId: String,
    val sourceLocator: String,
    val notes: String?,
    val schemaVersion: String,
    val rawJson: String
)

@Entity(tableName = "claims")
data class ClaimRoom(
    @PrimaryKey val id: String,
    val subjectId: String,
    val predicate: String,
    val valueType: String,
    val valueDataJson: String, // JSON string of value.data
    val classification: String,
    val status: String,
    val confidence: String,
    val verificationStatus: String,
    val sensitivity: String,
    val published: Boolean,
    val observedAt: String?,
    val validFrom: String?,
    val validTo: String?,
    val sourceId: String,
    val sourceLocator: String,
    val secondSourceId: String?,
    val secondSourceLocator: String?,
    val unit: String?,
    val lexicalContextJson: String?, // JSON of lexical_context or null
    val notes: String?,
    val schemaVersion: String,
    val rawJson: String
)

@Entity(tableName = "sources")
data class SourceRoom(
    @PrimaryKey val id: String,
    val title: String,
    val publisher: String?,
    val author: String?,
    val organization: String?,
    val countryCodesJson: String, // JSON array
    val url: String?,
    val archiveUrl: String?,
    val publicationDate: String?,
    val retrievedAt: String?,
    val language: String?,
    val license: String?,
    val qualityTier: String,
    val sourceType: String,
    val checksum: String?,
    val locator: String?,
    val notes: String?,
    val schemaVersion: String,
    val rawJson: String
)

@Entity(tableName = "denominators")
data class DenominatorRoom(
    @PrimaryKey val id: String,
    val countryCode: String,
    val layer: String,
    val definition: String,
    val denominator: Int,
    val asOf: String?,
    val snapshotDate: String?,
    val sourceId: String,
    val sourceLocator: String,
    val status: String,
    val license: String?,
    val missingReason: String?,
    val notes: String?,
    val value: Int,
    val schemaVersion: String,
    val rawJson: String
)

@Entity(tableName = "coverage")
data class CoverageRoom(
    @PrimaryKey val id: String,
    val countryCode: String,
    val layer: String,
    val denominatorId: String,
    val denominator: Int?,
    val matched: Int,
    val unmatched: Int,
    val excluded: Int,
    val exclusionReasonsJson: String,
    val missing: Int?,
    val missingReason: String?,
    val coveragePercentage: Double?,
    val complete: Boolean,
    val snapshotId: String,
    val snapshotDate: String?,
    val sourceId: String,
    val license: String?,
    val notes: String?,
    val schemaVersion: String,
    val rawJson: String
)

@Entity(tableName = "snapshots")
data class SnapshotRoom(
    @PrimaryKey val id: String,
    val title: String,
    val capturedAt: String,
    val sourceId: String,
    val scope: String,
    val method: String,
    val checksum: String?,
    val notes: String?,
    val schemaVersion: String,
    val rawJson: String
)

@Entity(tableName = "manifests")
data class ManifestRoom(
    @PrimaryKey val iso2: String,
    val filename: String,
    val rawJson: String
)

// For FTS search - alias-aware
@Entity(tableName = "search_index")
data class SearchIndexRoom(
    @PrimaryKey val entityId: String,
    val canonicalName: String,
    val normalizedName: String,
    val countryCode: String,
    val entityType: String,
    val status: String,
    val aliasesConcatenated: String, // all alias names joined
    val normalizedAliases: String
)
