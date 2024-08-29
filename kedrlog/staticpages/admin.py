from django.contrib import admin
from django.utils.safestring import mark_safe

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
            "fields": ["active", "name", "header", "second_header", "header_image", "header_image_preview"],
        },
    ),
    (
        'Основные услуги',
        {
            "fields": ["header_house", "description_house", "is_show_card_image", "description_spa_services"],
        },
    ),
    (
        'Дополнительные услуги',
        {
            "fields": ["header_service", "description_service"],
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
        'Контент',
        {
            "fields": ["content_image", "content_text", ],
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


@admin.register(static_pages_models.TextContentRulesGiftCert)
class TextContentRulesGiftCertAdmin(admin.ModelAdmin):
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
    readonly_fields = ['header_image_preview']

    @staticmethod
    @admin.display(description="Предварительный просмотр изображения")
    def header_image_preview(obj):
        return mark_safe(f'<img src="{obj.header_image.url}" style="max-height: 200px;">')


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
