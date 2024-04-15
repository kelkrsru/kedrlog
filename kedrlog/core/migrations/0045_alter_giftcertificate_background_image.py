# Generated by Django 4.2.4 on 2024-03-31 13:29

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_remove_giftcertificate_header_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='giftcertificate',
            name='background_image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, help_text='Изображение отображается в фоне карточки Подарочного сертификата', keep_meta=True, quality=-1, scale=None, size=[600, 400], upload_to='img/giftcert/', verbose_name='Файл фонового изображения'),
        ),
    ]
