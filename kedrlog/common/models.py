from ckeditor.fields import RichTextField
from django.db import models


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания и дату обновления"""

    created = models.DateField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )
    updated = models.DateField(
        verbose_name='Дата изменения',
        auto_now=True,
    )

    class Meta:
        abstract = True


class Seo(models.Model):
    """Абстрактная модель, добавляет поля для seo."""

    seo_title = models.CharField(
        max_length=60,
        verbose_name='Заголовок страницы',
        blank=True
    )
    seo_description = models.CharField(
        max_length=160,
        verbose_name='Описание страницы',
        blank=True
    )
    seo_keywords = models.CharField(
        max_length=100,
        verbose_name='Ключевые слова',
        blank=True
    )

    class Meta:
        abstract = True


class GalleryItem(CreatedModel):
    """Класс для элементов галереи."""

    name = models.CharField(
        max_length=255,
        verbose_name='Наименование элемента',
    )
    alt = models.CharField(
        max_length=255,
        verbose_name='Alt описание картинки',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок элемента',
        blank=True
    )
    description = models.CharField(
        max_length=255,
        verbose_name='Описание элемента',
        blank=True
    )
    image_large = models.ImageField(
        verbose_name='Картинка в исходном разрешении',
        upload_to='gallery/'
    )
    image_small = models.ImageField(
        verbose_name='Картинка для превью',
        upload_to='gallery/'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Элемент галереи'
        verbose_name_plural = 'Элементы галереи'


class Content(CreatedModel, Seo):
    """Класс для страницы с контентом."""
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование'
    )
    header = models.CharField(
        max_length=255,
        verbose_name='Заголовок',
        help_text='Введите заголовок'
    )
    second_header = models.CharField(
        max_length=255,
        verbose_name='Подзаголовок',
        help_text='Введите подзаголовок'
    )
    active = models.BooleanField(
        verbose_name='Активность',
        help_text='Выберите в качестве активного. Текущий активный элемент потеряет этот статус',
        default=False
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Gallery(Content):
    """Класс для страницы галереи."""
    items = models.ManyToManyField(
        GalleryItem,
        verbose_name='Элементы',
        help_text='Выберите необходимые элементы галереи'
    )

    class Meta:
        abstract = True


class TextContent(Content):
    """Класс для страницы с текстовым контентом."""
    text = RichTextField(
        verbose_name='Текст',
        help_text='Текст для страницы'
    )

    class Meta:
        abstract = True


class Badge(CreatedModel):
    """Класс для плашек на карточки товара или другие элементы."""
    class ColorBackground(models.TextChoices):
        PRIMARY = 'bg-primary', 'Синий'
        SECONDARY = 'bg-secondary', 'Серый'
        SUCCESS = 'bg-success', 'Зеленый'
        DANGER = 'bg-danger', 'Красный'
        DARK = 'bg-dark', 'Черный'
        BRAND_GREEN = 'bg-green', 'Фирменный зеленый'
        BRAND_BROWN = 'bg-brown', 'Фирменный коричневый'

    name = models.CharField(
        'Наименование',
        max_length=255
    )
    text = models.CharField(
        'Текст на плашке',
        max_length=30,
    )
    background = models.CharField(
        'Цвет фона плашки',
        max_length=30,
        choices=ColorBackground.choices,
        default=ColorBackground.SUCCESS
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Плашка'
        verbose_name_plural = 'Плашки'


# class YandexMetrica(CreatedModel):
#     """Класс для счетчика Яндекс метрики."""
#     active = models.BooleanField('Активность', default=True)
#     number = models.CharField('Номер счетчика', help_text='Номер счетчика из аккаунта', max_length=15)
#     account = models.EmailField('Аккаунт', help_text='Email, к которому привязан счетчик')
#     code = models.TextField('Код счетчика', help_text='Код счетчика, для вставки на страницы сайта')
#
#     def __str__(self):
#         return f'Счетчик №{self.number} - аккаунт {self.account}'
#
#     class Meta:
#         verbose_name = 'Счетчик Яндекс Метрики'
#         verbose_name_plural = 'Счетчики Яндекс Метрики'

#
# class Portals(models.Model):
#     """Модель портала Битрикс24"""
#     member_id = models.CharField(
#         verbose_name='Уникальный код портала',
#         max_length=255,
#         unique=True,
#     )
#     name = models.CharField(
#         verbose_name='Имя портала',
#         max_length=255,
#     )
#     auth_id = models.CharField(
#         verbose_name='Токен аутентификации',
#         max_length=255,
#     )
#     auth_id_create_date = models.DateTimeField(
#         verbose_name='Дата получения токена аутентификации',
#         auto_now=True,
#     )
#     refresh_id = models.CharField(
#         verbose_name='Токен обновления',
#         max_length=255,
#     )
#     client_id = models.CharField(
#         verbose_name='Уникальный ID клиента',
#         max_length=50,
#         null=True,
#         blank=True,
#     )
#     client_secret = models.CharField(
#         verbose_name='Секретный токен клиента',
#         max_length=100,
#         null=True,
#         blank=True,
#     )
#
#     class Meta:
#         verbose_name = 'Портал'
#         verbose_name_plural = 'Порталы'
#
#     def __str__(self):
#         return self.name
