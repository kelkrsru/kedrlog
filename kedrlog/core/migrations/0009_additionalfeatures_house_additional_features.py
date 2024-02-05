# Generated by Django 4.2.4 on 2023-10-22 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_house_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('description', models.CharField(help_text='Выводится на странице бронирования', max_length=255, verbose_name='Описание')),
                ('icon', models.ImageField(help_text='Иконка в формате png 64*64 px', upload_to='img/houses/icons/', verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Дополнительная характеристика',
                'verbose_name_plural': 'Дополнительные характеристики',
            },
        ),
        migrations.AddField(
            model_name='house',
            name='additional_features',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.additionalfeatures', verbose_name='Дополнительные характеристики'),
        ),
    ]
