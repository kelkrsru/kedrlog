# Generated by Django 4.2.4 on 2023-12-16 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_priceforspaservices_remove_spaservices_duration_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='priceforspaservices',
            options={'verbose_name': 'Цена для программ парения', 'verbose_name_plural': 'Цены для программ парения'},
        ),
        migrations.RemoveField(
            model_name='priceforspaservices',
            name='min_guest',
        ),
    ]
