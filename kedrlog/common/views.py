# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from pybitrix24 import Bitrix24
#
# from .models import Portals
#
#
# @csrf_exempt
# def install(request):
#     """Метод установки приложения"""
#
#     try:
#         portal: Portals = Portals.objects.get(
#             member_id=request.POST['member_id'])
#         portal.auth_id = request.POST['AUTH_ID']
#         portal.refresh_id = request.POST['REFRESH_ID']
#         portal.save()
#     except Portals.DoesNotExist:
#         portal: Portals = Portals.objects.create(
#             member_id=request.POST['member_id'],
#             name=request.GET.get('DOMAIN'),
#             auth_id=request.POST['AUTH_ID'],
#             refresh_id=request.POST['REFRESH_ID']
#         )
#     try:
#         SettingsPortal.objects.get(portal=portal)
#     except SettingsPortal.DoesNotExist:
#         SettingsPortal.objects.create(portal=portal)
#
#     bx24 = Bitrix24(portal.name)
#     bx24._access_token = portal.auth_id
#     bx24._refresh_token = portal.refresh_id
#
#     return render(request, 'core/install.html')
