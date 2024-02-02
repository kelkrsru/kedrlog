# Generated by Django 4.2.4 on 2024-01-22 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_alter_settingsbitrix24_stage_id_for_deal_adding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='deal_id_b24',
            field=models.PositiveIntegerField(blank=True, help_text='ID сделки в Битрикс24', null=True, unique=True, verbose_name='ID сделки в Битрикс24'),
        ),
    ]