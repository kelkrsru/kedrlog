# Generated by Django 4.2.4 on 2023-11-29 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0002_alter_contentblockbooking_background_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='houseshowbooking',
            options={'ordering': ['-house__active', 'house__name'], 'verbose_name': 'Расположение Парных на блоке Бронирования'},
        ),
    ]
