from django.contrib import admin

from .models import (AdditionalFeatures, AdditionalServices, Company, GiftCertificate, GiftCertificateType, House,
                     OrderGiftCertificate, Price, PriceForSpaServices, Rate, Reserve, ReserveServices, SettingsBitrix24,
                     SettingsSite, SocialNetworks, SpaServices, WeekendDays, Weeks)

admin.site.enable_nav_sidebar = False


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', ]
    fieldsets = [
        (
            None,
            {
                "fields": ["active", "name", "phone", "address", "logo_header", "logo_footer", "favicon"],
            },
        ),
        (
            'Социальные сети',
            {
                'fields': ['social_networks', ],
            }
        ),
        (
            'Seo для главной страницы',
            {
                'fields': ['seo_title', 'seo_description', 'seo_keywords'],
            }
        ),
    ]


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', 'name']


@admin.register(AdditionalFeatures)
class AdditionalFeaturesAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(AdditionalServices)
class AdditionalServicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'active', 'group', ]
    ordering = ['-active']
    list_editable = ['group', ]


@admin.register(SpaServices)
class SpaServicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', 'sort']
    ordering = ['-active', 'sort']
    list_editable = ['sort', ]


@admin.register(PriceForSpaServices)
class PriceForSpaServicesAdmin(admin.ModelAdmin):
    list_display = ['price', 'max_guest', 'duration']


@admin.register(Weeks)
class WeeksAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    ordering = ['number']


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    ordering = ['name', ]
    fieldsets = [
        (
            None,
            {
                "fields": ["name", "comment", "description", "house", "price", "min_time", 'max_guest',
                           "guests_in_price", "additional_guest_price"],
            },
        ),
        (
            'Интеграция с Битрикс24',
            {
                "fields": ['id_rent_in_catalog_b24', 'id_additional_guest_in_catalog_b24'],
            },
        ),
    ]


class ReserveServicesInline(admin.TabularInline):
    model = ReserveServices
    extra = 0
    min_num = 0
    readonly_fields = ['cost', 'id_b24']


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ['start_date_time', 'end_date_time', 'house', ]
    inlines = [ReserveServicesInline, ]


@admin.register(WeekendDays)
class WeekendDaysAdmin(admin.ModelAdmin):
    list_display = ['date', ]
    list_filter = ['date', ]


@admin.register(SocialNetworks)
class SocialNetworksAdmin(admin.ModelAdmin):
    list_display = ['name', 'show_header', 'show_footer', 'show_block_booking', ]


@admin.register(SettingsBitrix24)
class SettingsBitrix24Admin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active']


@admin.register(SettingsSite)
class SettingsSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active']
    fieldsets = [
        (
            None,
            {
                "fields": ["active", "name"],
            },
        ),
        (
            'Настройки модуля бронирования',
            {
                "fields": ['reserve_start_time', 'reserve_end_time', 'reserve_interval', 'reserve_show_interval',
                           'reserve_closed', 'reserve_closed_all'],
            },
        ),
        (
            'Настройки подарочных сертификатов',
            {
                "fields": ['gift_certificate_closed', 'gift_certificate_closed_all', 'text_gift_certificate_closed',
                           'text_gift_certificate_ok'],
            },
        ),
    ]


@admin.register(GiftCertificateType)
class GiftCertificateTypeAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(GiftCertificate)
class GiftCertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active']
    fieldsets = [
        (
            None,
            {
                "fields": ["active", "name", 'description'],
            },
        ),
        (
            'Настройки подарочного сертификата',
            {
                "fields": ['type', 'min_price', 'max_price', 'step_price', 'validity'],
            },
        ),
        (
            'Настройки внешнего вида',
            {
                "fields": ['background_image_card', 'text_color', 'background_image_form'],
            },
        ),
        (
            'Настройки отправки и интеграции',
            {
                "fields": ['send_email', 'email', 'send_b24', 'id_catalog_b24'],
            },
        ),
    ]


@admin.register(OrderGiftCertificate)
class OrderGiftCertificateAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'buy_date_time', 'validity_date_time']
    ordering = ['-validity_date_time']
    fieldsets = [
        (
            'Параметры сертификата',
            {
                'fields': ['type', 'validity_date_time', 'user', 'gift_certificate'],
            },
        ),
        (
            'Стоимость и оплата',
            {
                'fields': ['price', 'paid', 'buy_date_time', 'used'],
            },
        ),
        (
            'Данные пользователя',
            {
                'fields': ['user_name', 'user_lastname', 'user_phone', 'user_email', 'user_address'],
            },
        ),
        (
            'Отправка и интеграция',
            {
                'fields': ['sent_email', 'sent_bitrix', 'deal_id_b24'],
            },
        ),
    ]
