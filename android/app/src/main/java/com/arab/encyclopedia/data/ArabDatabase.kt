package com.arab.encyclopedia.data

import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import android.content.Context

@Database(
    entities = [
        EntityRoom::class,
        AliasRoom::class,
        RelationshipRoom::class,
        ClaimRoom::class,
        SourceRoom::class,
        DenominatorRoom::class,
        CoverageRoom::class,
        SnapshotRoom::class,
        ManifestRoom::class,
        SearchIndexRoom::class
    ],
    version = 1,
    exportSchema = true
)
abstract class ArabDatabase : RoomDatabase() {
    abstract fun entityDao(): EntityDao
    abstract fun aliasDao(): AliasDao
    abstract fun relationshipDao(): RelationshipDao
    abstract fun claimDao(): ClaimDao
    abstract fun sourceDao(): SourceDao
    abstract fun denominatorDao(): DenominatorDao
    abstract fun coverageDao(): CoverageDao
    abstract fun snapshotDao(): SnapshotDao
    abstract fun manifestDao(): ManifestDao
    abstract fun searchDao(): SearchDao

    companion object {
        @Volatile
        private var INSTANCE: ArabDatabase? = null

        fun getDatabase(context: Context): ArabDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    ArabDatabase::class.java,
                    "arab_encyclopedia.db"
                )
                .fallbackToDestructiveMigration()
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
