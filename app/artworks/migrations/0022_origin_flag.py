# Generated by Django 3.1.7 on 2022-06-26 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0021_origin_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='origin',
            name='flag',
            field=models.ImageField(default='/defaultImage.png', null=True, upload_to=''),
        ),
    ]
