from common.models import Gallery, TextContent


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
