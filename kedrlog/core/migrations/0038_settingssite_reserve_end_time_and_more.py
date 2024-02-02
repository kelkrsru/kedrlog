# Generated by Django 4.2.4 on 2024-01-25 15:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_settingssite'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingssite',
            name='reserve_end_time',
            field=models.PositiveSmallIntegerField(default=24, help_text='Укажите час, после которого кончается бронирование', validators=[django.core.validators.MinValueValidator(0, 'Часы не могут быть меньше 0'), django.core.validators.MaxValueValidator(24, 'Часы не могут быть больше 24')], verbose_name='Окончание бронирования'),
        ),
        migrations.AddField(
            model_name='settingssite',
            name='reserve_start_time',
            field=models.PositiveSmallIntegerField(default=0, help_text='Укажите час, с которого начинается бронирование', validators=[django.core.validators.MinValueValidator(0, 'Часы не могут быть меньше 0'), django.core.validators.MaxValueValidator(24, 'Часы не могут быть больше 24')], verbose_name='Старт бронирования'),
        ),
    ]
