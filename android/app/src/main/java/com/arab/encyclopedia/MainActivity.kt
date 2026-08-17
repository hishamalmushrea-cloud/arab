package com.arab.encyclopedia

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.arab.encyclopedia.data.ArabDatabase
import com.arab.encyclopedia.data.DataImporter
import com.arab.encyclopedia.ui.screens.*
import com.arab.encyclopedia.ui.theme.ArabEncyclopediaTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ArabEncyclopediaTheme {
                val navController = rememberNavController()
                val context = LocalContext.current
                val db = remember { ArabDatabase.getDatabase(context) }
                var isDbReady by remember { mutableStateOf(false) }
                var importProgress by remember { mutableStateOf("جاري التحقق من البيانات...") }
                var importResult by remember { mutableStateOf<com.arab.encyclopedia.data.ImportResult?>(null) }
                val scope = rememberCoroutineScope()

                LaunchedEffect(Unit) {
                    val populated = DataImporter.isDatabasePopulated(context)
                    if (populated) {
                        isDbReady = true
                    } else {
                        // First launch - import 8.8 MB JSON into Room - preserves 100%
                        try {
                            val result = DataImporter.importFromAssets(context) { progress ->
                                importProgress = progress
                            }
                            importResult = result
                            isDbReady = result.isComplete()
                        } catch (e: Exception) {
                            importProgress = "فشل الاستيراد: ${e.message}"
                            e.printStackTrace()
                        }
                    }
                }

                if (!isDbReady) {
                    // Splash / Import screen
                    Surface(modifier = Modifier.fillMaxSize()) {
                        Column(modifier = Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.Center) {
                            Text("موسوعة العرب", style = MaterialTheme.typography.headlineLarge)
                            Text("Schema 2.0.0 — 5317 كيان + 3261 اسم + 5706 علاقة + 2245 معلومة + 151 مصدر", style = MaterialTheme.typography.bodyMedium)
                            Spacer(Modifier.height(16.dp))
                            LinearProgressIndicator(modifier = Modifier.fillMaxWidth())
                            Spacer(Modifier.height(8.dp))
                            Text(importProgress, style = MaterialTheme.typography.bodySmall)
                            importResult?.let {
                                Spacer(Modifier.height(8.dp))
                                Text("تم: ${it.entities} كيان، ${it.aliases} اسم، ${it.relationships} علاقة، ${it.claims} معلومة — 100% preserved = ${it.isComplete()}", style = MaterialTheme.typography.labelSmall)
                            }
                            Text("البيانات الأساسية تعمل Offline — الروابط الخارجية تحتاج إنترنت", style = MaterialTheme.typography.labelSmall)
                        }
                    }
                } else {
                    Scaffold(
                        bottomBar = {
                            NavigationBar {
                                NavigationBarItem(
                                    icon = { Text("🏠") },
                                    label = { Text("الرئيسية") },
                                    selected = false,
                                    onClick = { navController.navigate("home") }
                                )
                                NavigationBarItem(
                                    icon = { Text("🔍") },
                                    label = { Text("بحث") },
                                    selected = false,
                                    onClick = { navController.navigate("search") }
                                )
                                NavigationBarItem(
                                    icon = { Text("🌍") },
                                    label = { Text("الدول") },
                                    selected = false,
                                    onClick = { navController.navigate("countries") }
                                )
                            }
                        }
                    ) { padding ->
                        Box(modifier = Modifier.padding(padding)) {
                            NavHost(navController = navController, startDestination = "home") {
                                composable("home") {
                                    HomeScreen(
                                        onNavigateToCountry = { iso2 -> navController.navigate("country/$iso2") },
                                        onNavigateToSearch = { navController.navigate("search") }
                                    )
                                }
                                composable("countries") {
                                    // Reuse country list via Home logic - for now show Home's country part
                                    // We'll use a dedicated screen later
                                    CountriesScreenPlaceholder(onNavigateToCountry = { iso2 -> navController.navigate("country/$iso2") })
                                }
                                composable("search") {
                                    SearchScreen(onNavigateToEntity = { iso2, entityId -> navController.navigate("entity/$iso2/$entityId") })
                                }
                                composable("country/{iso2}") { backStackEntry ->
                                    val iso2 = backStackEntry.arguments?.getString("iso2") ?: "SA"
                                    CountryScreen(iso2 = iso2, onNavigateToEntity = { _, entityId -> navController.navigate("entity/$iso2/$entityId") })
                                }
                                composable("entity/{iso2}/{entityId}") { backStackEntry ->
                                    val iso2 = backStackEntry.arguments?.getString("iso2") ?: "SA"
                                    val entityId = backStackEntry.arguments?.getString("entityId") ?: ""
                                    EntityScreen(entityId = entityId, iso2 = iso2, onNavigateToEntity = { _, id -> navController.navigate("entity/$iso2/$id") })
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun CountriesScreenPlaceholder(onNavigateToCountry: (String) -> Unit) {
    val context = LocalContext.current
    val db = remember { ArabDatabase.getDatabase(context) }
    var countries by remember { mutableStateOf<List<com.arab.encyclopedia.data.EntityRoom>>(emptyList()) }
    LaunchedEffect(Unit) {
        countries = db.entityDao().getCountries()
    }
    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("الدول العربية الـ22", style = MaterialTheme.typography.headlineMedium)
        Spacer(Modifier.height(8.dp))
        countries.forEach { c ->
            Card(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), onClick = { onNavigateToCountry(c.countryCode) }) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text(c.canonicalName)
                    Text("${c.countryCode} — ${c.id}", style = MaterialTheme.typography.labelSmall)
                }
            }
        }
    }
}
