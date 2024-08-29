# Generated by Django 4.2.4 on 2024-08-22 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0061_alter_weeks_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='id_rent_weekend_in_catalog_b24',
        ),
        migrations.RemoveField(
            model_name='rate',
            name='price_weekend',
        ),
        migrations.AddField(
            model_name='price',
            name='is_active_in_weekend_day',
            field=models.BooleanField(default=False, help_text='Праздничные дни берутся из справочника Праздничные дни.', verbose_name='Действует в праздничный день'),
        ),
        migrations.AddField(
            model_name='rate',
            name='max_guest',
            field=models.PositiveSmallIntegerField(default=12, verbose_name='Максимальное количество гостей'),
        ),
        migrations.AlterField(
            model_name='rate',
            name='house',
            field=models.ManyToManyField(related_name='house_rates', to='core.house', verbose_name='Парная'),
        ),
        migrations.RemoveField(
            model_name='rate',
            name='price',
        ),
        migrations.AddField(
            model_name='rate',
            name='price',
            field=models.ManyToManyField(help_text='Цены тарифа', related_name='price_rates', to='core.price', verbose_name='Цена'),
        ),
    ]
