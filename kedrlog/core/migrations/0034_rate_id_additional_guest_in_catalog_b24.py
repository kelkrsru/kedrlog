# Generated by Django 4.2.4 on 2024-01-19 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_settingsbitrix24_is_reserve_site_field_code_b24_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='id_additional_guest_in_catalog_b24',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='ID товара дополнительного гостя в каталоге Битрикс24'),
        ),
    ]