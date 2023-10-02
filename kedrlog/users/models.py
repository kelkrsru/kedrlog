from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Класс переопределенного пользователя."""
    birth_date = models.DateField(
        verbose_name='Дата рождения',
        null=True,
        blank=True
    )
