from urllib.parse import urlparse

from bitrix24 import Bitrix24
from ckeditor.fields import RichTextField
from common.models import CreatedModel, GalleryItem, Seo
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

User = get_user_model()


class Company(CreatedModel, Seo):
    """Класс для описания основных параметров компании."""

    active = models.BooleanField(
        verbose_name='Активность',
        help_text='Выберите компанию в качестве основной. Текущая основная компания потеряет этот статус',
        default=False
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование',
        help_text='Укажите наименование компании для отображения в заголовках сайта'
    )
    phone = models.CharField(
        max_length=255,
        verbose_name='Основной номер телефона',
        help_text='Основной телефон компании, который отображается в верхнем меню сайта и в подвале сайта'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес',
        help_text='Адрес компании, который отображается в подвале сайта'
    )
    logo_header = models.ImageField(
        verbose_name='Файл логотипа компании в шапке',
        help_text='Файл логотипа компании в шапке в формате png, рекомендованный размер 60x60 px с прозрачным фоном',
        blank=True,
        upload_to='img/logo/'
    )
    logo_footer = models.ImageField(
        verbose_name='Файл логотипа компании в подвале',
        help_text='Файл логотипа компании в подвале в формате png, рекомендованный размер 60x60 px с прозрачным фоном',
        blank=True,
        upload_to='img/logo/'
    )
    favicon = models.ImageField(
        verbose_name='Файл favicon',
        help_text='Файл favicon в формате ico',
        blank=True,
        upload_to='img/favicon/'
    )
    social_networks = models.ManyToManyField(
        'SocialNetworks',
        verbose_name='Социальные сети',
        related_name='company_social_networks',
        blank=True
    )

    def save(self, *args, **kwargs):
        if self.active:
            Company.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class House(CreatedModel):
    """Класс Парная."""
    active = models.BooleanField(
        verbose_name='Активность',
        default=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование',
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Описание',
    )
    floor = models.PositiveSmallIntegerField(
        verbose_name='Количество этажей',
        default=1
    )
    restroom = models.PositiveSmallIntegerField(
        verbose_name='Количество комнат отдыха',
        default=1
    )
    max_guests = models.PositiveSmallIntegerField(
        verbose_name='Максимальное количество гостей',
        default=10
    )
    cost_include = models.CharField(
        max_length=128,
        verbose_name='Стоимость включает',
        blank=True
    )
    cleaning = models.PositiveSmallIntegerField(
        verbose_name='Время на уборку в часах',
        help_text='Если 0, то уборка отсутствует',
        default=0
    )
    photo_main = models.ForeignKey(
        GalleryItem,
        verbose_name='Основное фото',
        on_delete=models.PROTECT,
        related_name='house_photo_main'
    )
    gallery_items = models.ManyToManyField(
        GalleryItem,
        verbose_name='Элементы галереи',
        related_name='house_gallery_item'
    )
    additional_features = models.ManyToManyField(
        'AdditionalFeatures',
        verbose_name='Дополнительные характеристики',
        related_name='house_additional_features',
    )
    id_b24 = models.PositiveSmallIntegerField(
        verbose_name='ID ресурса бронирования в Б24',
        help_text='ID ресурса бронирования в Битрикс24',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Парная'
        verbose_name_plural = 'Парные'


class AdditionalFeatures(CreatedModel):
    """Дополнительные характеристики для парных."""
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование',
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Описание',
        help_text='Выводится на странице бронирования'
    )
    icon = models.ImageField(
        verbose_name='Иконка',
        help_text='Иконка в формате png 64*64 px',
        upload_to='img/houses/icons/'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дополнительная характеристика'
        verbose_name_plural = 'Дополнительные характеристики'


class Rate(CreatedModel):
    """Класс Тариф."""
    active = models.BooleanField(
        verbose_name='Активность',
        help_text='Выбор активного тарифа для Парной',
        default=False
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=255,
        blank=True
    )
    house = models.ForeignKey(
        House,
        verbose_name='Парная',
        related_name='rate_house',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        verbose_name='Цена',
        help_text='Цена за 1 час в обычный день пн, вт, ср, чт',
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    price_weekend = models.DecimalField(
        verbose_name='Цена выходного дня',
        help_text='Цена за 1 час в выходной день пт, сб, вс и праздники',
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    min_time = models.PositiveSmallIntegerField(
        verbose_name='Минимальное время парения',
        help_text='Минимальное время парения в часах',
        default=3
    )
    guests_in_price = models.PositiveSmallIntegerField(
        verbose_name='Количество гостей, включенных в стоимость',
        default=6
    )
    additional_guest_price = models.DecimalField(
        verbose_name='Доплата за дополнительного гостя',
        help_text='Доплата за дополнительного гостя за все время',
        max_digits=10,
        decimal_places=2,
        default=1000.00,
    )
    id_rent_in_catalog_b24 = models.PositiveIntegerField(
        verbose_name='ID товара аренды в каталоге Битрикс24',
        blank=True,
        null=True
    )
    id_rent_weekend_in_catalog_b24 = models.PositiveIntegerField(
        verbose_name='ID товара аренды выходного дня в каталоге Битрикс24',
        blank=True,
        null=True
    )
    id_additional_guest_in_catalog_b24 = models.PositiveIntegerField(
        verbose_name='ID товара дополнительного гостя в каталоге Битрикс24',
        blank=True,
        null=True
    )

    @staticmethod
    def is_day_of(date):
        """Проверить день на праздничный/выходной."""
        if date.weekday() in [4, 5, 6] or WeekendDays.objects.filter(date=date):
            return True
        return False

    def get_price(self, date):
        """Получить цену, исходя из буднего/праздничного/выходного дня."""
        if self.is_day_of(date):
            return self.price_weekend
        return self.price

    def save(self, *args, **kwargs):
        if self.active:
            Rate.objects.filter(active=True, house=self.house).update(active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'


class Reserve(CreatedModel):
    """Класс Бронирование."""
    start_date_time = models.DateTimeField(
        verbose_name='Дата и время начала бронирования',
    )
    end_date_time = models.DateTimeField(
        verbose_name='Дата и время окончания бронирования',
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name='Продолжительность бронирования',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
    )
    house = models.ForeignKey(
        House,
        verbose_name='Парная',
        on_delete=models.PROTECT,
    )
    count_guests = models.PositiveSmallIntegerField(
        verbose_name='Количество человек',
        validators=[MinValueValidator(1, 'Количество человек не может быть меньше 0 или 0'), ],
    )
    cost = models.DecimalField(
        verbose_name='Сумма',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    additional_services = models.ManyToManyField(
        'AdditionalServices',
        verbose_name='Дополнительные услуги',
        through='ReserveServices',
        blank=True,
    )
    paid = models.BooleanField(
        verbose_name='Оплачено',
        default=False,
    )
    send_to_bitrix = models.BooleanField(
        verbose_name='Отправлено в Битрикс24',
        default=False,
    )
    deal_id_b24 = models.PositiveIntegerField(
        verbose_name='ID сделки в Битрикс24',
        help_text='ID сделки в Битрикс24',
        unique=True,
        blank=True,
        null=True
    )

    @classmethod
    def _get_start_busy(cls, reserve_date, reserve_house):
        """Метод, который формирует множество из времени начало парения, уже занятых за переданную дату."""
        start_date_time_busy = set()
        tz = timezone.get_current_timezone()
        start_date_interval = timezone.datetime.combine(reserve_date - timezone.timedelta(days=1),
                                                        timezone.datetime.min.time(), tz)
        end_date_interval = timezone.datetime.combine(reserve_date + timezone.timedelta(days=1),
                                                      timezone.datetime.max.time(), tz)
        reserve_date_interval = [start_date_interval, end_date_interval]
        # Добавим все часы в занятые, которые вне расписания бронирования
        settings_site = SettingsSite.objects.get(active=True)
        reserve_start_time = timezone.datetime(reserve_date.year, reserve_date.month, reserve_date.day,
                                               hour=settings_site.reserve_start_time, minute=0, second=0)
        if settings_site.reserve_end_time != 24:
            reserve_end_time = timezone.datetime(reserve_date.year, reserve_date.month, reserve_date.day,
                                                 hour=settings_site.reserve_end_time, minute=0, second=0)
        else:
            reserve_end_time = timezone.datetime(reserve_date.year, reserve_date.month, reserve_date.day,
                                                 hour=23, minute=59, second=59)
        while reserve_start_time > timezone.datetime.combine(
                reserve_date - timezone.timedelta(days=1), timezone.datetime.max.time()):
            start_date_time_busy.add(reserve_start_time - timezone.timedelta(hours=1))
            reserve_start_time -= timezone.timedelta(hours=1)
        while reserve_end_time < timezone.datetime.combine(
                reserve_date + timezone.timedelta(days=1), timezone.datetime.min.time()):
            start_date_time_busy.add(reserve_end_time + timezone.timedelta(hours=1))
            reserve_end_time += timezone.timedelta(hours=1)

        reserves = cls.objects.filter(house=reserve_house, start_date_time__range=reserve_date_interval)
        for reserve in reserves:
            start_date_time = timezone.make_naive(reserve.start_date_time, tz)
            duration = reserve.duration
            for x in range(duration + reserve_house.cleaning):
                date_time_add = start_date_time + timezone.timedelta(hours=x)
                start_date_time_busy.add(date_time_add)

        webhook = SettingsBitrix24.objects.get(active=True).webhook
        b24 = Bitrix24(webhook)
        bookings = b24.callMethod('calendar.resource.booking.list',
                                  filter={"resourceTypeIdList": [reserve_house.id_b24],
                                          "from": start_date_interval.strftime('%y-%m-%d'),
                                          "to": end_date_interval.strftime('%y-%m-%d')})
        for booking in bookings:
            start_date_time = timezone.datetime.strptime(booking.get("DATE_FROM"), "%d.%m.%Y %H:%M:%S")
            end_date_time = timezone.datetime.strptime(booking.get("DATE_TO"), "%d.%m.%Y %H:%M:%S")
            while start_date_time < end_date_time + timezone.timedelta(hours=reserve_house.cleaning):
                start_date_time_busy.add(start_date_time)
                start_date_time += timezone.timedelta(hours=1)

        return start_date_time_busy

    @classmethod
    def _get_start_allow(cls, start_date_time_busy, duration, house_cleaning, reserve_date):
        """Метод, который формирует множество из времени начало парения, разрешенных для бронирования."""
        # timezone.timedelta(hours=(duration + house_cleaning))
        reserve_date = timezone.datetime.combine(reserve_date - timezone.timedelta(days=1),
                                                 timezone.datetime.min.time())
        date_time_range_3days = {reserve_date + timezone.timedelta(hours=i) for i in range(72)}

        start_date_time_allow = date_time_range_3days.difference(start_date_time_busy)
        start_date_time_allow = sorted(start_date_time_allow)
        i = 0
        while i < len(start_date_time_allow):
            reserve_interval = [start_date_time_allow[i] + timezone.timedelta(hours=x) for x in
                                range(duration + house_cleaning)]
            j = False
            for date_time in reserve_interval:
                if date_time in start_date_time_busy:
                    start_date_time_allow.pop(i)
                    j = True
                    break
            if not j:
                i += 1

        return set(start_date_time_allow)

    @staticmethod
    def _add_start_busy_not_min_intervals(start_date_time_busy, duration, house_cleaning):
        """Метод, который добавляет начало парения в занятое, если меньше минимального промежутка."""

        min_interval = timezone.timedelta(hours=(duration + house_cleaning))
        start_date_time_busy = sorted(start_date_time_busy)
        start_date_time_busy_temp = list()

        for i in range(len(start_date_time_busy) - 1):
            delta = start_date_time_busy[i + 1] - start_date_time_busy[i]
            if (delta <= min_interval) and (delta != timezone.timedelta(hours=1)):
                j = start_date_time_busy[i + 1]
                while j >= start_date_time_busy[i] + timezone.timedelta(hours=1):
                    j -= timezone.timedelta(hours=1)
                    start_date_time_busy_temp.append(j)
        start_date_time_busy += start_date_time_busy_temp

        return set(start_date_time_busy)

    @classmethod
    def get_start_busy_and_allow(cls, reserve_date, reserve_house, duration):
        start_date_time_busy = cls._get_start_busy(reserve_date, reserve_house)
        start_date_time_busy_temp = cls._add_start_busy_not_min_intervals(start_date_time_busy, duration,
                                                                          reserve_house.cleaning)
        start_date_time_allow = cls._get_start_allow(start_date_time_busy_temp, duration, reserve_house.cleaning,
                                                     reserve_date)

        return start_date_time_busy, start_date_time_allow

    @classmethod
    def check_reserve(cls, start_date_time, reserve_house, duration):
        """Метод проверки времени на занятость."""
        reserve_date = start_date_time.date()
        start_date_time_busy = cls._get_start_busy(reserve_date, reserve_house)
        reserve_interval = [start_date_time + timezone.timedelta(hours=x) for x in range(duration
                                                                                         + reserve_house.cleaning)]

        for date_time in reserve_interval:
            date_time = date_time.replace(tzinfo=None)
            if date_time in start_date_time_busy:
                return False
        return True

    def __str__(self):
        return f'Бронирование {self.house.name} с {self.start_date_time} по {self.end_date_time}'

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'


class AdditionalServices(CreatedModel):
    """Класс Дополнительные услуги."""

    class Measure(models.TextChoices):
        PIECE = 'piece', 'шт.'
        SERVICE = 'service', 'усл.'
        HOUR = 'hour', 'час'

        __empty__ = 'Не выбрано'

    active = models.BooleanField(
        verbose_name='Активность',
        default=True
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=255,
        blank=True
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    measure = models.CharField(
        verbose_name='Единицы измерения',
        max_length=20,
        choices=Measure.choices,
        default=Measure.__empty__
    )
    group = models.PositiveSmallIntegerField(
        verbose_name='Группа',
        help_text='Услуга/товар входит в группу. На странице бронирования можно будет выбрать только один из группы.',
        blank=True,
        null=True,
    )
    id_catalog_b24 = models.PositiveIntegerField(
        verbose_name='ID товара/услуги',
        help_text='ID товара/услуги в каталоге Битрикс24',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дополнительная услуга'
        verbose_name_plural = 'Дополнительные услуги'


class SpaServices(CreatedModel):
    """Класс Программы парения."""

    active = models.BooleanField(
        verbose_name='Активность',
        default=True
    )
    sort = models.PositiveSmallIntegerField(
        verbose_name='Сортировка',
        help_text='Чем меньше значение, тем выше будет запись',
        default=10
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=2048,
        blank=True
    )
    include = RichTextField(
        verbose_name='Программа включает',
        help_text='Что вас ждет в программе парения'
    )
    price = models.ManyToManyField(
        'PriceForSpaServices',
        verbose_name='Цена',
        blank=True,
        related_name='price_spa_services',
    )
    header_image = models.ImageField(
        verbose_name='Файл основного изображения',
        help_text='Изображение отображается в шапке карточки на странице Спа-программы',
        blank=True,
        upload_to='img/spa/'
    )
    id_catalog_b24 = models.PositiveIntegerField(
        verbose_name='ID товара/услуги',
        help_text='ID товара/услуги в каталоге Битрикс24',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Программа парения'
        verbose_name_plural = 'Программы парения'


class GiftCertificateType(CreatedModel):
    """Класс Типы подарочных сертификатов."""
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255
    )
    value = models.CharField(
        verbose_name='Значение',
        max_length=255
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип подарочного сертификата'
        verbose_name_plural = 'Типы подарочных сертификатов'


class GiftCertificate(CreatedModel):
    """Класс Подарочный сертификат."""
    class ColorText(models.TextChoices):
        WHITE = 'white', 'Белый'
        DARK = 'dark', 'Черный'
        SHADOW = 'shadow', 'Белый с черной обводкой'
        __empty__ = 'Не выбрано'

    active = models.BooleanField(
        verbose_name='Активность',
        default=True
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    type = models.ManyToManyField(
        GiftCertificateType,
        verbose_name='Тип',
        help_text='Тип подарочного сертификата',
        related_name='gift_certificates'
    )
    min_price = models.DecimalField(
        verbose_name='Минимальный номинал',
        help_text='Минимальный номинал сертификата',
        max_digits=10,
        decimal_places=2,
        default=1000
    )
    max_price = models.DecimalField(
        verbose_name='Максимальный номинал',
        help_text='Максимальный номинал сертификата',
        max_digits=10,
        decimal_places=2,
        default=1000000
    )
    step_price = models.DecimalField(
        verbose_name='Шаг',
        help_text='Шаг для изменения номинала сертификата',
        max_digits=10,
        decimal_places=2,
        default=1000
    )
    validity = models.PositiveSmallIntegerField(
        'Срок действия',
        help_text='Срок действия сертификата в днях. По умолчанию 0 - неограничен',
        default=0
    )
    send_email = models.BooleanField(
        'Отправлять на email',
        help_text='Отправлять информацию по заказанным сертификатам на email. Обязательно укажите его в настройках',
        default=True
    )
    email = models.EmailField(
        'Email адрес',
        help_text='Email адрес для отправки информации по заказанным сертификатам',
        blank=True
    )
    send_b24 = models.BooleanField(
        'Отправлять в Битрикс24',
        help_text='Создавать в Битрикс24 сделки по заказанным сертификатам',
        default=False
    )
    id_catalog_b24 = models.PositiveIntegerField(
        verbose_name='ID товара',
        help_text='ID товара в каталоге Битрикс24',
        null=True,
        blank=True
    )
    background_image_card = ResizedImageField(
        verbose_name='Файл фонового изображения карточки',
        help_text='Изображение отображается в фоне карточки Подарочного сертификата',
        blank=True,
        upload_to='img/giftcert/',
        size=[600, 400]
    )
    background_image_form = ResizedImageField(
        verbose_name='Файл фонового изображения формы',
        help_text='Изображение отображается в фоне формы Подарочного сертификата',
        blank=True,
        upload_to='img/giftcert/',
        size=[800, 800]
    )
    text_color = models.CharField(
        'Цвет текста в карточке',
        max_length=10,
        choices=ColorText.choices,
        default=ColorText.DARK
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подарочный сертификат'
        verbose_name_plural = 'Подарочные сертификаты'


class OrderGiftCertificate(CreatedModel):
    """Класс для Заказа подарочного сертификата."""
    gift_certificate = models.ForeignKey(
        GiftCertificate,
        verbose_name='Подарочный сертификат',
        help_text='Из какого подарочного сертификата был создан заказ. Служебное поле для определения начальных '
                  'параметров',
        on_delete=models.PROTECT,
        related_name='orders',
    )
    buy_date_time = models.DateTimeField(
        'Дата и время оплаты',
        help_text='Дата и время оплаты сертификата',
        blank=True,
        null=True,
    )
    validity_date_time = models.DateField(
        'Действителен до',
        help_text='Дата и время, до которых сертификат действителен. Если не заполнено, то срок неограничен',
        null=True,
        blank=True
    )
    type = models.ForeignKey(
        GiftCertificateType,
        verbose_name='Тип сертификата',
        help_text='Тип выбранного сертификата',
        on_delete=models.PROTECT,
        related_name='orders'
    )
    price = models.DecimalField(
        'Стоимость',
        help_text='Стоимость сертификата',
        max_digits=10,
        decimal_places=2
    )
    paid = models.BooleanField(
        'Оплачено',
        help_text='Сумма сертификата оплачена клиентом',
        default=False,
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
    )
    user_name = models.CharField(
        'Имя клиента',
        help_text='Имя клиента',
        max_length=255,
        blank=True
    )
    user_lastname = models.CharField(
        'Фамилия клиента',
        help_text='Фамилия клиента',
        max_length=255,
        blank=True
    )
    user_email = models.EmailField(
        'Email клиента',
        help_text='Электронная почта клиента',
        blank=True
    )
    user_address = models.CharField(
        'Адрес клиента',
        help_text='Адрес доставки сертификата клиенту',
        max_length=255,
        blank=True
    )
    user_phone = models.CharField(
        'Телефон клиента',
        help_text='Телефон клиента',
        max_length=20,
        blank=True
    )
    sent_email = models.BooleanField(
        'Отправлено на email',
        help_text='Сертификат и детали заказа отправлены на email клиента',
        default=False
    )
    sent_bitrix = models.BooleanField(
        verbose_name='Отправлено в Битрикс24',
        help_text='Отправлено в Битрикс24, создана сделка',
        default=False,
    )
    deal_id_b24 = models.PositiveIntegerField(
        verbose_name='ID сделки в Битрикс24',
        help_text='ID сделки в Битрикс24',
        unique=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Сертификат №{self.pk} до {str(self.validity_date_time) if self.validity_date_time else "Неограничен"}'

    class Meta:
        verbose_name = 'Заказ на подарочный сертификат'
        verbose_name_plural = 'Заказы на подарочные сертификаты'


class PriceForSpaServices(CreatedModel):
    """Класс с ценами для программ парения."""
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    max_guest = models.PositiveSmallIntegerField(
        verbose_name='Максимальное количество человек',
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name='Продолжительность, мин.',
        help_text='Продолжительность программы парения в минутах',
    )

    def __str__(self):
        return f'{self.price} руб. до {self.max_guest} чел. за {self.duration} мин.'

    class Meta:
        verbose_name = 'Цена для программ парения'
        verbose_name_plural = 'Цены для программ парения'


class ReserveServices(CreatedModel):
    """Класс дополнительных услуг для бронирования"""
    reserve = models.ForeignKey(Reserve, on_delete=models.CASCADE, verbose_name='Бронирование')
    additional_service = models.ForeignKey(AdditionalServices, on_delete=models.PROTECT,
                                           verbose_name='Дополнительная услуга')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость', blank=True)
    id_b24 = models.PositiveSmallIntegerField(verbose_name='ID товарной позиции в Б24', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.cost = self.additional_service.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.reserve} - {self.additional_service} - {self.quantity}'

    class Meta:
        verbose_name = 'Дополнительная услуга для бронирования'
        verbose_name_plural = 'Дополнительные услуги для бронирования'


class WeekendDays(CreatedModel):
    """Класс праздничные дни."""
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование',
        null=True,
        blank=True
    )
    date = models.DateField(
        verbose_name='Дата праздника',
    )

    def __str__(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Праздничный день'
        verbose_name_plural = 'Праздничные дни'


class SocialNetworks(CreatedModel):
    """Класс социальные сети."""
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование',
    )
    link = models.URLField(
        verbose_name='Ссылка'
    )
    icon = models.ImageField(
        verbose_name='Иконка',
        upload_to='img/social/'
    )
    show_header = models.BooleanField(
        verbose_name='Показывать в шапке',
        default=False
    )
    show_footer = models.BooleanField(
        verbose_name='Показывать в подвале',
        default=False
    )
    show_block_booking = models.BooleanField(
        verbose_name='Показывать в блоке бронирования',
        default=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'


class SettingsBitrix24(CreatedModel):
    """Класс для настроек интеграции с Битрикс24."""
    active = models.BooleanField(
        verbose_name='Активность',
        default=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование',
    )
    webhook = models.URLField(
        verbose_name='Webhook',
        help_text='Webhook для интеграции с Битрикс24',
        null=True,
        blank=True
    )
    responsible_by_default = models.PositiveIntegerField(
        verbose_name='Ответственный по умолчанию',
        help_text='ID ответственного, который будет подставляться при создании сущностей CRM',
        default=1,
    )
    stage_id_for_deal_adding = models.CharField(
        verbose_name='ID стадии для создания сделки',
        help_text='ID стадии воронки сделок для создания сделки бронирования с сайта в CRM',
        max_length=10,
        default=6,
    )
    stage_id_for_gift_cert = models.CharField(
        verbose_name='ID стадии для создания сделки по подарочному сертификату',
        help_text='ID стадии воронки сделок для создания сделки по подарочному сертификату с сайта в CRM',
        max_length=10,
        default=6,
    )
    reserve_field_code_b24 = models.CharField(
        verbose_name='Код поля Бронирование',
        help_text='Код поля Бронирование в Битрикс24 (тип поля Бронирование ресурсов)',
        max_length=20,
        default='UF_CRM_0000000000'
    )
    is_reserve_site_field_code_b24 = models.CharField(
        verbose_name='Код поля Бронирование с сайта',
        help_text='Код поля Бронирование с сайта в Битрикс24 (тип поля Да/Нет)',
        max_length=20,
        default='UF_CRM_0000000000'
    )

    def get_rest_key(self):
        return urlparse(self.webhook).path.split('/')[-2]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.active:
            SettingsBitrix24.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Настройки для Битрикс24'
        verbose_name_plural = 'Настройки для Битрикс24'


class SettingsSite(CreatedModel):
    """Класс для настроек сайта."""
    active = models.BooleanField(
        verbose_name='Активность',
        default=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование',
    )
    reserve_start_time = models.PositiveSmallIntegerField(
        verbose_name='Старт бронирования',
        help_text='Укажите час, с которого начинается бронирование',
        default=0,
        validators=[MinValueValidator(0, 'Часы не могут быть меньше 0'),
                    MaxValueValidator(24, 'Часы не могут быть больше 24')],
    )
    reserve_end_time = models.PositiveSmallIntegerField(
        verbose_name='Окончание бронирования',
        help_text='Укажите час, после которого кончается бронирование',
        default=24,
        validators=[MinValueValidator(0, 'Часы не могут быть меньше 0'),
                    MaxValueValidator(24, 'Часы не могут быть больше 24')],
    )
    reserve_closed = models.BooleanField(
        verbose_name='Бронирование закрыто',
        help_text='Закрыть возможность бронирования на сайте для посетителей, есть возможность только у персонала',
        default=False,
    )
    reserve_closed_all = models.BooleanField(
        verbose_name='Бронирование закрыто для всех',
        help_text='Закрыть возможность бронирования на сайте для всех, есть возможность только у суперпользователя',
        default=False,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.active:
            SettingsSite.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'
