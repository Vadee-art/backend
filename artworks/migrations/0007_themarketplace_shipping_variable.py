# Generated by Django 3.1.7 on 2021-12-29 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0006_auto_20211229_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='themarketplace',
            name='shipping_variable',
            field=models.FloatField(default=0, unique=True),
        ),
    ]
