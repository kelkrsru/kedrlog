# Generated by Django 4.2.4 on 2024-08-18 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_alter_price_options_alter_weeks_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeks',
            name='name',
            field=models.CharField(default='test', help_text='Наименование дня недели', max_length=255, verbose_name='Наименование'),
            preserve_default=False,
        ),
    ]