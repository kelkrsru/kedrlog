# Generated by Django 4.2.4 on 2024-04-19 16:47

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staticpages', '0013_alter_contentprice_description_house_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentprice',
            name='description_spa_services',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Описание для программ парения'),
        ),
    ]
