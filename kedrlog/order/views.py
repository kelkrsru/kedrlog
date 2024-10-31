import decimal

import pandas as pd
from bitrix24 import Bitrix24
from bitrix24.exceptions import BitrixError
from common.views import contact_get_or_create_in_b24, user_get_or_create_in_site
from core.models import Company, House, Rate, Reserve, ReserveServices, SettingsBitrix24, SettingsSite
from core.reserve import check_reserve, get_busy_time_for_date
from django.contrib.auth import get_user_model
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()
COMPANY = Company.objects.get(active=True)


def index(request):
    """Метод главной страницы."""
    template = 'order/index-new.html'

    if request.method == 'GET':
        start_date = timezone.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count_guests = 4
    elif request.method == 'POST' and all([True if param in request.POST else False for param in
                                           ['start_date', 'count_guests']]):
        start_date = timezone.datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
        count_guests = int(request.POST.get('count_guests'))
    else:
        return render(request, 'error.html', {'error_name': 'Не все параметры переданы. Обратитесь к администратору.'})

    settings_site = get_object_or_404(SettingsSite, active=True)
    if settings_site.reserve_closed_all and not request.user.is_superuser:
        return render(request, 'order/reserve_closed.html', {'company': COMPANY})
    if settings_site.reserve_closed and not request.user.is_superuser and not request.user.is_staff:
        return render(request, 'order/reserve_closed.html', {'company': COMPANY})

    houses = House.objects.filter(active=True)
    max_guests = Rate.objects.filter(id__in=houses.values('house_rates')).aggregate(Max("max_guest"))
    now_date_time = timezone.datetime.now()

    # additional_services = AdditionalServices.objects.filter(active=True)
    start_date_time_busy = {}
    for house in houses:
        start_date_time_busy[house.id] = get_busy_time_for_date(house.id, start_date)

    date_time_range = [
        {'print': f'{i.time().strftime("%H:%M")}', 'value': i, 'str_value': i.strftime('%Y-%m-%d %H:%M')} for i in
        pd.date_range(start_date + timezone.timedelta(hours=settings_site.reserve_start_time),
                      start_date + timezone.timedelta(hours=settings_site.reserve_end_time,
                                                      minutes=settings_site.reserve_show_interval),
                      freq=f'{settings_site.reserve_show_interval}min')]

    context = {
        'company': COMPANY,
        'houses': houses,
        'start_date': start_date.date(),
        'max_guests': max_guests.get('max_guest__max'),
        'date_time_range': date_time_range,
        'count_guests': count_guests,
        # 'additional_services': additional_services,
        'start_date_time_busy': start_date_time_busy,
        'now_date_time': now_date_time
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

# def update_total_section_house(request):
#     """Метод для обновления таблицы Информация по заказу при выборе парной."""
#
#     if request.method != 'POST':
#         return JsonResponse({'result': False, 'error': 'Неизвестный тип запроса'})
#     start_date = request.POST.get('start_date')
#     start_time = request.POST.get('start_time')
#     start_date_time = timezone.datetime.strptime(start_date + ' ' + start_time, "%Y-%m-%d %H:%M")
#     duration = timezone.timedelta(hours=int(request.POST.get('duration')))
#     end_date_time = start_date_time + duration
#     house = get_object_or_404(House, pk=request.POST.get('house_id'))
#     house_string = (f'Аренда {house.name} c {start_date_time.strftime("%d.%m.%Y %H:%M")} по '
#                     f'{end_date_time.strftime("%d.%m.%Y %H:%M")}')
#     rate = house.rate_house.get(active=True)
#     # Выясняем цену по прайсу с учетом перехода на следующий день
#     if start_date_time.date() != end_date_time.date():
#         delta_start_day = end_date_time.replace(hour=0) - start_date_time
#         delta_end_day = end_date_time - end_date_time.replace(hour=0)
#         house_price = rate.get_price(start_date_time) * decimal.Decimal(delta_start_day.total_seconds() / 3600)
#         house_price += rate.get_price(end_date_time) * decimal.Decimal(delta_end_day.total_seconds() / 3600)
#     else:
#         house_price = rate.get_price(start_date_time) * int(request.POST.get('duration'))
#     return JsonResponse({'result': True, 'house_string': house_string, 'house_price': f'{house_price}'})


# def update_total_section_service(request):
#     """Метод для обновления таблицы Информация по заказу при выборе дополнительных услуг."""
#
#     if request.method != 'POST':
#         return JsonResponse({'result': False, 'error': 'Неизвестный тип запроса'})
#     service_id = request.POST.get('service_id')
#     quantity = request.POST.get('quantity')
#     service = get_object_or_404(AdditionalServices, pk=service_id)
#     price = service.price * int(quantity)
#     return JsonResponse({'result': True, 'service_name': service.name, 'service_price': f'{price}'})


@xframe_options_exempt
@csrf_exempt
def get_price_for_date(request):
    """Получить цену тарифа по дате."""
    if request.method != 'POST':
        return JsonResponse({'result': False, 'error': 'Неизвестный тип запроса'})
    rate_id = int(request.POST.get('rate_id'))
    start_date = timezone.datetime.strptime(request.POST.get('date'), "%d.%m.%Y").date()
    duration = int(request.POST.get('duration'))
    count_guests = int(request.POST.get('count_guests'))
    username = request.user.username

    settings_site = get_object_or_404(SettingsSite, active=True)
    duration = decimal.Decimal(duration / settings_site.reserve_interval)
    rate = Rate.objects.get(id=rate_id)
    price = rate.get_price(start_date)
    total_price_rent = round(price * duration, 2)
    additional_guest_price = 0

    if count_guests > rate.guests_in_price:
        additional_guest_price = round(rate.additional_guest_price * (count_guests - rate.guests_in_price), 2)
    total_price = total_price_rent + additional_guest_price

    return JsonResponse({'result': True, 'price': price, 'total_price_rent': total_price_rent,
                         'additional_guest_price': additional_guest_price, 'total_price': total_price,
                         'username': username})


@xframe_options_exempt
@csrf_exempt
def get_settings_interval(request):
    """Метод для получения текущих настроек интервала бронирования."""
    if request.method != 'GET':
        return JsonResponse({'result': False, 'error': 'Неизвестный тип запроса'})
    settings_site = get_object_or_404(SettingsSite, active=True)
    return JsonResponse({'result': True, 'reserve_interval': settings_site.reserve_interval,
                         'reserve_show_interval': settings_site.reserve_show_interval})


@xframe_options_exempt
@csrf_exempt
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
        rate_id = int(request.POST.get('rate_id'))
        end_date_time = start_date_time + timezone.timedelta(minutes=duration)
        count_guests = int(request.POST.get('count_guests'))
        user_first_name = request.POST.get('user_first_name')
        user_last_name = request.POST.get('user_last_name')
        user_email = request.POST.get('user_email')
        user_phone = request.POST.get('user_phone')
        user = request.user
        total_price = decimal.Decimal(request.POST.get('total_price'))
        house = get_object_or_404(House, pk=int(request.POST.get('house_pk')))
        # additional_services = json.loads(request.POST.get('additional_services'))
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

        if not check_reserve(house.id, start_date_time, duration):
            return {'result': False, 'error': 'Не удалось создать заказ. Выбранное вами время уже забронировано. '
                                              'Обновите страницу и попробуйте снова.'}

        # Создаем заказ (бронирование) на сайте
        try:
            order = Reserve.objects.create(start_date_time=start_date_time, end_date_time=end_date_time,
                                           duration=duration, user=user, house=house, count_guests=count_guests,
                                           cost=total_price, rate_id=rate_id)
            # for additional_service in additional_services:
            #     id_service = list(additional_service.keys())[0]
            #     service = AdditionalServices.objects.get(id=id_service)
            #     ReserveServices.objects.create(reserve=order, additional_service=service,
            #                                    quantity=int(additional_service.get(id_service)))
        except ValueError as ex:
            return {'result': False, 'error': f'Не удалось создать заказ. Подробности ошибки {ex}'}

        # Создаем сделку в Битрикс24
        # deal_create_in_b24(contact.get('ID'), settings, order, b24)
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
