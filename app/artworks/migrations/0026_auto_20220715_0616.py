# Generated by Django 3.1.7 on 2022-07-15 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0025_auto_20220715_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='depth',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
