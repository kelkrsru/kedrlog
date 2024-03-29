# Generated by Django 4.2.4 on 2023-11-20 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_house_guests_in_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='guests_in_price',
        ),
        migrations.AddField(
            model_name='rate',
            name='additional_guest_price',
            field=models.DecimalField(decimal_places=2, default=1000.0, help_text='Доплата за дополнительного гостя за все время', max_digits=10, verbose_name='Доплата за дополнительного гостя'),
        ),
        migrations.AddField(
            model_name='rate',
            name='guests_in_price',
            field=models.PositiveSmallIntegerField(default=6, verbose_name='Количество гостей, включенных в стоимость'),
        ),
    ]
