# Generated by Django 4.2.4 on 2023-09-07 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_timecost_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='rate',
            field=models.ManyToManyField(related_name='rate_time_cost', to='core.timecost', verbose_name='Интервалы тарификации'),
        ),
    ]
