# Generated by Django 4.2.4 on 2024-10-24 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_remove_house_cost_include'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserve',
            name='rate',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='rate_reserves', to='core.rate', verbose_name='Тариф'),
        ),
    ]