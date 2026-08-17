package com.arab.encyclopedia.data

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

@Dao
interface EntityDao {
    @Query("SELECT * FROM entities WHERE id = :id")
    suspend fun getById(id: String): EntityRoom?

    @Query("SELECT * FROM entities WHERE countryCode = :iso2")
    suspend fun getByCountry(iso2: String): List<EntityRoom>

    @Query("SELECT * FROM entities WHERE entityType = 'country'")
    suspend fun getCountries(): List<EntityRoom>

    @Query("SELECT * FROM entities WHERE countryCode = :iso2 AND entityType = :type")
    suspend fun getByCountryAndType(iso2: String, type: String): List<EntityRoom>

    @Query("SELECT * FROM entities")
    suspend fun getAll(): List<EntityRoom>

    @Query("SELECT COUNT(*) FROM entities")
    suspend fun count(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(entities: List<EntityRoom>)

    @Query("DELETE FROM entities")
    suspend fun clear()
}

@Dao
interface AliasDao {
    @Query("SELECT * FROM aliases WHERE entityId = :entityId")
    suspend fun getByEntity(entityId: String): List<AliasRoom>

    @Query("SELECT * FROM aliases WHERE name LIKE '%' || :query || '%'")
    suspend fun searchByName(query: String): List<AliasRoom>

    @Query("SELECT COUNT(*) FROM aliases")
    suspend fun count(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(aliases: List<AliasRoom>)

    @Query("DELETE FROM aliases")
    suspend fun clear()
}

@Dao
interface RelationshipDao {
    @Query("SELECT * FROM relationships WHERE childId = :id OR parentId = :id")
    suspend fun getRelated(id: String): List<RelationshipRoom>

    @Query("SELECT * FROM relationships WHERE parentId = :parentId AND relationshipType = 'administrative_parent'")
    suspend fun getChildren(parentId: String): List<RelationshipRoom>

    @Query("SELECT * FROM relationships WHERE childId = :childId AND relationshipType = 'administrative_parent'")
    suspend fun getParent(childId: String): RelationshipRoom?

    @Query("SELECT COUNT(*) FROM relationships")
    suspend fun count(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(relationships: List<RelationshipRoom>)

    @Query("DELETE FROM relationships")
    suspend fun clear()
}

@Dao
interface ClaimDao {
    @Query("SELECT * FROM claims WHERE subjectId = :subjectId")
    suspend fun getBySubject(subjectId: String): List<ClaimRoom>

    @Query("SELECT COUNT(*) FROM claims")
    suspend fun count(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(claims: List<ClaimRoom>)

    @Query("DELETE FROM claims")
    suspend fun clear()
}

@Dao
interface SourceDao {
    @Query("SELECT * FROM sources WHERE id = :id")
    suspend fun getById(id: String): SourceRoom?

    @Query("SELECT * FROM sources")
    suspend fun getAll(): List<SourceRoom>

    @Query("SELECT * FROM sources WHERE qualityTier = :tier")
    suspend fun getByTier(tier: String): List<SourceRoom>

    @Query("SELECT COUNT(*) FROM sources")
    suspend fun count(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(sources: List<SourceRoom>)

    @Query("DELETE FROM sources")
    suspend fun clear()
}

@Dao
interface CoverageDao {
    @Query("SELECT * FROM coverage WHERE countryCode = :iso2")
    suspend fun getByCountry(iso2: String): List<CoverageRoom>

    @Query("SELECT * FROM coverage")
    suspend fun getAll(): List<CoverageRoom>

    @Query("SELECT COUNT(*) FROM coverage")
    suspend fun count(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(coverage: List<CoverageRoom>)

    @Query("DELETE FROM coverage")
    suspend fun clear()
}

@Dao
interface DenominatorDao {
    @Query("SELECT * FROM denominators WHERE countryCode = :iso2")
    suspend fun getByCountry(iso2: String): List<DenominatorRoom>

    @Query("SELECT COUNT(*) FROM denominators")
    suspend fun count(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(denominators: List<DenominatorRoom>)

    @Query("DELETE FROM denominators")
    suspend fun clear()
}

@Dao
interface SnapshotDao {
    @Query("SELECT * FROM snapshots ORDER BY capturedAt DESC")
    suspend fun getAll(): List<SnapshotRoom>

    @Query("SELECT COUNT(*) FROM snapshots")
    suspend fun count(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(snapshots: List<SnapshotRoom>)

    @Query("DELETE FROM snapshots")
    suspend fun clear()
}

@Dao
interface ManifestDao {
    @Query("SELECT * FROM manifests")
    suspend fun getAll(): List<ManifestRoom>

    @Query("SELECT * FROM manifests WHERE iso2 = :iso2")
    suspend fun getByIso(iso2: String): ManifestRoom?

    @Query("SELECT COUNT(*) FROM manifests")
    suspend fun count(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(manifests: List<ManifestRoom>)

    @Query("DELETE FROM manifests")
    suspend fun clear()
}

@Dao
interface SearchDao {
    @Query("SELECT * FROM search_index WHERE canonicalName LIKE '%' || :query || '%' OR aliasesConcatenated LIKE '%' || :query || '%' OR normalizedName LIKE '%' || :qNorm || '%'")
    suspend fun search(query: String, qNorm: String): List<SearchIndexRoom>

    @Query("SELECT COUNT(*) FROM search_index")
    suspend fun count(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(items: List<SearchIndexRoom>)

    @Query("DELETE FROM search_index")
    suspend fun clear()
}
