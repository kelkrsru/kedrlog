# Generated by Django 4.2.4 on 2023-10-30 15:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_house_additional_features_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reserve',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='rate',
            name='rate',
        ),
        migrations.AddField(
            model_name='rate',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Цена за 1 час в обычный день пн, вт, ср, чт', max_digits=10, verbose_name='Цена'),
        ),
        migrations.AddField(
            model_name='rate',
            name='price_weekend',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Цена за 1 час в выходной день пт, сб, вс и праздники', max_digits=10, verbose_name='Цена выходного дня'),
        ),
        migrations.AddField(
            model_name='reserve',
            name='duration',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Продолжительность бронирования'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reserve',
            name='end_date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 30, 22, 51, 48, 29712), verbose_name='Дата и время окончания бронирования'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reserve',
            name='start_date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 30, 22, 52, 4, 834285), verbose_name='Дата и время начала бронирования'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='house',
            name='additional_features',
            field=models.ManyToManyField(related_name='house_additional_features', to='core.additionalfeatures', verbose_name='Дополнительные характеристики'),
        ),
        migrations.DeleteModel(
            name='TimeCost',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='reserve',
            name='start_time',
        ),
    ]