from ckeditor.fields import RichTextField
from common.models import Content, Gallery, TextContent
from core.models import GiftCertificate, SpaServices
from django.db import models
from django_resized import ResizedImageField


class GalleryHouses(Gallery):
    """Класс галереи для страницы Дома."""
    def save(self, *args, **kwargs):
        if self.active:
            GalleryHouses.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Галерея страницы Дома'
        verbose_name_plural = 'Галереи страницы Дома'


class GalleryTerritory(Gallery):
    """Класс галереи для страницы Территория."""
    def save(self, *args, **kwargs):
        if self.active:
            GalleryTerritory.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Галерея страницы Территория'
        verbose_name_plural = 'Галереи страницы Территория'


class GalleryFood(Gallery):
    """Класс галереи для страницы Территория."""
    def save(self, *args, **kwargs):
        if self.active:
            GalleryFood.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Галерея страницы Трапезная'
        verbose_name_plural = 'Галереи страницы Трапезная'


class TextContentRules(TextContent):
    """Класс текстового контента для страницы Правила посещения бани."""
    def save(self, *args, **kwargs):
        if self.active:
            TextContentRules.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Контент для страницы Правила посещения'
        verbose_name_plural = 'Контент для страницы Правила посещения'


class TextContentRulesGiftCert(TextContent):
    """Класс текстового контента для страницы Правила использования подарочного сертификата."""
    def save(self, *args, **kwargs):
        if self.active:
            TextContentRulesGiftCert.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Контент для страницы Правила использования подарочного сертификата'
        verbose_name_plural = 'Контент для страницы Правила использования подарочного сертификата'


class TextContentFz152(TextContent):
    """Класс текстового контента для страницы ФЗ152."""
    def save(self, *args, **kwargs):
        if self.active:
            TextContentFz152.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Контент для страницы Обработка ПД ФЗ-152'
        verbose_name_plural = 'Контент для страницы Обработка ПД ФЗ-152'


class TextContentAccessories(TextContent):
    """Класс текстового контента для страницы Аксессуары."""
    def save(self, *args, **kwargs):
        if self.active:
            TextContentAccessories.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Контент для страницы Аксессуары'
        verbose_name_plural = 'Контент для страницы Аксессуары'


class TextContentRent(TextContent):
    """Класс текстового контента для страницы Аренда комплекса."""
    def save(self, *args, **kwargs):
        if self.active:
            TextContentRent.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Контент для страницы Аренда комплекса'
        verbose_name_plural = 'Контент для страницы Аренда комплекса'


class TextContentCorporate(TextContent):
    """Класс текстового контента для страницы Корпоративным клиентам."""
    def save(self, *args, **kwargs):
        if self.active:
            TextContentCorporate.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Контент для страницы Корпоративным клиентам'
        verbose_name_plural = 'Контент для страницы Корпоративным клиентам'


class ContentPrice(Content):
    """Класс контента для страницы Цены."""
    header_image = models.ImageField(
        verbose_name='Файл основного изображения',
        blank=True,
        upload_to='img/price/'
    )
    header_house = models.CharField(
        verbose_name='Заголовок для основных услуг',
        max_length=1024,
    )
    is_show_card_image = models.BooleanField(
        'Показывать фото в карточке',
        help_text='Показывать фото в карточке тарифа парной',
        default=False,
    )
    description_house = RichTextField(
        verbose_name='Описание для основных услуг',
        blank=True,
        null=True
    )
    description_spa_services = RichTextField(
        verbose_name='Описание для программ парения',
        blank=True,
        null=True
    )
    header_service = models.CharField(
        verbose_name='Заголовок для дополнительных услуг',
        max_length=1024,
    )
    description_service = RichTextField(
        verbose_name='Описание для дополнительных услуг',
        max_length=1024,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if self.active:
            ContentPrice.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Контент для страницы Цены'
        verbose_name_plural = 'Контент для страницы Цены'


class ContentSpa(Content):
    """Класс контента для страницы Спа-программы."""
    spa_service = models.ManyToManyField(
        SpaServices,
        verbose_name='Программы парения',
        help_text='Выберите отображаемые программы парения',
        related_name='spa_service_content_spa',
        blank=True,
    )

    def save(self, *args, **kwargs):
        if self.active:
            ContentSpa.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Контент для страницы Спа-программы'
        verbose_name_plural = 'Контент для страницы Спа-программы'


class ContentGiftCertificate(Content):
    """Класс контента для страницы Подарочные сертификаты."""
    gift_certificates = models.ManyToManyField(
        GiftCertificate,
        verbose_name='Подарочные сертификаты',
        help_text='Выберите подарочные сертификаты для отображения на странице Подарочные сертификаты',
        related_name='contents'
    )
    content_image = ResizedImageField(
        verbose_name='Файл изображения',
        help_text='Изображение сразу после сертификатов',
        blank=True,
        upload_to='img/giftcert/',
        size=[800, 800]
    )
    content_text = RichTextField(
        verbose_name='Текст страницы',
        help_text='Текст после изображения',
        blank=True
    )

    def save(self, *args, **kwargs):
        if self.active:
            ContentGiftCertificate.objects.filter(active=True).update(active=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Контент для страницы Подарочные сертификаты'
        verbose_name_plural = 'Контент для страницы Подарочные сертификаты'
