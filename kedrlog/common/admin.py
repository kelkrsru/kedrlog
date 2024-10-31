#
# from .models import Portals
#
#
# class PortalsAdmin(admin.ModelAdmin):
#     list_display = (
#         'pk',
#         'member_id',
#         'name',
#         'auth_id_create_date',
#     )
#
#
# admin.site.register(Portals, PortalsAdmin)
from common.models import Badge, GalleryItem
from django.contrib import admin


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', ]
