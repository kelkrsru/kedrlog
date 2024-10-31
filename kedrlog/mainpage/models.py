from common.models import CreatedModel
from core.models import House
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models


class ContentBlock(CreatedModel):
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование блока',
    )
    active = models.BooleanField(
        verbose_name='Активность',
        help_text='Выберите блок в качестве активного. Текущий активный блок потеряет этот статус',
        default=False
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class ContentBlockMain(ContentBlock):
    """Класс для главного баннера."""
    header = models.CharField(
        max_length=255,
        verbose_name='Заголовок главного баннера',
        help_text='Введите заголовок главного баннера'
    )
    second_header = models.CharField(
        max_length=255,
        verbose_name='Подзаголовок главного баннера',
        help_text='Введите подзаголовок главного баннера'
    )
    video_mp4 = models.FileField(
        verbose_name='Видео файл mp4',
        help_text='Выберите видео файл в формате mp4',
        validators=[FileExtensionValidator(['mp4'])],
        upload_to='video/contentblockmain/'
    )

    def save(self, *args, **kwargs):
        if self.active:
            ContentBlockMain.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Главный баннер'
        verbose_name_plural = 'Главные баннеры'


class ToastMain(ContentBlock):
    """Класс для главного баннера."""
    header = models.CharField('Заголовок', help_text='Введите заголовок всплывающего окна', max_length=50, null=True,
                              blank=True)
    second_header = models.CharField('Подзаголовок', help_text='Введите подзаголовок всплывающего окна', max_length=50,
                                     null=True, blank=True)
    image = models.ImageField('Картинка', help_text='Загрузите картинку-баннер', upload_to='img/toasts/')

    def save(self, *args, **kwargs):
        if self.active:
            ToastMain.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Всплывающее окно'
        verbose_name_plural = 'Всплывающие окна'


class ContentBlockRoundedMenuItem(models.Model):
    """Класс для элементов блока с круглыми иконками."""
    name = models.CharField(
        max_length=50,
        verbose_name='Наименование элемента'
    )
    image = models.ImageField(
        verbose_name='Иконка элемента',
        upload_to='img/roundedmenu',
    )
    image_alt = models.CharField(
        verbose_name='Alt описание',
        max_length=50,
    )
    link = models.CharField(
        verbose_name='Ссылка на страницу',
        max_length=255,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Элемент'
        verbose_name_plural = 'Элементы'


class ContentBlockHeader(models.Model):
    """Класс для заголовка блока."""
    header = models.CharField(
        max_length=255,
        verbose_name='Заголовок блока',
        help_text='Введите заголовок блока',
        blank=True
    )
    second_header = models.CharField(
        max_length=255,
        verbose_name='Подзаголовок блока',
        help_text='Введите подзаголовок блока',
        blank=True
    )

    class Meta:
        abstract = True


class ContentBlockRoundedMenu(ContentBlock, ContentBlockHeader):
    """Класс для меню с круглыми иконками."""
    items = models.ManyToManyField(
        ContentBlockRoundedMenuItem,
        verbose_name='Элементы',
    )

    class Meta:
        abstract = True


class ContentBlockInfrastructure(ContentBlockRoundedMenu):
    """Класс для блока Инфраструктура."""

    def save(self, *args, **kwargs):
        if self.active:
            ContentBlockInfrastructure.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блок Инфраструктура'
        verbose_name_plural = 'Блоки Инфраструктура'


class ContentBlockService(ContentBlockRoundedMenu):
    """Класс для блока Дополнительные услуги."""

    def save(self, *args, **kwargs):
        if self.active:
            ContentBlockService.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блок Дополнительные услуги'
        verbose_name_plural = 'Блоки Дополнительные услуги'


class ContentBlockYandexMap(ContentBlock, ContentBlockHeader):
    """Класс блока для Яндекс карты."""
    link = models.URLField(
        verbose_name='Ссылка на Яндекс карту',
        help_text='Только ссылка, без тегов'
    )

    def save(self, *args, **kwargs):
        if self.active:
            ContentBlockYandexMap.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блок Яндекс карта'
        verbose_name_plural = 'Блоки Яндекс карта'


class HouseShowBooking(CreatedModel):
    """Таблица соединения между Домами и их отображением на блоке Бронирования."""
    house = models.ForeignKey(
        House,
        verbose_name='Парная',
        on_delete=models.CASCADE
    )
    block_booking = models.ForeignKey(
        'ContentBlockBooking',
        verbose_name='Блок Бронирования',
        on_delete=models.CASCADE
    )
    position_top = models.PositiveSmallIntegerField(
        verbose_name='Отступ сверху',
        validators=[MinValueValidator(0, 'Значение не должно быть меньше 0'),
                    MaxValueValidator(100, 'Значение не должно быть больше 100')]
    )
    position_left = models.PositiveSmallIntegerField(
        verbose_name='Отступ слева',
        validators=[MinValueValidator(0, 'Значение не должно быть меньше 0'),
                    MaxValueValidator(100, 'Значение не должно быть больше 100')]
    )

    def __str__(self):
        return self.house.name

    class Meta:
        verbose_name = 'Расположение Парных на блоке Бронирования'
        ordering = ['-house__active', 'house__name']


class ContentBlockBooking(ContentBlock, ContentBlockHeader):
    """Класс блока для Бронирования."""
    background_image = models.ImageField(
        verbose_name='Фоновое изображение',
        upload_to='img/booking'
    )
    houses = models.ManyToManyField(
        House,
        through=HouseShowBooking,
        through_fields=['block_booking', 'house']
    )

    def save(self, *args, **kwargs):
        if self.active:
            ContentBlockBooking.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Блок Бронирование'
        verbose_name_plural = 'Блоки Бронирование'
