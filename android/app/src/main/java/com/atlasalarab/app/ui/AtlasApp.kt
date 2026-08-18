package com.atlasalarab.app.ui

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Bookmarks
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.LocalLibrary
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.Public
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.CenterAlignedTopAppBar
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.atlasalarab.app.data.AtlasRepository
import com.atlasalarab.app.data.ReadingStore
import com.atlasalarab.app.ui.screens.AboutScreen
import com.atlasalarab.app.ui.screens.CountriesScreen
import com.atlasalarab.app.ui.screens.CountryScreen
import com.atlasalarab.app.ui.screens.DocumentScreen
import com.atlasalarab.app.ui.screens.EntityScreen
import com.atlasalarab.app.ui.screens.HomeScreen
import com.atlasalarab.app.ui.screens.LibraryDocumentScreen
import com.atlasalarab.app.ui.screens.LibraryScreen
import com.atlasalarab.app.ui.screens.SavedScreen
import com.atlasalarab.app.ui.screens.SearchScreen
import com.atlasalarab.app.ui.screens.SourceDetailScreen
import com.atlasalarab.app.ui.screens.SourcesScreen

private object Routes {
    const val Home = "home"
    const val Countries = "countries"
    const val Search = "search"
    const val Sources = "sources"
    const val Library = "library"
    const val Saved = "saved"
    const val About = "about"
    const val Country = "country/{code}"
    const val Entity = "entity/{id}"
    const val Source = "source/{id}"
    const val Document = "document/{id}"
    const val LibraryCountry = "library-country/{code}"
    const val LibraryDocument = "library-document/{id}"

    fun country(code: String) = "country/$code"
    fun entity(id: String) = "entity/$id"
    fun source(id: String) = "source/$id"
    fun document(id: String) = "document/$id"
    fun countryLibrary(code: String) = "library-country/$code"
    fun libraryDocument(id: String) = "library-document/$id"
}

private data class BottomDestination(val route: String, val label: String, val icon: ImageVector)

