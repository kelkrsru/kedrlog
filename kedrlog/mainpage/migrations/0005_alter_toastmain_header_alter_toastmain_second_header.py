# Generated by Django 4.2.4 on 2024-10-29 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0004_toastmain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toastmain',
            name='header',
            field=models.CharField(blank=True, help_text='Введите заголовок всплывающего окна', max_length=50, null=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='toastmain',
            name='second_header',
            field=models.CharField(blank=True, help_text='Введите подзаголовок всплывающего окна', max_length=50, null=True, verbose_name='Подзаголовок'),
        ),
    ]
