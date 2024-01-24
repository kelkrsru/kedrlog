# Generated by Django 4.2.4 on 2023-12-03 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_socialnetworks_show_block_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateField(auto_now=True, verbose_name='Дата изменения')),
                ('quantity', models.PositiveIntegerField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('additional_service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.additionalservices')),
                ('reserve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.reserve')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='reserve',
            name='additional_services',
            field=models.ManyToManyField(through='core.ReserveServices', to='core.additionalservices', verbose_name='Дополнительные услуги'),
        ),
    ]
