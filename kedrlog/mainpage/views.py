from core.models import Company
from django.shortcuts import render
from mainpage.models import (ContentBlockBooking, ContentBlockInfrastructure,
                             ContentBlockMain, ContentBlockService,
                             ContentBlockYandexMap)

COMPANY = Company.objects.get(active=True)


def index(request):
    """Метод главной страницы."""
    template = 'mainpage/index.html'

    content_block_main = ContentBlockMain.objects.get(active=True)
    content_block_infra = ContentBlockInfrastructure.objects.get(active=True)
    content_block_service = ContentBlockService.objects.get(active=True)
    content_block_yandex_map = ContentBlockYandexMap.objects.get(active=True)
    content_block_booking = ContentBlockBooking.objects.get(active=True)

    min_cost, min_time, include_guests = (dict() for _ in range(3))
    for house in content_block_booking.houseshowbooking_set.all():
        if house.house.rate_house.filter(active=True).exists():
            min_cost[house.house.pk] = round(house.house.rate_house.get(active=True).price)
            include_guests[house.house.pk] = house.house.rate_house.get(active=True).guests_in_price
            min_time[house.house.pk] = house.house.rate_house.get(active=True).min_time

    context = {
        'company': COMPANY,
        'content_block_main': content_block_main,
        'content_block_infra': content_block_infra,
        'content_block_service': content_block_service,
        'content_block_yandex_map': content_block_yandex_map,
        'content_block_booking': content_block_booking,
        'min_cost': min_cost,
        'min_time': min_time,
        'include_guests': include_guests,
    }
    return render(request, template, context)
