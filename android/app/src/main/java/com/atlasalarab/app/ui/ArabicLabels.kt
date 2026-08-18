package com.atlasalarab.app.ui

import java.text.NumberFormat
import java.util.Locale

object ArabicLabels {
    private val types = mapOf(
        "country" to "دولة",
        "city" to "مدينة",
        "village" to "قرية",
        "market" to "سوق",
        "person" to "شخصية",
        "landmark" to "مَعلم",
        "cultural_site" to "موقع ثقافي",
        "archaeological_site" to "موقع أثري",
        "historical_place" to "مكان تاريخي",
        "natural_site" to "موقع طبيعي",
        "language" to "لغة",
        "language_variety" to "تنوع لغوي",
        "lexical_form" to "لفظ محلي",
        "tn_governorate" to "ولاية تونسية",
        "tn_delegation" to "معتمدية",
        "tn_imada" to "عمادة",
        "tn_municipality" to "بلدية تونسية",
        "sa_region" to "منطقة إدارية",
        "sa_governorate" to "محافظة سعودية",
        "sa_markaz" to "مركز",
        "jo_governorate" to "محافظة أردنية",
        "jo_liwa" to "لواء",
        "jo_qada" to "قضاء",
        "ae_emirate" to "إمارة",
        "ae_abu_dhabi_municipality_jurisdiction" to "نطاق بلدية أبوظبي",
        "ae_dubai_planning_sector" to "قطاع تخطيطي بدبي",
        "ae_sharjah_municipality_jurisdiction" to "نطاق بلدية بالشارقة",
        "ae_rak_administrative_area" to "منطقة إدارية برأس الخيمة",
        "ae_ajman_constituent" to "وحدة محلية بعجمان",
        "ae_fujairah_municipal_authority" to "سلطة بلدية بالفجيرة",
        "ae_uaq_municipal_authority" to "سلطة بلدية بأم القيوين",
        "bh_governorate" to "محافظة بحرينية",
        "dz_wilaya" to "ولاية جزائرية",
        "sd_state" to "ولاية سودانية",
        "so_federal_member_state" to "ولاية اتحادية",
        "so_region" to "إقليم صومالي",
        "iq_governorate" to "محافظة عراقية",
        "kw_governorate" to "محافظة كويتية",
        "ma_region" to "جهة مغربية",
        "ma_prefecture" to "عمالة",
        "ma_province" to "إقليم مغربي",
        "ye_governorate" to "محافظة يمنية",
        "ye_capital_municipality" to "أمانة العاصمة",
        "km_island" to "جزيرة",
        "km_prefecture" to "محافظة قمرية",
        "km_commune" to "جماعة",
        "dj_region" to "إقليم جيبوتي",
        "dj_commune" to "بلدية جيبوتية",
        "dj_subprefecture" to "مقاطعة فرعية",
        "djibouti_city" to "مدينة جيبوتي",
        "sy_governorate" to "محافظة سورية",
        "om_governorate" to "محافظة عُمانية",
        "om_wilaya" to "ولاية عُمانية",
        "ps_governorate" to "محافظة فلسطينية",
        "qa_municipality" to "بلدية قطرية",
        "lb_governorate" to "محافظة لبنانية",
        "lb_district" to "قضاء لبناني",
        "ly_municipality" to "بلدية ليبية",
        "ly_shabiya_historical" to "شعبية تاريخية",
        "eg_governorate" to "محافظة مصرية",
        "mr_wilaya" to "ولاية موريتانية",
    )

    private val statuses = mapOf(
        "current" to "حالي",
        "historical" to "تاريخي",
        "proposed" to "مقترح",
        "claimed" to "مُدّعى",
        "verified" to "موثّق",
        "source_verified" to "موثّق بالمصدر",
        "official" to "رسمي",
        "high" to "ثقة عالية",
        "medium" to "ثقة متوسطة",
        "low" to "ثقة منخفضة",
        "published" to "منشور",
    )

    private val predicates = mapOf(
        "administrative_registry_entry" to "قيد في السجل الإداري",
        "administrative_profile" to "الصفة الإدارية",
        "administrative_center" to "المركز الإداري",
        "population" to "عدد السكان",
        "jurisdiction_semantics" to "طبيعة الاختصاص",
        "environmental_context" to "السياق البيئي",
        "world_heritage_inscription_year" to "سنة الإدراج في التراث العالمي",
        "world_heritage_category" to "فئة التراث العالمي",
        "unesco_world_heritage_inscription" to "الإدراج في التراث العالمي",
        "official_regional_dish" to "الطبق الإقليمي الرسمي",
        "official_national_dish" to "الطبق الوطني الرسمي",
        "official_national_dessert" to "الحلوى الوطنية الرسمية",
        "regional_capital_row" to "العاصمة الإقليمية",
        "statistical_region" to "الإقليم الإحصائي",
        "place_classification" to "تصنيف المكان",
        "condition" to "الحالة",
        "period" to "الفترة التاريخية",
        "protection_status" to "حالة الحماية",
        "heritage_scope" to "نطاق التراث",
        "historical_context" to "السياق التاريخي",
        "historical_name_context" to "سياق الاسم التاريخي",
        "area" to "المساحة",
        "bounded_place_context" to "سياق المكان",
        "lexical_attestation" to "توثيق اللفظ",
        "lexical_form" to "الصيغة اللفظية",
        "intangible_cultural_practice" to "ممارسة ثقافية غير مادية",
        "food_culture" to "ثقافة الطعام",
        "food_practice" to "ممارسة غذائية",
        "craft_practice" to "حرفة تقليدية",
        "performance_practice" to "فن أدائي",
        "cultural_practice" to "ممارسة ثقافية",
        "cultural_space" to "فضاء ثقافي",
        "place_connection" to "صلة بالمكان",
        "significance" to "الأهمية",
        "market_character" to "طبيعة السوق",
        "protection_context" to "سياق الحماية",
        "documented_chronology" to "التسلسل الزمني الموثق",
        "administrative_history" to "التاريخ الإداري",
        "administrative_child_counts" to "عدد الوحدات التابعة",
        "district_count" to "عدد المناطق",
        "wilayat_count" to "عدد الولايات",
        "commune_count" to "عدد الجماعات",
        "moughataa_count" to "عدد المقاطعات",
        "federal_establishment_law" to "قانون الإنشاء الاتحادي",
        "establishment_instrument" to "أداة الإنشاء",
        "emergency_inscription" to "إدراج طارئ",
        "world_heritage_in_danger" to "تراث عالمي مهدد",
    )

