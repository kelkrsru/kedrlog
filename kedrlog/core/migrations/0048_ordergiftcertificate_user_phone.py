# Generated by Django 4.2.4 on 2024-04-05 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_ordergiftcertificate_user_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordergiftcertificate',
            name='user_phone',
            field=models.CharField(blank=True, help_text='Телефон клиента', max_length=20, verbose_name='Телефон клиента'),
        ),
    ]
