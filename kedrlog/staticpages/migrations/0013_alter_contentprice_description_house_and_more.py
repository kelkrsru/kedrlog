# Generated by Django 4.2.4 on 2024-04-19 16:09

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staticpages', '0012_textcontentrulesgiftcert_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentprice',
            name='description_house',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Описание для основных услуг'),
        ),
        migrations.AlterField(
            model_name='contentprice',
            name='description_service',
            field=ckeditor.fields.RichTextField(blank=True, max_length=1024, null=True, verbose_name='Описание для дополнительных услуг'),
        ),
    ]
