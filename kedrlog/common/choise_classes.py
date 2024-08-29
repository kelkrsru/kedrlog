from django.db import models


class DayWeek(models.IntegerChoices):
    MONDAY = 1, 'Понедельник'
    TUESDAY = 2, 'Вторник'
    WEDNESDAY = 3, 'Среда'
    THURSDAY = 4, 'Четверг'
    FRIDAY = 5, 'Пятница'
    SATURDAY = 6, 'Суббота'
    SUNDAY = 7, 'Воскресенье'

    __empty__ = 'Не выбрано'
