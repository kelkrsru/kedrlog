from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from common.models import CreatedModel, GalleryItem

User = get_user_model()


class Company(CreatedModel):
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
        upload_to='media/img/logo/'
    )
    logo_footer = models.ImageField(
        verbose_name='Файл логотипа компании в подвале',
        help_text='Файл логотипа компании в подвале в формате png, рекомендованный размер 60x60 px с прозрачным фоном',
        blank=True,
        upload_to='media/img/logo/'
    )
    favicon = models.ImageField(
        verbose_name='Файл favicon',
        help_text='Файл favicon в формате ico',
        blank=True,
        upload_to='media/img/favicon/'
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
        verbose_name='Время на уборку в минутах',
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Парная'
        verbose_name_plural = 'Парные'


class TimeCost(CreatedModel):
    """Класс интервал - цена."""
    start_time = models.TimeField(
        verbose_name='Начальное время',
        help_text='Граница включена в тариф'
    )
    end_time = models.TimeField(
        verbose_name='Конечное время',
        help_text='Граница НЕ включена в тариф'
    )
    interval = models.PositiveSmallIntegerField(
        verbose_name='Интервал тарификации, мин',
        validators=[MinValueValidator(0, 'Значение не должно быть меньше 0'),
                    MaxValueValidator(180, 'Значение не должно быть больше 180')],
        default=60
    )
    cost = models.DecimalField(
        verbose_name='Стоимость, руб.',
        help_text='Стоимость за один интервал тарификации',
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f'{str(self.start_time)} - {str(self.end_time)} - {str(self.cost)} руб. - {str(self.interval)} мин.'

    class Meta:
        verbose_name = 'Интервал тарификации'
        verbose_name_plural = 'Интервалы тарификации'
        unique_together = ['start_time', 'end_time', 'cost', 'interval']


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
    rate = models.ManyToManyField(
        TimeCost,
        verbose_name='Интервалы тарификации',
        related_name='rate_time_cost',
    )

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
    start_date = models.DateField(
        verbose_name='Дата начала бронирования',
    )
    start_time = models.TimeField(
        verbose_name='Время начала бронирования',
    )
    end_date = models.DateField(
        verbose_name='Дата окончания бронирования',
    )
    end_time = models.TimeField(
        verbose_name='Время окончания бронирования',
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
        validators=[MinValueValidator(1, 'Количество людей не может быть меньше 0 или 0'), ],
    )
    cost = models.DecimalField(
        verbose_name='Сумма',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    paid = models.BooleanField(
        verbose_name='Оплачено',
        default=False,
    )
    send_to_bitrix = models.BooleanField(
        verbose_name='Отправлено в Битрикс24',
        default=False,
    )

    def __str__(self):
        return f'Бронирование {self.house.name} с {self.start_date} {self.start_time} по {self.end_date} ' \
               f'{self.end_time}'

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        unique_together = ['start_date', 'start_time', 'end_date', 'end_time', 'house']
