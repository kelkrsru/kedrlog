# Generated by Django 4.2.4 on 2024-01-27 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_settingssite_reserve_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalservices',
            name='group',
            field=models.PositiveSmallIntegerField(blank=True, help_text='Услуга/товар входит в группу. На странице бронирования можно будет выбрать только один из группы.', null=True, verbose_name='Группа'),
        ),
    ]
