# Generated by Django 3.2.20 on 2023-08-23 19:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0005_auto_20230615_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='artist',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='artworks',
                to='artworks.artist',
            ),
        ),
    ]