    private val relationships = mapOf(
        "administrative_parent" to "تابع إداريًا",
        "boundary_intersects" to "تتقاطع حدوده مع",
        "located_in" to "يقع في",
        "associated_with" to "مرتبط بـ",
        "seat_of" to "مقرّ لـ",
        "form_of" to "صيغة من",
        "attested_in" to "موثّق في",
        "variety_of" to "تنوع من",
    )

    private val layers = mapOf(
        "country_scope" to "نطاق الدولة",
        "populated_places" to "الأماكن المأهولة",
        "bounded_populated_place" to "عينة أماكن مأهولة",
        "cities" to "المدن",
        "neighborhoods" to "الأحياء",
        "governorates" to "المحافظات / الولايات",
        "municipalities" to "البلديات",
        "delegations" to "المعتمديات",
        "imadas" to "العمادات",
        "world_heritage_property" to "ممتلكات التراث العالمي",
        "world_heritage_properties" to "ممتلكات التراث العالمي",
        "unesco_world_heritage_properties" to "ممتلكات التراث العالمي",
    )

    fun entityType(value: String): String = types[value] ?: readableFallback(value)
    fun status(value: String?): String = value?.let { statuses[it] ?: readableFallback(it) } ?: "غير محدد"
    fun predicate(value: String): String = predicates[value] ?: readableFallback(value)
    fun relationship(value: String): String = relationships[value] ?: readableFallback(value)
    fun layer(value: String): String = layers[value] ?: types[value] ?: readableFallback(value)
    fun classification(value: String): String = when (value) {
        "official" -> "رسمي"
        "regional" -> "إقليمي"
        "historical" -> "تاريخي"
        "emirate_specific" -> "خاص بالإمارة"
        "local" -> "محلي"
        "national" -> "وطني"
        "shared" -> "مشترك"
        "popular" -> "شعبي"
        "disputed" -> "مختلف عليه"
        else -> readableFallback(value)
    }

    fun sourceTier(value: String): String = when (value) {
        "A" -> "A — مصدر رسمي مباشر"
        "B" -> "B — مصدر مؤسسي أو أكاديمي"
        "C" -> "C — مصدر بحثي مساعد"
        else -> value
    }

    fun sourceType(value: String): String = when (value) {
        "institutional_page" -> "صفحة مؤسسية"
        "official_register" -> "سجل رسمي"
        "official_report" -> "تقرير رسمي"
        "official_dataset" -> "بيانات رسمية"
        "institutional_dataset" -> "بيانات مؤسسية"
        "law" -> "تشريع"
        "census" -> "تعداد"
        "archive" -> "أرشيف"
        "project_audit" -> "تدقيق المشروع"
        "academic" -> "مصدر أكاديمي"
        "standard" -> "معيار"
        else -> readableFallback(value)
    }

    fun documentKind(value: String): String = when (value) {
        "manifest" -> "بيان النطاق والقيود"
        "cultural_status" -> "حالة المجالات الثقافية"
        else -> readableFallback(value)
    }

    fun libraryCollection(value: String): String = when (value) {
        "الدول" -> "موسوعة الدول"
        "العواصم" -> "العواصم العربية"
        "الحارات_والأحياء" -> "الأحياء والحارات"
        "الخريطة_الثقافية" -> "الخريطة الثقافية"
        "المقارنات" -> "الدراسات المقارنة"
        "قاعدة_بيانات_الأماكن" -> "جداول الأماكن"
        "المصادر_والمراجع" -> "المصادر والمراجع"
        else -> value.replace('_', ' ')
    }

    fun fileSize(bytes: Long): String = when {
        bytes >= 1_048_576 -> "${decimal(bytes / 1_048_576.0)} م.ب"
        bytes >= 1_024 -> "${decimal(bytes / 1_024.0)} ك.ب"
        else -> "$bytes بايت"
    }

    fun flag(countryCode: String): String = countryCode.uppercase().map {
        Character.toChars(0x1F1E6 + (it.code - 'A'.code)).concatToString()
    }.joinToString("")

    fun number(value: Int): String = NumberFormat.getIntegerInstance(Locale("ar")).format(value)
    fun decimal(value: Double): String = NumberFormat.getNumberInstance(Locale("ar")).apply {
        maximumFractionDigits = 1
    }.format(value)

    private fun readableFallback(value: String): String = value
        .replace(Regex("^(ae|bh|dj|dz|eg|iq|jo|km|kw|lb|ly|ma|mr|om|ps|qa|sa|sd|so|sy|tn|ye)_"), "")
        .replace('_', ' ')
}
