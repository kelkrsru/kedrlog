# Generated by Django 4.2.4 on 2023-09-11 03:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_alter_rate_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('start_date', models.DateField(verbose_name='Дата начала бронирования')),
                ('start_time', models.TimeField(verbose_name='Время начала бронирования')),
                ('end_date', models.DateField(verbose_name='Дата окончания бронирования')),
                ('end_time', models.TimeField(verbose_name='Время окончания бронирования')),
                ('count_guests', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Количество людей не может быть меньше 0 или 0')], verbose_name='Количество человек')),
                ('send_to_bitrix', models.BooleanField(default=False, verbose_name='Отправлено в Битрикс24')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.house', verbose_name='Парная')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
                'unique_together': {('start_date', 'start_time', 'end_date', 'end_time', 'house')},
            },
        ),
    ]
