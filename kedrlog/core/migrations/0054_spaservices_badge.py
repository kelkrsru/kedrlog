# Generated by Django 4.2.4 on 2024-04-19 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_badge'),
        ('core', '0053_spaservices_sort'),
    ]

    operations = [
        migrations.AddField(
            model_name='spaservices',
            name='badge',
            field=models.ForeignKey(blank=True, help_text='Плашка на карточке товара', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='spa_services', to='common.badge', verbose_name='Плашка'),
        ),
    ]
