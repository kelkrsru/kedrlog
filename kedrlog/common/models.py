from django.db import models

from ckeditor.fields import RichTextField


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
