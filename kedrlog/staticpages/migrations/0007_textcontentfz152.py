# Generated by Django 4.2.4 on 2024-01-27 08:01

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staticpages', '0006_delete_textcontentspa'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextContentFz152',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('seo_title', models.CharField(blank=True, max_length=60, verbose_name='Заголовок страницы')),
                ('seo_description', models.CharField(blank=True, max_length=160, verbose_name='Описание страницы')),
                ('seo_keywords', models.CharField(blank=True, max_length=100, verbose_name='Ключевые слова')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('header', models.CharField(help_text='Введите заголовок', max_length=255, verbose_name='Заголовок')),
                ('second_header', models.CharField(help_text='Введите подзаголовок', max_length=255, verbose_name='Подзаголовок')),
                ('active', models.BooleanField(default=False, help_text='Выберите в качестве активного. Текущий активный элемент потеряет этот статус', verbose_name='Активность')),
                ('text', ckeditor.fields.RichTextField(help_text='Текст для страницы', verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Контент для страницы Обработка ПД ФЗ-152',
                'verbose_name_plural': 'Контент для страницы Обработка ПД ФЗ-152',
            },
        ),
    ]
