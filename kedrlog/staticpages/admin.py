from django.contrib import admin
import staticpages.models as static_pages_models

FIELDS_SEO = {"fields": ["seo_title", "seo_description", "seo_keywords"]}

FIELDSETS_FOR_GALLERY = [
    (
        None,
        {
            "fields": ["active", "name", "header", "second_header", "items"],
        },
    ),
    (
        "Настройки для SEO",
        FIELDS_SEO
    ),
]

FIELDSETS_FOR_TEXT_CONTENT = [
    (
        None,
        {
            "fields": ["active", "name", "header", "second_header", "text"],
        },
    ),
    (
        "Настройки для SEO",
        FIELDS_SEO
    ),
]

FIELDSETS_FOR_PRICE = [
    (
        None,
        {
            "fields": ["active", "name", "header", "second_header", "header_image"],
        },
    ),
    (
        'Основные услуги',
        {
            "fields": ["header_house", "description_house", "house"],
        },
    ),
    (
        'Дополнительные услуги',
        {
            "fields": ["header_service", "description_service", "service"],
        },
    ),
    (
        "Настройки для SEO",
        FIELDS_SEO
    ),
]

FIELDSETS_FOR_SPA = [
    (
        None,
        {
            "fields": ["active", "name", "header", "second_header", "spa_service"],
        },
    ),
    (
        "Настройки для SEO",
        FIELDS_SEO
    ),
]

FIELDSETS_FOR_GIFT_CERTIFICATE = [
    (
        None,
        {
            "fields": ["active", "name", "header", "second_header", "gift_certificates"],
        },
    ),
    (
        "Настройки для SEO",
        FIELDS_SEO
    ),
]


@admin.register(static_pages_models.GalleryHouses)
class GalleryHousesAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_GALLERY


@admin.register(static_pages_models.GalleryTerritory)
class GalleryTerritoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_GALLERY


@admin.register(static_pages_models.GalleryFood)
class GalleryFoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_GALLERY


@admin.register(static_pages_models.TextContentRules)
class TextContentRulesAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_TEXT_CONTENT


@admin.register(static_pages_models.TextContentFz152)
class TextContentFz152Admin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_TEXT_CONTENT


@admin.register(static_pages_models.TextContentAccessories)
class TextContentAccessoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_TEXT_CONTENT


@admin.register(static_pages_models.TextContentCorporate)
class TextContentCorporateAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_TEXT_CONTENT


@admin.register(static_pages_models.ContentPrice)
class ContentPriceAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_PRICE


@admin.register(static_pages_models.ContentSpa)
class ContentSpaAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_SPA


@admin.register(static_pages_models.ContentGiftCertificate)
class ContentSpaAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_GIFT_CERTIFICATE
