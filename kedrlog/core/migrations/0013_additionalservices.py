# Generated by Django 4.2.4 on 2023-11-16 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_rate_min_time_alter_house_cleaning'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('active', models.BooleanField(default=True, verbose_name='Активность')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Цена')),
                ('measure', models.CharField(choices=[(None, 'Не выбрано'), ('piece', 'шт.'), ('service', 'усл.'), ('hour', 'час')], default='Не выбрано', max_length=20, verbose_name='Единицы измерения')),
                ('id_catalog_b24', models.PositiveIntegerField(blank=True, help_text='ID товара/услуги в каталоге Битрикс24', null=True, verbose_name='ID товара/услуги')),
            ],
            options={
                'verbose_name': 'Дополнительная услуга',
                'verbose_name_plural': 'Дополнительные услуги',
            },
        ),
    ]
