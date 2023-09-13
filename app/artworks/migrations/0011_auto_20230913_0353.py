# Generated by Django 3.2.20 on 2023-09-13 00:23

import django.db.models.deletion
from django.apps import apps
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
        ('artworks', '0010_auto_20230913_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='region',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='cities_light.region',
            ),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='city',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='cities_light.city',
            ),
        ),
    ]
