# Generated by Django 4.2.4 on 2023-12-03 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_reserveservices_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserveservices',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, verbose_name='Общая стоимость'),
            preserve_default=False,
        ),
    ]
