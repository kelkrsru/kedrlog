# Generated by Django 4.2.4 on 2024-01-13 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_b24',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='ID пользователя в Б24'),
        ),
    ]
