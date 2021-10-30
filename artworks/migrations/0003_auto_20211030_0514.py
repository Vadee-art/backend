# Generated by Django 3.1.7 on 2021-10-30 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0002_artwork_is_carousel'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='/defaultImage.png', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='category',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
