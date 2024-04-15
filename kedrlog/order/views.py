import decimal
import json

from bitrix24 import Bitrix24
from bitrix24.exceptions import BitrixError
from common.views import user_get_or_create_in_site, contact_get_or_create_in_b24
from core.models import (AdditionalServices, Company, House, Rate, Reserve, ReserveServices, SettingsBitrix24,
                         SettingsSite)
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

User = get_user_model()
COMPANY = None # Company.objects.get(active=True)


def index(request):
    """Метод главной страницы."""
    template = 'order/index.html'

    if request.method != 'POST':
        return render(request, 'error.html', {'error_name': 'Неизвестный тип запроса'})
    if not all([True if param in request.POST else False for param in ['house', 'date', 'duration']]):
        return render(request, 'error.html', {'error_name': 'Ошибка'})

    settings_site = get_object_or_404(SettingsSite, active=True)
    if settings_site.reserve_closed_all and not request.user.is_superuser:
        return render(request, 'order/reserve_closed.html', {'company': COMPANY})
    if settings_site.reserve_closed and not request.user.is_superuser and not request.user.is_staff:
        return render(request, 'order/reserve_closed.html', {'company': COMPANY})

    house = get_object_or_404(House, pk=request.POST.get('house'))
    date = timezone.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
    duration = int(request.POST.get('duration'))
    rate = house.rate_house.get(active=True)
    price_house = rate.get_price(date)
    price_house_tomorrow = rate.get_price(date + timezone.timedelta(days=1))

    start_date_time_busy, start_date_time_allow = Reserve.get_start_busy_and_allow(date, house, duration)

    additional_services = AdditionalServices.objects.filter(active=True)

    date_time_range = [{'print': f'{i}:00', 'value': timezone.datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
                        + timezone.timedelta(hours=i)} for i in range(24)]

    context = {
        'company': COMPANY,
        'house': house,
        'start_date': date,
        'duration': duration,
        'start_date_time_busy': start_date_time_busy,
        'start_date_time_allow': start_date_time_allow,
        'rate': rate,
        'price_house': price_house,
        'price_house_tomorrow': price_house_tomorrow,
        'now_date': timezone.datetime.now(),
        'date_time_range': date_time_range,
        'str_start_stop': {'start': [1, 7, 13, 19], 'stop': [6, 12, 18, 24]},
        'additional_services': additional_services
    }
    return render(request, template, context)


# def update_start_date_time_table(request):
#     """Метод обновления таблицы выбора времени."""
#     if request.method != 'POST':
#         return JsonResponse({'result': False, 'error': 'Неизвестный тип запроса'})
#     house = get_object_or_404(House, pk=request.POST.get('house'))
#     date = timezone.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
#     duration = int(request.POST.get('duration'))
#     print(date)
#
#     start_date_time_busy, start_date_time_allow = Reserve.get_start_busy_and_allow(date, house, duration)
#
#     return JsonResponse({
#         'result': True,
#         'start_date_time_busy': list(start_date_time_busy),
#         'start_date_time_allow': list(start_date_time_allow)
#     })


def update_total_section_house(request):
    """Метод для обновления таблицы Информация по заказу при выборе парной."""

    if request.method != 'POST':
        return JsonResponse({'result': False, 'error': 'Неизвестный тип запроса'})
    start_date = request.POST.get('start_date')
    start_time = request.POST.get('start_time')
    start_date_time = timezone.datetime.strptime(start_date + ' ' + start_time, "%Y-%m-%d %H:%M")
    duration = timezone.timedelta(hours=int(request.POST.get('duration')))
    end_date_time = start_date_time + duration
    house = get_object_or_404(House, pk=request.POST.get('house_id'))
    house_string = (f'Аренда {house.name} c {start_date_time.strftime("%d.%m.%Y %H:%M")} по '
                    f'{end_date_time.strftime("%d.%m.%Y %H:%M")}')
    rate = house.rate_house.get(active=True)
    # Выясняем цену по прайсу с учетом перехода на следующий день
    if start_date_time.date() != end_date_time.date():
        delta_start_day = end_date_time.replace(hour=0) - start_date_time
        delta_end_day = end_date_time - end_date_time.replace(hour=0)
        house_price = rate.get_price(start_date_time) * decimal.Decimal(delta_start_day.total_seconds() / 3600)
        house_price += rate.get_price(end_date_time) * decimal.Decimal(delta_end_day.total_seconds() / 3600)
    else:
        house_price = rate.get_price(start_date_time) * int(request.POST.get('duration'))
    return JsonResponse({'result': True, 'house_string': house_string, 'house_price': f'{house_price}'})


