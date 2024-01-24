from django.contrib import admin

from staticpages.models import GalleryHouses, GalleryTerritory, GalleryFood, TextContentRules, TextContentAccessories, \
    TextContentRent, TextContentCorporate, ContentPrice, ContentSpa

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


@admin.register(GalleryHouses)
class GalleryHousesAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_GALLERY


@admin.register(GalleryTerritory)
class GalleryTerritoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_GALLERY


@admin.register(GalleryFood)
class GalleryFoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_GALLERY


@admin.register(TextContentRules)
class TextContentRulesAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_TEXT_CONTENT


@admin.register(TextContentAccessories)
class TextContentAccessoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_TEXT_CONTENT


@admin.register(TextContentRent)
class TextContentRentAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_TEXT_CONTENT


@admin.register(TextContentCorporate)
class TextContentCorporateAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_TEXT_CONTENT


@admin.register(ContentPrice)
class ContentPriceAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_PRICE


@admin.register(ContentSpa)
class ContentSpaAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    fieldsets = FIELDSETS_FOR_SPA
