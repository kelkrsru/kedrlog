from django.shortcuts import get_object_or_404
from django.utils import timezone
from bitrix24 import Bitrix24

from core.models import Reserve, House, SettingsBitrix24, SettingsSite


def get_busy_time_for_date(house_id, reserve_date):
    """Метод получения занятого времени для парной на определенную дату."""
    start_date_time_busy = set()
    tz = timezone.get_current_timezone()
    settings_site = get_object_or_404(SettingsSite, active=True)
    start_date_interval = timezone.datetime.combine(reserve_date - timezone.timedelta(days=1),
                                                    timezone.datetime.min.time(), tz)
    end_date_interval = timezone.datetime.combine(reserve_date + timezone.timedelta(days=1),
                                                  timezone.datetime.max.time(), tz)
    reserve_date_interval = [start_date_interval, end_date_interval]

    reserve_house = House.objects.get(id=house_id)
    reserves = Reserve.objects.filter(house=reserve_house, start_date_time__range=reserve_date_interval)
    for reserve in reserves:
        start_date_time = timezone.make_naive(reserve.start_date_time, tz)
        end_date_time = timezone.make_naive(reserve.end_date_time, tz)

        while start_date_time < end_date_time + timezone.timedelta(minutes=reserve_house.cleaning):
            start_date_time_busy.add(start_date_time)
            start_date_time += timezone.timedelta(minutes=settings_site.reserve_show_interval)

    webhook = SettingsBitrix24.objects.get(active=True).webhook
    b24 = Bitrix24(webhook)
    bookings = b24.callMethod('calendar.resource.booking.list',
                              filter={"resourceTypeIdList": [reserve_house.id_b24],
                                      "from": start_date_interval.strftime('%y-%m-%d'),
                                      "to": end_date_interval.strftime('%y-%m-%d')})
    for booking in bookings:
        start_date_time = timezone.datetime.strptime(booking.get("DATE_FROM"), "%d.%m.%Y %H:%M:%S")
        end_date_time = timezone.datetime.strptime(booking.get("DATE_TO"), "%d.%m.%Y %H:%M:%S")
        while start_date_time < end_date_time + timezone.timedelta(
                minutes=reserve_house.cleaning + 1):  # +1, потому что Битрикс возвращает Н:59
            start_date_time_busy.add(start_date_time)
            start_date_time += timezone.timedelta(minutes=settings_site.reserve_show_interval)

    return start_date_time_busy


def check_reserve(house_id, start_date_time, duration):
    """Метод проверки времени на занятость."""
    print(f'{type(start_date_time)=}')
    print(f'{start_date_time=}')
    reserve_date = start_date_time.date()
    reserve_house = House.objects.get(id=house_id)
    start_date_time_busy = get_busy_time_for_date(house_id, reserve_date)
    print(f'{start_date_time_busy}')
    reserve_interval = [start_date_time + timezone.timedelta(minutes=x) for x in range(duration
                                                                                       + reserve_house.cleaning)]

    for date_time in reserve_interval:
        date_time = date_time.replace(tzinfo=None)
        if date_time in start_date_time_busy:
            return False
    return True
