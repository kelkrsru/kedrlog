from core.models import Company
from django.shortcuts import render
from mainpage.models import (ContentBlockBooking, ContentBlockInfrastructure,
                             ContentBlockMain, ContentBlockService,
                             ContentBlockYandexMap, ToastMain)

COMPANY = Company.objects.get(active=True)


def index(request):
    """Метод главной страницы."""
    template = 'mainpage/index.html'

    def _create_or_update_min(dict_obj, key, value):
        if key not in dict_obj:
            dict_obj[key] = value
            return
        dict_obj[key] = min(value, dict_obj[key])

    content_block_main = ContentBlockMain.objects.get(active=True)
    content_block_infra = ContentBlockInfrastructure.objects.get(active=True)
    content_block_service = ContentBlockService.objects.get(active=True)
    content_block_yandex_map = ContentBlockYandexMap.objects.get(active=True)
    content_block_booking = ContentBlockBooking.objects.get(active=True)
    toast_main = ToastMain.objects.filter(active=True).first() if ToastMain.objects.filter(active=True) else 0

    min_cost, min_time, include_guests = (dict() for _ in range(3))
    for element in content_block_booking.houseshowbooking_set.all():
        if not element.house.house_rates.all().exists():
            continue
        for rate in element.house.house_rates.all():
            _create_or_update_min(min_cost, element.house.pk, rate.get_min_price())
            _create_or_update_min(include_guests, element.house.pk, rate.guests_in_price)
            _create_or_update_min(min_time, element.house.pk, rate.min_time)

    context = {
        'company': COMPANY,
        'content_block_main': content_block_main,
        'toast_main': toast_main,
        'content_block_infra': content_block_infra,
        'content_block_service': content_block_service,
        'content_block_yandex_map': content_block_yandex_map,
        'content_block_booking': content_block_booking,
        'min_cost': {key: str(round(value)) for key, value in min_cost.items()},
        'min_time': min_time,
        'include_guests': include_guests,
    }
    return render(request, template, context)
