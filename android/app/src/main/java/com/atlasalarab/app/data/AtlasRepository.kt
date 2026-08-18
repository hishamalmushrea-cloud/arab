package com.atlasalarab.app.data

import android.net.Uri
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class AtlasRepository(private val database: AtlasDatabase) {
    suspend fun projectStats() = io { database.projectStats() }
    suspend fun countries() = io { database.countries() }
    suspend fun countryDetails(code: String) = io { database.countryDetails(code) }
    suspend fun search(query: String, countryCode: String? = null) = io { database.search(query, countryCode) }
    suspend fun entityDetails(id: String) = io { database.entityDetails(id) }
    suspend fun sources(countryCode: String? = null) = io { database.sources(countryCode) }
    suspend fun source(id: String) = io { database.source(id) }
    suspend fun document(id: String) = io { database.document(id) }
    suspend fun libraryOverview(countryCode: String? = null) = io { database.libraryOverview(countryCode) }
    suspend fun searchLibrary(
        query: String,
        countryCode: String? = null,
        collection: String? = null,
        category: String? = null,
    ) = io { database.searchLibrary(query, countryCode, collection, category) }
    suspend fun libraryDocument(id: String) = io { database.libraryDocument(id) }

    suspend fun resolveLibraryLink(currentPath: String, rawTarget: String): String? = io {
        val target = Uri.decode(rawTarget.substringBefore('#').substringBefore('?')).trim()
        if (target.isBlank()) return@io null
        val segments: MutableList<String> = if (target.startsWith('/')) {
            mutableListOf()
        } else {
            currentPath.substringBeforeLast('/', "").split('/').filter { it.isNotBlank() }.toMutableList()
        }
        target.trimStart('/').replace('\\', '/').split('/').forEach { segment ->
            when (segment) {
                "", "." -> Unit
                ".." -> if (segments.isNotEmpty()) segments.removeLast()
                else -> segments += segment
            }
        }
        database.libraryDocumentIdByPath(segments.joinToString("/"))
    }

    private suspend fun <T> io(block: () -> T): T = withContext(Dispatchers.IO) { block() }
}
