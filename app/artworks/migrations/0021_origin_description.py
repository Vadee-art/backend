# Generated by Django 3.1.7 on 2022-06-26 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0020_artwork_is_notable'),
    ]

    operations = [
        migrations.AddField(
            model_name='origin',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]