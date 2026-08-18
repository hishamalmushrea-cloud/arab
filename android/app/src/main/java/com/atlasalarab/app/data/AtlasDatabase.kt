package com.atlasalarab.app.data

import android.content.Context
import android.database.Cursor
import android.database.sqlite.SQLiteDatabase
import com.atlasalarab.app.BuildConfig
import java.io.File

/** Read-only access to the complete, pre-packaged Schema 2.0.0 database. */
class AtlasDatabase(private val context: Context) {
    private val lock = Any()
    @Volatile private var database: SQLiteDatabase? = null

    private fun open(): SQLiteDatabase {
        database?.let { return it }
        synchronized(lock) {
            database?.let { return it }
            val target = context.getDatabasePath(DATABASE_NAME)
            val preferences = context.getSharedPreferences(PREFERENCES, Context.MODE_PRIVATE)
            val installedVersion = preferences.getString(DATA_VERSION_KEY, null)
            if (!target.exists() || installedVersion != BuildConfig.ATLAS_DATA_VERSION) {
                installBundledDatabase(target)
                preferences.edit().putString(DATA_VERSION_KEY, BuildConfig.ATLAS_DATA_VERSION).apply()
            }
            return SQLiteDatabase.openDatabase(
                target.absolutePath,
                null,
                SQLiteDatabase.OPEN_READONLY or SQLiteDatabase.NO_LOCALIZED_COLLATORS,
            ).also { database = it }
        }
    }

    private fun installBundledDatabase(target: File) {
        target.parentFile?.mkdirs()
        val temporary = File(target.parentFile, "$DATABASE_NAME.installing")
        if (temporary.exists()) temporary.delete()
        context.assets.open(ASSET_PATH).use { input ->
            temporary.outputStream().buffered().use { output -> input.copyTo(output) }
        }
        if (target.exists() && !target.delete()) {
            temporary.delete()
            error("تعذر استبدال قاعدة بيانات أطلس العرب")
        }
        if (!temporary.renameTo(target)) {
            temporary.delete()
            error("تعذر تثبيت قاعدة بيانات أطلس العرب")
        }
    }

