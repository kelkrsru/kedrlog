from django.contrib import admin
from .models import Company, House, Rate, Reserve, AdditionalFeatures, AdditionalServices, WeekendDays, SocialNetworks, \
    ReserveServices, SpaServices, PriceForSpaServices, SettingsBitrix24, SettingsSite

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
    list_display = ['name', 'price', 'active']
    ordering = ['-active']


@admin.register(SpaServices)
class SpaServicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active']


@admin.register(PriceForSpaServices)
class PriceForSpaServicesAdmin(admin.ModelAdmin):
    list_display = ['price', 'max_guest', 'duration']


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ['name', 'house', 'active', ]
    ordering = ['house__name', '-active', 'name', ]
    fieldsets = [
        (
            None,
            {
                "fields": ["active", "name", "description", "house", "price", "price_weekend", "min_time",
                           "guests_in_price", "additional_guest_price"],
            },
        ),
        (
            'Интеграция с Битрикс24',
            {
                "fields": ['id_rent_in_catalog_b24', 'id_rent_weekend_in_catalog_b24',
                           'id_additional_guest_in_catalog_b24'],
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
