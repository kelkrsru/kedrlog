# Generated by Django 4.2.4 on 2023-10-22 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_additionalfeatures_house_additional_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='additional_features',
        ),
        migrations.AddField(
            model_name='house',
            name='additional_features',
            field=models.ManyToManyField(blank=True, null=True, related_name='house_additional_features', to='core.additionalfeatures', verbose_name='Дополнительные характеристики'),
        ),
    ]