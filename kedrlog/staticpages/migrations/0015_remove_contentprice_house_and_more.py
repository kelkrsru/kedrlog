# Generated by Django 4.2.4 on 2024-08-28 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staticpages', '0014_contentprice_description_spa_services'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentprice',
            name='house',
        ),
        migrations.RemoveField(
            model_name='contentprice',
            name='service',
        ),
        migrations.AddField(
            model_name='contentprice',
            name='is_show_card_image',
            field=models.BooleanField(default=False, help_text='Показывать фото в карточке тарифа парной', verbose_name='Показывать фото в карточке'),
        ),
    ]
