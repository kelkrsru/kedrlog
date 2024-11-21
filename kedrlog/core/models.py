from urllib.parse import urlparse

from ckeditor.fields import RichTextField
from common.models import Badge, CreatedModel, GalleryItem, Seo
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
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
    comfort = models.PositiveSmallIntegerField(
        verbose_name='Комфортное размещение',
        default=10
    )
    cleaning = models.PositiveSmallIntegerField(
        verbose_name='Время на уборку в минутах',
        help_text='Если 0, то уборка отсутствует',
        default=30
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


class Weeks(CreatedModel):
    """Класс дней недели."""
    MSG_MIN_MAX = 'Убедитесь что данное значение от 1 до 7'
    MSG_UNIQUE = 'Убедитесь, что данное значение является уникальным'

    name = models.CharField(
        'Наименование',
        help_text='Наименование дня недели',
        max_length=255
    )
    number = models.PositiveSmallIntegerField(
        'Порядковый номер',
        help_text='Порядковый номер дня недели',
        validators=[MinValueValidator(1, MSG_MIN_MAX), MaxValueValidator(7, MSG_MIN_MAX)],
        unique=True,
        error_messages={'unique': MSG_UNIQUE}
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'


class Price(CreatedModel):
    """Класс цен для тарифа."""

    price = models.DecimalField(
        'Цена',
        help_text='Цена за интервал бронирования, который задается в настройках сайта',
        max_digits=10,
        decimal_places=2,
    )
    day_period_validity = models.ManyToManyField(
        Weeks,
        verbose_name='Период действия, день',
        help_text='Дни, в которые будет действовать данная цена',
    )
    is_active_in_weekend_day = models.BooleanField(
        'Действует в праздничный день',
        help_text='Праздничные дни берутся из справочника Праздничные дни.',
        default=False
    )

    def __str__(self):
        return (f'Цена {self.price} в {", ".join(self.day_period_validity.all().values_list("name", flat=True))}'
                f'{" и Праздничный день" if self.is_active_in_weekend_day else ""}')

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'


class Rate(CreatedModel):
    """Класс Тариф."""
    name = models.CharField(
        verbose_name='Наименование',
        max_length=255
    )
    comment = models.CharField(
        'Комментарий',
        help_text='Рабочий комментарий, например этажность парной',
        blank=True,
        max_length=1024
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    house = models.ManyToManyField(
        House,
        verbose_name='Парная',
        related_name='house_rates',
    )
    price = models.ManyToManyField(
        Price,
        verbose_name='Цена',
        help_text='Цены тарифа',
        related_name='price_rates'
    )
    min_time = models.PositiveSmallIntegerField(
        verbose_name='Минимальное время парения',
        help_text='Минимальное время парения в минутах',
        default=180
    )
    max_guest = models.PositiveSmallIntegerField(
        'Максимальное количество гостей',
        default=12
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
    id_additional_guest_in_catalog_b24 = models.PositiveIntegerField(
        verbose_name='ID товара дополнительного гостя в каталоге Битрикс24',
        blank=True,
        null=True
    )

    def get_min_price(self):
        """Получить минимальную цену в тарифе."""
        return min(self.price.all().values_list('price', flat=True))

    @staticmethod
    def is_day_of_weekend(date):
        """Проверить день на праздничный."""
        if WeekendDays.objects.filter(date=date):
            return True
        return False

    def get_price(self, date):
        """Получить цену, исходя из буднего/праздничного/выходного дня."""
        print(f'{date.weekday()=}')
        if self.is_day_of_weekend(date):
            return Price.objects.get(price_rates=self, is_active_in_weekend_day=True).price
        return Price.objects.get(price_rates=self, day_period_validity__exact=date.weekday() + 1).price

    def __str__(self):
        return f'{self.name}{" " + self.comment if self.comment else ""}'

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
    rate = models.ForeignKey(Rate, verbose_name='Тариф', on_delete=models.PROTECT, related_name='rate_reserves')
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
    badge = models.ForeignKey(
        Badge,
        verbose_name='Плашка',
        help_text='Плашка на карточке товара',
        related_name='spa_services',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
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
    used = models.BooleanField(
        'Использован',
        help_text='Сертификат уже использован клиентом',
        default=False
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
    reserve_interval = models.PositiveSmallIntegerField(
        'Интервал бронирования', help_text='Интервал бронирования в минутах', default=60
    )
    reserve_show_interval = models.PositiveSmallIntegerField(
        'Интервал показа бронирования', help_text='Интервал показа бронирования в минутах', default=30
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
    gift_certificate_closed = models.BooleanField(
        'Сертификаты закрыты',
        help_text='Закрыть возможность оформления подарочного сертификата на сайте для посетителей, есть возможность '
                  'только у персонала',
        default=False,
    )
    gift_certificate_closed_all = models.BooleanField(
        'Сертификаты закрыты для всех',
        help_text='Закрыть возможность оформления подарочного сертификата на сайте для всех, есть возможность только у '
                  'суперпользователя',
        default=False,
    )
    text_gift_certificate_closed = RichTextField(
        'Текст страницы заглушки',
        help_text='Текст, который отображается на странице заглушке при закрытой возможности оформления подарочных '
                  'сертификатов',
        default='Возможность оформления подарочного сертификата закрыта.'
    )
    text_gift_certificate_ok = RichTextField(
        'Текст страницы успеха',
        help_text='Текст, который отображается на странице после успешного оформления подарочного сертификата, под '
                  'параметрами сертификата.',
        default='Спасибо, что вы с нами.',
        blank=True
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