def update_total_section_service(request):
    """Метод для обновления таблицы Информация по заказу при выборе дополнительных услуг."""

    if request.method != 'POST':
        return JsonResponse({'result': False, 'error': 'Неизвестный тип запроса'})
    service_id = request.POST.get('service_id')
    quantity = request.POST.get('quantity')
    service = get_object_or_404(AdditionalServices, pk=service_id)
    price = service.price * int(quantity)
    return JsonResponse({'result': True, 'service_name': service.name, 'service_price': f'{price}'})


def new(request):
    """Метод для создания нового заказа."""

    def deal_create_in_b24(contact_id, settings, order, b24):
        """Метод, который создает сделку в Битрикс24."""
        # Создаем сделку в Б24
        duration_s = order.duration * 3600
        start_date_time = order.start_date_time
        start_date = start_date_time.date()
        end_date_time = order.end_date_time
        end_date = end_date_time.date()
        start_date_time_str = start_date_time.strftime("%d.%m.%Y %H:%M:%S")
        start_date_str = start_date_time.strftime("%d.%m.%Y")
        start_time_str = start_date_time.strftime("%H:%M")
        end_time_str = end_date_time.strftime("%H:%M")
        title = f'Онлайн {start_date_str} {start_time_str}-{end_time_str} {order.house} {order.user.get_full_name()}'
        fields = {
            'TITLE': title,
            'TYPE_ID': 'SALE',
            'STAGE_ID': settings.stage_id_for_deal_adding,
            'OPENED': 'Y',
            'CONTACT_ID': contact_id,
            'ASSIGNED_BY_ID': settings.responsible_by_default,
            settings.reserve_field_code_b24: ([f'resource|{order.house.id_b24}|{start_date_time_str}|'
                                               f'{duration_s}|Аренда парной {order.house}']),
            settings.is_reserve_site_field_code_b24: 'Y'
            # #тип_ресурса#|#ID_ресурса#|#дата_время_начала#|#длительность_в_секундах#|#название_услуги#
        }
        deal_id = b24.callMethod('crm.deal.add', fields=fields)
        if deal_id:
            order.deal_id_b24 = deal_id
            order.send_to_bitrix = True
            order.save()
        # Добавляем в сделку главный товар
        rate = Rate.objects.get(active=True, house=order.house)

        data = []
        if (start_date != end_date) and (rate.is_day_of(start_date) != rate.is_day_of(end_date)):
            data.append({
                rate.is_day_of(start_date): (end_date_time.replace(hour=0) - start_date_time).total_seconds() / 3600
            })
            data.append({
                rate.is_day_of(end_date): order.duration - ((end_date_time.replace(hour=0)
                                                             - start_date_time).total_seconds() / 3600)
            })
        else:
            data.append({
                rate.is_day_of(start_date): order.duration
            })
        for elem in data:
            fields = {
                'ownerId': deal_id,
                'ownerType': 'D',
                'productId': (rate.id_rent_weekend_in_catalog_b24 if list(elem.keys())[0]
                              else rate.id_rent_in_catalog_b24),
                'price': str(rate.price_weekend if list(elem.keys())[0] else rate.price),
                'quantity': str(list(elem.values())[0]),
            }
            try:
                b24.callMethod('crm.item.productrow.add', fields=fields)
            except BitrixError:
                pass
        # Добавляем в сделку дополнительные товары
        for service in ReserveServices.objects.filter(reserve=order):
            fields = {
                'ownerId': deal_id,
                'ownerType': 'D',
                'productId': service.additional_service.id_catalog_b24,
                'price': str(service.additional_service.price),
                'quantity': service.quantity,
            }
            result_set_prods = b24.callMethod('crm.item.productrow.add', fields=fields)
            if result_set_prods and 'productRow' in result_set_prods:
                service.id_b24 = result_set_prods.get('productRow').get('id')
                service.save()
        # Обработка дополнительного гостя
        if order.count_guests > rate.guests_in_price:
            fields = {
                'ownerId': deal_id,
                'ownerType': 'D',
                'productId': rate.id_additional_guest_in_catalog_b24,
                'price': str(rate.additional_guest_price),
                'quantity': order.count_guests - rate.guests_in_price,
            }
            try:
                b24.callMethod('crm.item.productrow.add', fields=fields)
            except BitrixError:
                pass
        # Двигаем на стадию Онлайн Бронирование (только так в Б24 корректно отрабатывают роботы)
        fields = {
            'STAGE_ID': 6,
        }
        b24.callMethod('crm.deal.update', id=deal_id, fields=fields)

        # services = [{"PRODUCT_ID": service.additional_service.id_catalog_b24,
        #              "PRICE": str(service.additional_service.price),
        #              "QUANTITY": str(service.quantity)} for service in ReserveServices.objects.filter(reserve=order)]
        # print(f'{services=}')
        # result_set_prods = b24.callMethod('crm.deal.productrows.set', id=deal_id, rows=services)

        return True

    def main():
        start_date_time = request.POST.get('start_date_time')
        start_date_time = timezone.datetime.strptime(start_date_time, "%Y-%m-%d %H:%M").replace(
            tzinfo=timezone.get_current_timezone())
        duration = int(request.POST.get('duration'))
        end_date_time = start_date_time + timezone.timedelta(hours=duration)
        count_guests = int(request.POST.get('count_guests'))
        user_first_name = request.POST.get('user_first_name')
        user_last_name = request.POST.get('user_last_name')
        user_email = request.POST.get('user_email')
        user_phone = request.POST.get('user_phone')
        user = request.user
        total_price = decimal.Decimal(request.POST.get('total_price'))
        house = get_object_or_404(House, pk=int(request.POST.get('house_pk')))
        additional_services = json.loads(request.POST.get('additional_services'))
        settings = SettingsBitrix24.objects.get(active=True)

        # Проверяем пользователя на сайте
        if not user.is_authenticated:
            user = user_get_or_create_in_site(user_phone, user_email, user_first_name, user_last_name)

        # Проверяем пользователя в Битрикс24
        webhook = settings.webhook
        b24 = Bitrix24(webhook)
        if user.id_b24:
            try:
                contact = b24.callMethod('crm.contact.get', id=user.id_b24)
            except BitrixError:
                contact = contact_get_or_create_in_b24(b24, user, settings.responsible_by_default)
        else:
            contact = contact_get_or_create_in_b24(b24, user, settings.responsible_by_default)

        if not Reserve.check_reserve(start_date_time, house, duration):
            return {'result': False, 'error': 'Не удалось создать заказ. Выбранное вами время уже забронировано. '
                                              'Обновите страницу и попробуйте снова.'}

        # Создаем заказ (бронирование) на сайте
        try:
            order = Reserve.objects.create(start_date_time=start_date_time, end_date_time=end_date_time,
                                           duration=duration, user=user, house=house, count_guests=count_guests,
                                           cost=total_price)
            for additional_service in additional_services:
                id_service = list(additional_service.keys())[0]
                service = AdditionalServices.objects.get(id=id_service)
                ReserveServices.objects.create(reserve=order, additional_service=service,
                                               quantity=int(additional_service.get(id_service)))
        except ValueError as ex:
            return {'result': False, 'error': f'Не удалось создать заказ. Подробности ошибки {ex}'}

        # Создаем сделку в Битрикс24
        deal_create_in_b24(contact.get('ID'), settings, order, b24)
        return {'result': True}

    if request.method != 'POST':
        return JsonResponse({'result': False, 'error': 'Неизвестный тип запроса'})
    return JsonResponse(main())


def update(request, deal_id):
    """Метод для установки оплаты в заказе."""

    rest_key = SettingsBitrix24.objects.get(active=True).get_rest_key()
    key_url = request.GET.get('key')
    if rest_key != key_url:
        return HttpResponse(status=401)

    order = get_object_or_404(Reserve, deal_id_b24=deal_id)
    order.paid = True
    order.save()

    return HttpResponse(status=200)


def delete(request, deal_id):
    """Метод для удаления бронирования."""

    rest_key = SettingsBitrix24.objects.get(active=True).get_rest_key()
    key_url = request.GET.get('key')
    if rest_key != key_url:
        return HttpResponse(status=401)

    get_object_or_404(Reserve, deal_id_b24=deal_id).delete()
    return HttpResponse(status=200)
