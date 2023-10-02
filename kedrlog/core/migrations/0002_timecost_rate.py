# Generated by Django 4.2.4 on 2023-09-07 12:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('start_time', models.TimeField(help_text='Граница включена в тариф', verbose_name='Начальное время')),
                ('end_time', models.TimeField(help_text='Граница НЕ включена в тариф', verbose_name='Конечное время')),
                ('interval', models.PositiveSmallIntegerField(default=60, validators=[django.core.validators.MinValueValidator(0, 'Значение не должно быть меньше 0'), django.core.validators.MaxValueValidator(180, 'Значение не должно быть больше 180')], verbose_name='Интервал тарификации, мин')),
                ('cost', models.DecimalField(decimal_places=2, help_text='Стоимость за один интервал тарификации', max_digits=10, verbose_name='Стоимость, руб.')),
            ],
            options={
                'verbose_name': 'Интервал тарификации',
                'verbose_name_plural': 'Интервалы тарификации',
                'unique_together': {('start_time', 'end_time', 'cost', 'interval')},
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('active', models.BooleanField(default=False, help_text='Выбор активного тарифа для Парной', verbose_name='Активность')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Описание')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rate_house', to='core.house', verbose_name='Парная')),
                ('rate', models.ManyToManyField(related_name='rate_time_cost', to='core.timecost')),
            ],
            options={
                'verbose_name': 'Тариф',
                'verbose_name_plural': 'Тарифы',
            },
        ),
    ]