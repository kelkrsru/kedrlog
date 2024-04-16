# Generated by Django 4.2.4 on 2024-03-30 03:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0042_alter_giftcertificate_id_catalog_b24'),
    ]

    operations = [
        migrations.CreateModel(
            name='GiftCertificateType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
                ('value', models.CharField(max_length=255, verbose_name='Значение')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Тип подарочного сертификата',
                'verbose_name_plural': 'Типы подарочных сертификатов',
            },
        ),
        migrations.AddField(
            model_name='giftcertificate',
            name='validity',
            field=models.PositiveSmallIntegerField(default=0, help_text='Срок действия сертификата в днях. По умолчанию 0 - неограничен', verbose_name='Срок действия'),
        ),
        migrations.CreateModel(
            name='OrderGiftCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('buy_date_time', models.DateTimeField(default=django.utils.timezone.now, help_text='Дата и время оплаты сертификата', verbose_name='Дата и время оплаты')),
                ('validity_date_time', models.DateField(blank=True, help_text='Дата и время, до которых сертификат действителен. Если не заполнено, то срок неограничен', null=True, verbose_name='Действителен до')),
                ('price', models.DecimalField(decimal_places=2, help_text='Стоимость сертификата', max_digits=10, verbose_name='Стоимость')),
                ('paid', models.BooleanField(default=False, help_text='Сумма сертификата оплачена клиентом', verbose_name='Оплачено')),
                ('sent_email', models.BooleanField(default=False, help_text='Сертификат и детали заказа отправлены на email клиента', verbose_name='Отправлено на email')),
                ('sent_bitrix', models.BooleanField(default=False, help_text='Отправлено в Битрикс24, создана сделка', verbose_name='Отправлено в Битрикс24')),
                ('deal_id_b24', models.PositiveIntegerField(blank=True, help_text='ID сделки в Битрикс24', null=True, unique=True, verbose_name='ID сделки в Битрикс24')),
                ('type', models.ForeignKey(help_text='Тип выбранного сертификата', on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='core.giftcertificatetype', verbose_name='Тип сертификата')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ на подарочный сертификат',
                'verbose_name_plural': 'Заказы на подарочные сертификаты',
            },
        ),
        migrations.AddField(
            model_name='giftcertificate',
            name='type',
            field=models.ManyToManyField(help_text='Тип подарочного сертификата', related_name='gift_certificates', to='core.giftcertificatetype', verbose_name='Тип'),
        ),
    ]