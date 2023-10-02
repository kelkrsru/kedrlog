from django.contrib import admin
from .models import Company, House, TimeCost, Rate, Reserve

admin.site.enable_nav_sidebar = False


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'active', ]


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(TimeCost)
class TimeCostAdmin(admin.ModelAdmin):
    list_display = ['start_time', 'end_time', 'interval', 'cost', ]


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ['name', 'house', 'active', ]
    ordering = ['house__name', '-active', 'name', ]
    filter_horizontal = ('rate',)
    fieldsets = [
        (
            None,
            {
                "fields": ["active", "name", "description", "house", ],
            },
        ),
        (
            "Тарификация",
            {
                'fields': ['rate', ]
            }
        ),
    ]


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'start_time', 'end_date', 'end_time', 'house', ]
