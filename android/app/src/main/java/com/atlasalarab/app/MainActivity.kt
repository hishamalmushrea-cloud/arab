package com.atlasalarab.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.remember
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.platform.LocalLayoutDirection
import com.atlasalarab.app.data.AtlasDatabase
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.ReadingStore
import com.atlasalarab.app.ui.AtlasApp
import com.atlasalarab.app.ui.theme.AtlasTheme

class MainActivity : ComponentActivity() {
    private lateinit var atlasDatabase: AtlasDatabase

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        atlasDatabase = AtlasDatabase(applicationContext)
        setContent {
            AtlasTheme {
                CompositionLocalProvider(LocalLayoutDirection provides LayoutDirection.Rtl) {
                    val repository = remember { AtlasRepository(atlasDatabase) }
                    val readingStore = remember { ReadingStore(applicationContext) }
                    AtlasApp(repository, readingStore)
                }
            }
        }
    }

    override fun onDestroy() {
        atlasDatabase.close()
        super.onDestroy()
    }
}
