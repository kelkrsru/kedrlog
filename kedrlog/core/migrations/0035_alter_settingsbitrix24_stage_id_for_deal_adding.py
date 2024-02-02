# Generated by Django 4.2.4 on 2024-01-21 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_rate_id_additional_guest_in_catalog_b24'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingsbitrix24',
            name='stage_id_for_deal_adding',
            field=models.CharField(default=6, help_text='ID стадии воронки сделок для создания сделки бронирования с сайта в CRM', max_length=10, verbose_name='ID стадии для создания сделки'),
        ),
    ]