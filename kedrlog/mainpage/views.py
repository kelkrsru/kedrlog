from django.db.models import Min
from django.shortcuts import render

from core.models import Company, House
from mainpage.models import ContentBlockMain, ContentBlockInfrastructure, ContentBlockService, ContentBlockYandexMap, \
    ContentBlockBooking


def index(request):
    """Метод главной страницы."""
    template = 'mainpage/index.html'

    company = Company.objects.get(active=True)
    content_block_main = ContentBlockMain.objects.get(active=True)
    content_block_infra = ContentBlockInfrastructure.objects.get(active=True)
    content_block_service = ContentBlockService.objects.get(active=True)
    content_block_yandex_map = ContentBlockYandexMap.objects.get(active=True)
    content_block_booking = ContentBlockBooking.objects.get(active=True)

    min_cost = {}
    for house in content_block_booking.houseshowbooking_set.all():
        if house.house.rate_house.filter(active=True).exists():
            print(house.house.rate_house.get(active=True).rate.aggregate(Min('cost')))
            min_cost[house.house.pk] = house.house.rate_house.get(active=True).rate.aggregate(Min('cost')).get(
                'cost__min')

    context = {
        'company': company,
        'content_block_main': content_block_main,
        'content_block_infra': content_block_infra,
        'content_block_service': content_block_service,
        'content_block_yandex_map': content_block_yandex_map,
        'content_block_booking': content_block_booking,
        'min_cost': min_cost
    }
    response = render(request, template, context)
    return response
