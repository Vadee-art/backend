# Generated by Django 3.1.7 on 2022-08-08 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0005_auto_20220807_0612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artwork',
            name='isPrice',
        ),
    ]
