package com.atlasalarab.app.data

import android.content.Context
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import org.json.JSONArray
import org.json.JSONObject

data class ReadingItem(
    val id: String,
    val collection: String,
    val countryCode: String?,
    val countryName: String?,
    val category: String,
    val title: String,
    val relativePath: String,
    val fileType: String,
    val byteSize: Int,
    val lastOpenedAt: Long,
) {
    fun asSummary() = LibraryDocumentSummary(
        id = id,
        collection = collection,
        countryCode = countryCode,
        countryName = countryName,
        category = category,
        title = title,
        relativePath = relativePath,
        fileType = fileType,
        byteSize = byteSize,
    )
}

/** Local-only reading state. No account, permission, or network access is used. */
class ReadingStore(context: Context) {
    private val preferences = context.getSharedPreferences(PREFERENCES, Context.MODE_PRIVATE)
    private val _favorites = MutableStateFlow(readItems(FAVORITES_KEY))
    private val _recent = MutableStateFlow(readItems(RECENT_KEY))

    val favorites: StateFlow<List<ReadingItem>> = _favorites
    val recent: StateFlow<List<ReadingItem>> = _recent

    fun isFavorite(documentId: String): Boolean = _favorites.value.any { it.id == documentId }

    fun toggleFavorite(summary: LibraryDocumentSummary): Boolean {
        val current = _favorites.value.toMutableList()
        val existing = current.indexOfFirst { it.id == summary.id }
        val added = existing < 0
        if (added) current.add(0, summary.toReadingItem()) else current.removeAt(existing)
        _favorites.value = current
        writeItems(FAVORITES_KEY, current)
        return added
    }

    fun recordOpen(summary: LibraryDocumentSummary) {
        val updated = _recent.value.filterNot { it.id == summary.id }.toMutableList()
        updated.add(0, summary.toReadingItem())
        while (updated.size > MAX_RECENT) updated.removeLast()
        _recent.value = updated
        writeItems(RECENT_KEY, updated)
    }

    fun clearRecent() {
        _recent.value = emptyList()
        preferences.edit().remove(RECENT_KEY).apply()
    }

    fun savePosition(documentId: String, itemIndex: Int) {
        preferences.edit().putInt("$POSITION_PREFIX$documentId", itemIndex.coerceAtLeast(0)).apply()
    }

    fun position(documentId: String): Int = preferences.getInt("$POSITION_PREFIX$documentId", 0)

    private fun LibraryDocumentSummary.toReadingItem() = ReadingItem(
        id = id,
        collection = collection,
        countryCode = countryCode,
        countryName = countryName,
        category = category,
        title = title,
        relativePath = relativePath,
        fileType = fileType,
        byteSize = byteSize,
        lastOpenedAt = System.currentTimeMillis(),
    )

    private fun readItems(key: String): List<ReadingItem> = runCatching {
        val array = JSONArray(preferences.getString(key, "[]"))
        buildList {
            for (index in 0 until array.length()) {
                val item = array.getJSONObject(index)
                add(
                    ReadingItem(
                        id = item.getString("id"),
                        collection = item.getString("collection"),
                        countryCode = item.optString("countryCode").ifBlank { null },
                        countryName = item.optString("countryName").ifBlank { null },
                        category = item.getString("category"),
                        title = item.getString("title"),
                        relativePath = item.getString("relativePath"),
                        fileType = item.getString("fileType"),
                        byteSize = item.getInt("byteSize"),
                        lastOpenedAt = item.optLong("lastOpenedAt"),
                    ),
                )
            }
        }
    }.getOrDefault(emptyList())

    private fun writeItems(key: String, items: List<ReadingItem>) {
        val array = JSONArray()
        items.forEach { item ->
            array.put(
                JSONObject()
                    .put("id", item.id)
                    .put("collection", item.collection)
                    .put("countryCode", item.countryCode ?: "")
                    .put("countryName", item.countryName ?: "")
                    .put("category", item.category)
                    .put("title", item.title)
                    .put("relativePath", item.relativePath)
                    .put("fileType", item.fileType)
                    .put("byteSize", item.byteSize)
                    .put("lastOpenedAt", item.lastOpenedAt),
            )
        }
        preferences.edit().putString(key, array.toString()).apply()
    }

    companion object {
        private const val PREFERENCES = "atlas_reading"
        private const val FAVORITES_KEY = "favorites"
        private const val RECENT_KEY = "recent"
        private const val POSITION_PREFIX = "position:"
        private const val MAX_RECENT = 30
    }
}
