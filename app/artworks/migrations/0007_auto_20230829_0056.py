# Generated by Django 3.2.20 on 2023-08-28 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0006_auto_20230823_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]