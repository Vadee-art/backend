# Generated by Django 3.1.7 on 2022-08-08 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0002_artist_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='email',
        ),
    ]