private val bottomDestinations = listOf(
    BottomDestination(Routes.Home, "الرئيسية", Icons.Default.Home),
    BottomDestination(Routes.Countries, "الدول", Icons.Default.Public),
    BottomDestination(Routes.Library, "المكتبة", Icons.Default.LocalLibrary),
    BottomDestination(Routes.Search, "البحث", Icons.Default.Search),
    BottomDestination(Routes.Sources, "المصادر", Icons.Default.MenuBook),
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AtlasApp(repository: AtlasRepository, readingStore: ReadingStore) {
    val navController = rememberNavController()
    val backStackEntry by navController.currentBackStackEntryAsState()
    val destination = backStackEntry?.destination
    val route = destination?.route ?: Routes.Home
    val rootRoute = bottomDestinations.any { it.route == route }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        topBar = {
            CenterAlignedTopAppBar(
                title = {
                    Text(
                        titleForRoute(route),
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                    )
                },
                navigationIcon = {
                    if (!rootRoute) {
                        IconButton(onClick = { navController.popBackStack() }) {
                            Icon(Icons.AutoMirrored.Filled.ArrowBack, "رجوع")
                        }
                    }
                },
                colors = TopAppBarDefaults.centerAlignedTopAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    titleContentColor = MaterialTheme.colorScheme.primary,
                    navigationIconContentColor = MaterialTheme.colorScheme.onSurface,
                    actionIconContentColor = MaterialTheme.colorScheme.onSurfaceVariant,
                ),
                actions = {
                    if (route != Routes.Saved) {
                        IconButton(onClick = { navController.navigate(Routes.Saved) }) {
                            Icon(Icons.Default.Bookmarks, "المحفوظات وسجل القراءة")
                        }
                    }
                    if (route != Routes.About) {
                        IconButton(onClick = { navController.navigate(Routes.About) }) {
                            Icon(Icons.Default.Info, "حول التطبيق")
                        }
                    }
                },
            )
        },
        bottomBar = {
            NavigationBar {
                bottomDestinations.forEach { item ->
                    val selected = destination?.hierarchy?.any { it.route == item.route } == true
                    NavigationBarItem(
                        selected = selected,
                        onClick = {
                            navController.navigate(item.route) {
                                popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        icon = { Icon(item.icon, item.label) },
                        label = { Text(item.label) },
                    )
                }
            }
        },
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Routes.Home,
            modifier = Modifier.padding(innerPadding),
        ) {
            composable(Routes.Home) {
                HomeScreen(
                    repository = repository,
                    readingStore = readingStore,
                    onContinueReading = { navController.navigate(Routes.libraryDocument(it)) },
                    onOpenSearch = { navController.navigate(Routes.Search) },
                    onOpenCountries = { navController.navigate(Routes.Countries) },
                    onOpenLibrary = { navController.navigate(Routes.Library) },
                    onOpenCountry = { navController.navigate(Routes.country(it)) },
                )
            }
            composable(Routes.Countries) {
                CountriesScreen(repository, onOpenCountry = { navController.navigate(Routes.country(it)) })
            }
            composable(Routes.Library) {
                LibraryScreen(
                    repository = repository,
                    onOpenDocument = { navController.navigate(Routes.libraryDocument(it)) },
                )
            }
            composable(Routes.Search) {
                SearchScreen(
                    repository = repository,
                    onOpenEntity = { navController.navigate(Routes.entity(it)) },
                    onOpenLibraryDocument = { navController.navigate(Routes.libraryDocument(it)) },
                )
            }
            composable(Routes.Sources) {
                SourcesScreen(repository, onOpenSource = { navController.navigate(Routes.source(it)) })
            }
            composable(Routes.Saved) {
                SavedScreen(readingStore, onOpenDocument = { navController.navigate(Routes.libraryDocument(it)) })
            }
            composable(Routes.About) { AboutScreen(repository) }
            composable(Routes.Country) { entry ->
                CountryScreen(
                    code = entry.arguments?.getString("code").orEmpty(),
                    repository = repository,
                    onOpenEntity = { navController.navigate(Routes.entity(it)) },
                    onOpenSource = { navController.navigate(Routes.source(it)) },
                    onOpenDocument = { navController.navigate(Routes.document(it)) },
                    onOpenLibrary = { navController.navigate(Routes.countryLibrary(it)) },
                )
            }
            composable(Routes.Entity) { entry ->
                EntityScreen(
                    id = entry.arguments?.getString("id").orEmpty(),
                    repository = repository,
                    onOpenEntity = { navController.navigate(Routes.entity(it)) },
                    onOpenSource = { navController.navigate(Routes.source(it)) },
                )
            }
            composable(Routes.Source) { entry ->
                SourceDetailScreen(entry.arguments?.getString("id").orEmpty(), repository)
            }
            composable(Routes.Document) { entry ->
                DocumentScreen(entry.arguments?.getString("id").orEmpty(), repository)
            }
            composable(Routes.LibraryCountry) { entry ->
                LibraryScreen(
                    repository = repository,
                    initialCountryCode = entry.arguments?.getString("code"),
                    onOpenDocument = { navController.navigate(Routes.libraryDocument(it)) },
                )
            }
            composable(Routes.LibraryDocument) { entry ->
                LibraryDocumentScreen(
                    id = entry.arguments?.getString("id").orEmpty(),
                    repository = repository,
                    readingStore = readingStore,
                    onOpenDocument = { navController.navigate(Routes.libraryDocument(it)) },
                    onOpenCountryLibrary = { navController.navigate(Routes.countryLibrary(it)) },
                )
            }
        }
    }
}

private fun titleForRoute(route: String): String = when (route) {
    Routes.Home -> "أطلس العرب"
    Routes.Countries -> "الدول"
    Routes.Library -> "المكتبة الموسوعية"
    Routes.Saved -> "مكتبتي"
    Routes.Search -> "البحث"
    Routes.Sources -> "المصادر"
    Routes.About -> "حول التطبيق"
    Routes.Country -> "ملف الدولة"
    Routes.LibraryCountry -> "ملفات الدولة"
    Routes.LibraryDocument -> "محتوى الملف"
    Routes.Entity -> "تفاصيل المكان"
    Routes.Source -> "تفاصيل المصدر"
    Routes.Document -> "وثيقة البيانات"
    else -> "أطلس العرب"
}
