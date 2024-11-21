# Generated by Django 4.2.4 on 2024-11-21 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_alter_price_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='max_guests',
        ),
        migrations.AddField(
            model_name='house',
            name='comfort',
            field=models.PositiveSmallIntegerField(default=10, verbose_name='Комфортное размещение'),
        ),
    ]