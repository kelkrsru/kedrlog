# Generated by Django 4.2.4 on 2023-09-11 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_reserve_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='paid',
            field=models.BooleanField(default=False, verbose_name='Оплачено'),
        ),
    ]