    fun projectStats(): ProjectStats {
        val values = mutableMapOf<String, String>()
        open().rawQuery(
            "SELECT key,value FROM metadata WHERE key IN (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            arrayOf(
                "count.countries", "count.entities", "count.aliases", "count.relationships",
                "count.claims", "count.sources", "count.snapshots", "count.coverage",
                "schema_version", "dataset_version", "as_of", "notice_ar",
                "count.library_documents", "library_bytes", "library_collections", "library_notice_ar",
            ),
        ).use { cursor ->
            while (cursor.moveToNext()) values[cursor.string("key")] = cursor.string("value")
        }
        return ProjectStats(
            countries = values.getValue("count.countries").toInt(),
            entities = values.getValue("count.entities").toInt(),
            aliases = values.getValue("count.aliases").toInt(),
            relationships = values.getValue("count.relationships").toInt(),
            claims = values.getValue("count.claims").toInt(),
            sources = values.getValue("count.sources").toInt(),
            snapshots = values.getValue("count.snapshots").toInt(),
            coverageRecords = values.getValue("count.coverage").toInt(),
            schemaVersion = values.getValue("schema_version"),
            datasetVersion = values.getValue("dataset_version"),
            asOf = values.getValue("as_of"),
            notice = values.getValue("notice_ar"),
            libraryDocuments = values.getValue("count.library_documents").toInt(),
            libraryBytes = values.getValue("library_bytes").toLong(),
            libraryCollections = values.getValue("library_collections").toInt(),
            libraryNotice = values.getValue("library_notice_ar"),
        )
    }

    fun countries(): List<CountrySummary> = buildList {
        open().rawQuery(
            """SELECT * FROM countries ORDER BY name_ar""",
            null,
        ).use { cursor -> while (cursor.moveToNext()) add(cursor.country()) }
    }

    fun country(code: String): CountrySummary? = open().rawQuery(
        "SELECT * FROM countries WHERE code=?",
        arrayOf(code),
    ).use { cursor -> if (cursor.moveToFirst()) cursor.country() else null }

    fun countryDetails(code: String): CountryDetails? {
        val country = country(code) ?: return null
        return CountryDetails(
            country = country,
            typeCounts = entityTypeCounts(code),
            coverage = coverage(code),
            entities = entities(code),
            sources = sources(code),
            documents = documents(code),
            libraryDocumentCount = libraryDocumentCount(code),
        )
    }

    fun entityTypeCounts(countryCode: String): List<EntityTypeCount> = buildList {
        open().rawQuery(
            """SELECT entity_type, count(*) AS total FROM entities
               WHERE country_code=? GROUP BY entity_type ORDER BY total DESC, entity_type""",
            arrayOf(countryCode),
        ).use { cursor ->
            while (cursor.moveToNext()) add(EntityTypeCount(cursor.string("entity_type"), cursor.int("total")))
        }
    }

    fun entities(countryCode: String): List<EntitySummary> = buildList {
        open().rawQuery(
            """SELECT e.id,e.country_code,c.name_ar AS country_name,$PREFERRED_NAME_SQL AS entity_display_name,e.entity_type,
                      e.status,e.confidence,e.verification_status
               FROM entities e JOIN countries c ON c.code=e.country_code
               WHERE e.country_code=? ORDER BY e.canonical_name""",
            arrayOf(countryCode),
        ).use { cursor -> while (cursor.moveToNext()) add(cursor.entitySummary()) }
    }

    fun search(rawQuery: String, countryCode: String? = null, limit: Int = 80): List<SearchResult> {
        val query = normalizeArabic(rawQuery)
        if (query.length < 2) return emptyList()
        val countryClause = if (countryCode == null) "" else " AND s.country_code=?"
        val arguments = mutableListOf("%$query%")
        if (countryCode != null) arguments += countryCode
        arguments += query
        arguments += "$query%"
        arguments += (limit * 4).toString()
        val sql = """SELECT e.id,e.country_code,c.name_ar AS country_name,$PREFERRED_NAME_SQL AS entity_display_name,e.entity_type,
                            e.status,e.confidence,e.verification_status,s.display_name,s.language,s.is_canonical,
                            s.normalized_name
                     FROM search_index s
                     JOIN entities e ON e.id=s.entity_id
                     JOIN countries c ON c.code=e.country_code
                     WHERE s.normalized_name LIKE ?$countryClause
                     ORDER BY CASE WHEN s.normalized_name=? THEN 0
                                   WHEN s.normalized_name LIKE ? THEN 1 ELSE 2 END,
                              s.is_canonical DESC,e.canonical_name
                     LIMIT ?"""
        val deduplicated = linkedMapOf<String, SearchResult>()
        open().rawQuery(sql, arguments.toTypedArray()).use { cursor ->
            while (cursor.moveToNext() && deduplicated.size < limit) {
                val entity = cursor.entitySummary()
                deduplicated.putIfAbsent(
                    entity.id,
                    SearchResult(
                        entity = entity,
                        matchedName = cursor.string("display_name"),
                        matchedLanguage = cursor.string("language"),
                        canonicalMatch = cursor.int("is_canonical") == 1,
                    ),
                )
            }
        }
        return deduplicated.values.toList()
    }

    fun coverage(countryCode: String): List<CoverageItem> = buildList {
        open().rawQuery(
            """SELECT v.*,d.definition FROM coverage v
               JOIN denominators d ON d.id=v.denominator_id
               WHERE v.country_code=? ORDER BY v.complete DESC,v.layer""",
            arrayOf(countryCode),
        ).use { cursor ->
            while (cursor.moveToNext()) {
                add(
                    CoverageItem(
                        id = cursor.string("id"), layer = cursor.string("layer"),
                        definition = cursor.string("definition"), denominator = cursor.nullableInt("denominator"),
                        matched = cursor.int("matched"), unmatched = cursor.int("unmatched"),
                        excluded = cursor.int("excluded"), missing = cursor.nullableInt("missing"),
                        percentage = cursor.nullableDouble("coverage_percentage"),
                        complete = cursor.int("complete") == 1, snapshotDate = cursor.nullableString("snapshot_date"),
                        sourceId = cursor.string("source_id"), missingReason = cursor.nullableString("missing_reason"),
                    ),
                )
            }
        }
    }

    fun entityDetails(id: String): EntityDetails? {
        val base = open().rawQuery(
            """SELECT e.*,c.name_ar AS country_name,s.title AS source_title,$PREFERRED_NAME_SQL AS entity_display_name
               FROM entities e JOIN countries c ON c.code=e.country_code
               JOIN sources s ON s.id=e.canonical_source_id WHERE e.id=?""",
            arrayOf(id),
        ).use { cursor ->
            if (!cursor.moveToFirst()) return null
            EntityDetails(
                entity = cursor.entitySummary(),
                canonicalNameLanguage = cursor.string("canonical_name_language"),
                canonicalSourceId = cursor.string("canonical_source_id"),
                canonicalSourceTitle = cursor.string("source_title"),
                sourceLocator = cursor.string("source_locator"),
                coordinatesJson = cursor.nullableString("coordinates_json"),
                notes = cursor.nullableString("notes"),
                validFrom = cursor.nullableString("valid_from"),
                validTo = cursor.nullableString("valid_to"),
                aliases = emptyList(), claims = emptyList(), relations = emptyList(),
            )
        }
        return base.copy(
            aliases = aliases(id),
            claims = claims(id),
            relations = relations(id),
        )
    }

    private fun aliases(entityId: String): List<AliasItem> = buildList {
        open().rawQuery(
            "SELECT * FROM aliases WHERE entity_id=? ORDER BY language,name",
            arrayOf(entityId),
        ).use { cursor ->
            while (cursor.moveToNext()) add(
                AliasItem(
                    name = cursor.string("name"), language = cursor.string("language"),
                    kind = cursor.string("kind"), status = cursor.string("status"),
                    sourceId = cursor.string("source_id"),
                ),
            )
        }
    }

    private fun claims(entityId: String): List<ClaimItem> = buildList {
        open().rawQuery(
            """SELECT c.*,s.title AS source_title FROM claims c
               JOIN sources s ON s.id=c.source_id WHERE c.subject_id=?
               ORDER BY c.predicate,c.id""",
            arrayOf(entityId),
        ).use { cursor ->
            while (cursor.moveToNext()) add(
                ClaimItem(
                    id = cursor.string("id"), predicate = cursor.string("predicate"),
                    value = cursor.string("value_display"), unit = cursor.nullableString("unit"),
                    classification = cursor.nullableString("classification"), confidence = cursor.nullableString("confidence"),
                    status = cursor.string("status"), sourceId = cursor.string("source_id"),
                    sourceTitle = cursor.string("source_title"), sourceLocator = cursor.string("source_locator"),
                    observedAt = cursor.nullableString("observed_at"),
                ),
            )
        }
    }

    private fun relations(entityId: String): List<RelatedEntity> = buildList {
        val parentSql = """SELECT r.id AS relationship_id,r.relationship_type,r.status AS relationship_status,
                                  r.source_id,e.id,e.country_code,c.name_ar AS country_name,$PREFERRED_NAME_SQL AS entity_display_name,
                                  e.entity_type,e.status,e.confidence,e.verification_status
                           FROM relationships r JOIN entities e ON e.id=r.parent_id
                           JOIN countries c ON c.code=e.country_code WHERE r.child_id=?
                           ORDER BY e.canonical_name"""
        open().rawQuery(parentSql, arrayOf(entityId)).use { cursor ->
            while (cursor.moveToNext()) add(cursor.relatedEntity(RelationDirection.Parent))
        }
        val childSql = """SELECT r.id AS relationship_id,r.relationship_type,r.status AS relationship_status,
                                 r.source_id,e.id,e.country_code,c.name_ar AS country_name,$PREFERRED_NAME_SQL AS entity_display_name,
                                 e.entity_type,e.status,e.confidence,e.verification_status
                          FROM relationships r JOIN entities e ON e.id=r.child_id
                          JOIN countries c ON c.code=e.country_code WHERE r.parent_id=?
                          ORDER BY e.canonical_name"""
        open().rawQuery(childSql, arrayOf(entityId)).use { cursor ->
            while (cursor.moveToNext()) add(cursor.relatedEntity(RelationDirection.Child))
        }
    }

    fun sources(countryCode: String? = null): List<SourceItem> = buildList {
        val sql = if (countryCode == null) {
            "SELECT s.* FROM sources s ORDER BY s.quality_tier,s.title"
        } else {
            """SELECT s.* FROM sources s JOIN country_sources cs ON cs.source_id=s.id
               WHERE cs.country_code=? ORDER BY s.quality_tier,s.title"""
        }
        val args = countryCode?.let { arrayOf(it) }
        open().rawQuery(sql, args).use { cursor -> while (cursor.moveToNext()) add(cursor.source()) }
    }

    fun source(id: String): SourceItem? = open().rawQuery(
        "SELECT * FROM sources WHERE id=?",
        arrayOf(id),
    ).use { cursor -> if (cursor.moveToFirst()) cursor.source() else null }

    fun documents(countryCode: String? = null): List<ProjectDocument> = buildList {
        val sql = if (countryCode == null) {
            "SELECT * FROM project_documents ORDER BY country_code,kind"
        } else {
            "SELECT * FROM project_documents WHERE country_code=? ORDER BY kind"
        }
        open().rawQuery(sql, countryCode?.let { arrayOf(it) }).use { cursor ->
            while (cursor.moveToNext()) add(cursor.document())
        }
    }

    fun document(id: String): ProjectDocument? = open().rawQuery(
        "SELECT * FROM project_documents WHERE id=?",
        arrayOf(id),
    ).use { cursor -> if (cursor.moveToFirst()) cursor.document() else null }

    private fun libraryDocumentCount(countryCode: String): Int = open().rawQuery(
        "SELECT count(*) AS total FROM library_documents WHERE country_code=?",
        arrayOf(countryCode),
    ).use { cursor -> cursor.moveToFirst(); cursor.int("total") }

    fun libraryOverview(countryCode: String? = null): LibraryOverview {
        val where = if (countryCode == null) "" else " WHERE country_code=?"
        val arguments = countryCode?.let { arrayOf(it) }
        val totals = open().rawQuery(
            "SELECT count(*) AS total,coalesce(sum(byte_size),0) AS bytes FROM library_documents$where",
            arguments,
        ).use { cursor ->
            cursor.moveToFirst()
            cursor.int("total") to cursor.getLong(cursor.index("bytes"))
        }
        val collections = buildList {
            open().rawQuery(
                "SELECT collection,count(*) AS total FROM library_documents$where GROUP BY collection ORDER BY total DESC,collection",
                arguments,
            ).use { cursor ->
                while (cursor.moveToNext()) add(LibraryCollectionCount(cursor.string("collection"), cursor.int("total")))
            }
        }
        val categories = buildList {
            open().rawQuery(
                "SELECT category,count(*) AS total FROM library_documents$where GROUP BY category ORDER BY total DESC,category",
                arguments,
            ).use { cursor ->
                while (cursor.moveToNext()) add(LibraryCategoryCount(cursor.string("category"), cursor.int("total")))
            }
        }
        return LibraryOverview(
            totalCount = totals.first,
            totalBytes = totals.second,
            collections = collections,
            categories = categories,
            documents = librarySummaries(countryCode = countryCode),
        )
    }

    fun searchLibrary(
        rawQuery: String,
        countryCode: String? = null,
        collection: String? = null,
        category: String? = null,
        limit: Int = 250,
    ): List<LibraryDocumentSummary> {
        val query = normalizeArabic(rawQuery)
        if (query.length < 2) return emptyList()
        val clauses = mutableListOf("(l.normalized_title LIKE ? OR l.content LIKE ?)")
        val arguments = mutableListOf("%$query%", "%${rawQuery.trim()}%")
        if (countryCode != null) { clauses += "l.country_code=?"; arguments += countryCode }
        if (collection != null) { clauses += "l.collection=?"; arguments += collection }
        if (category != null) { clauses += "l.category=?"; arguments += category }
        arguments += query
        arguments += "$query%"
        arguments += limit.toString()
        val sql = """SELECT l.*,c.name_ar AS country_name FROM library_documents l
                     LEFT JOIN countries c ON c.code=l.country_code
                     WHERE ${clauses.joinToString(" AND ")}
                     ORDER BY CASE WHEN l.normalized_title=? THEN 0
                                   WHEN l.normalized_title LIKE ? THEN 1 ELSE 2 END,
                              l.title LIMIT ?"""
        return buildList {
            open().rawQuery(sql, arguments.toTypedArray()).use { cursor ->
                while (cursor.moveToNext()) add(cursor.librarySummary())
            }
        }
    }

    private fun librarySummaries(
        countryCode: String? = null,
        collection: String? = null,
        category: String? = null,
    ): List<LibraryDocumentSummary> {
        val clauses = mutableListOf<String>()
        val arguments = mutableListOf<String>()
        if (countryCode != null) { clauses += "l.country_code=?"; arguments += countryCode }
        if (collection != null) { clauses += "l.collection=?"; arguments += collection }
        if (category != null) { clauses += "l.category=?"; arguments += category }
        val where = if (clauses.isEmpty()) "" else " WHERE ${clauses.joinToString(" AND ")}"
        val sql = """SELECT l.*,c.name_ar AS country_name FROM library_documents l
                     LEFT JOIN countries c ON c.code=l.country_code$where
                     ORDER BY l.collection,l.category,l.title"""
        return buildList {
            open().rawQuery(sql, arguments.toTypedArray()).use { cursor ->
                while (cursor.moveToNext()) add(cursor.librarySummary())
            }
        }
    }

    fun libraryDocument(id: String): LibraryDocument? = open().rawQuery(
        """SELECT l.*,c.name_ar AS country_name FROM library_documents l
           LEFT JOIN countries c ON c.code=l.country_code WHERE l.id=?""",
        arrayOf(id),
    ).use { cursor ->
        if (!cursor.moveToFirst()) null
        else LibraryDocument(
            summary = cursor.librarySummary(),
            content = cursor.string("content"),
            contentSha256 = cursor.string("content_sha256"),
        )
    }

    fun libraryDocumentIdByPath(relativePath: String): String? {
        val clean = relativePath.trimEnd('/')
        return open().rawQuery(
            """SELECT id FROM library_documents
               WHERE relative_path=? OR relative_path=?
               ORDER BY CASE WHEN relative_path=? THEN 0 ELSE 1 END LIMIT 1""",
            arrayOf(clean, "$clean/README.md", clean),
        ).use { cursor -> if (cursor.moveToFirst()) cursor.string("id") else null }
    }

    fun close() = synchronized(lock) {
        database?.close()
        database = null
    }

    private fun Cursor.country() = CountrySummary(
        code = string("code"), nameAr = string("name_ar"), nameEn = string("name_en"),
        entityCount = int("entity_count"), aliasCount = int("alias_count"),
        relationshipCount = int("relationship_count"), claimCount = int("claim_count"),
        sourceCount = int("source_count"), coverageCount = int("coverage_count"),
        completeLayers = int("complete_layers"),
    )

    private fun Cursor.entitySummary() = EntitySummary(
        id = string("id"), countryCode = string("country_code"), countryName = string("country_name"),
        name = string("entity_display_name"), type = string("entity_type"), status = string("status"),
        confidence = nullableString("confidence"), verificationStatus = nullableString("verification_status"),
    )

    private fun Cursor.relatedEntity(direction: RelationDirection) = RelatedEntity(
        relationshipId = string("relationship_id"), relationshipType = string("relationship_type"),
        direction = direction, entity = entitySummary(), status = string("relationship_status"),
        sourceId = string("source_id"),
    )

    private fun Cursor.source() = SourceItem(
        id = string("id"), title = string("title"), publisher = string("publisher"),
        organization = nullableString("organization"), author = nullableString("author"),
        sourceType = string("source_type"), url = string("url"), archiveUrl = nullableString("archive_url"),
        publicationDate = nullableString("publication_date"), retrievedAt = string("retrieved_at"),
        license = string("license"), language = string("language"), qualityTier = string("quality_tier"),
        locator = string("locator"), notes = nullableString("notes"),
    )

    private fun Cursor.document() = ProjectDocument(
        id = string("id"), countryCode = nullableString("country_code"), kind = string("kind"),
        title = string("title"), contentType = string("content_type"), content = string("content"),
    )

    private fun Cursor.librarySummary() = LibraryDocumentSummary(
        id = string("id"), collection = string("collection"), countryCode = nullableString("country_code"),
        countryName = nullableString("country_name"), category = string("category"), title = string("title"),
        relativePath = string("relative_path"), fileType = string("file_type"), byteSize = int("byte_size"),
    )

    private fun Cursor.index(name: String) = getColumnIndexOrThrow(name)
    private fun Cursor.string(name: String) = getString(index(name))
    private fun Cursor.nullableString(name: String): String? = if (isNull(index(name))) null else getString(index(name))
    private fun Cursor.int(name: String) = getInt(index(name))
    private fun Cursor.nullableInt(name: String): Int? = if (isNull(index(name))) null else getInt(index(name))
    private fun Cursor.nullableDouble(name: String): Double? = if (isNull(index(name))) null else getDouble(index(name))

    companion object {
        private const val PREFERRED_NAME_SQL = "COALESCE((SELECT a.name FROM aliases a WHERE a.entity_id=e.id AND a.language='ar' ORDER BY CASE a.kind WHEN 'official' THEN 0 WHEN 'official_variant' THEN 1 ELSE 2 END,a.name LIMIT 1),e.canonical_name)"
        private const val DATABASE_NAME = "arab_atlas.db"
        private const val ASSET_PATH = "database/arab_atlas.db"
        private const val PREFERENCES = "atlas_database"
        private const val DATA_VERSION_KEY = "installed_data_version"
    }
}

fun normalizeArabic(value: String): String = value
    .trim()
    .lowercase()
    .replace(Regex("[\\u064B-\\u065F\\u0670\\u06D6-\\u06ED]"), "")
    .replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا').replace('ٱ', 'ا')
    .replace('ى', 'ي').replace('ة', 'ه').replace('ؤ', 'و').replace('ئ', 'ي')
    .replace("ـ", "")
    .replace(Regex("[^\\p{L}\\p{N}_]+"), " ")
    .trim()
    .replace(Regex("\\s+"), " ")
