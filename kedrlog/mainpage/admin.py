from django.contrib import admin
from mainpage.models import (ContentBlockBooking, ContentBlockInfrastructure,
                             ContentBlockMain, ContentBlockRoundedMenuItem,
                             ContentBlockService, ContentBlockYandexMap,
                             HouseShowBooking, ToastMain)


@admin.register(ContentBlockMain)
class ContentBlockMainAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]


@admin.register(ToastMain)
class ToastMainAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]


@admin.register(ContentBlockInfrastructure)
class ContentBlockInfrastructureAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]


@admin.register(ContentBlockYandexMap)
class ContentBlockYandexMapAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]


@admin.register(ContentBlockService)
class ContentBlockServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]


class HouseShowBookingInline(admin.TabularInline):
    model = HouseShowBooking
    extra = 1


@admin.register(ContentBlockBooking)
class ContentBlockBookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    ordering = ['-active', ]
    inlines = [HouseShowBookingInline, ]


@admin.register(HouseShowBooking)
class HouseShowBookingAdmin(admin.ModelAdmin):
    list_display = ['house', 'block_booking']
    ordering = ['block_booking', ]


@admin.register(ContentBlockRoundedMenuItem)
class ContentBlockRoundedMenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', ]
