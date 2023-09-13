# Generated by Django 3.2.20 on 2023-09-13 00:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0010_auto_20230913_0319'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.region'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city'),
        ),
    ]
