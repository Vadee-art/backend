# Generated by Django 3.2.20 on 2023-09-13 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0011_auto_20230913_0353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='country',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='region',
        ),
    ]
