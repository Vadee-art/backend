# Generated by Django 3.1.7 on 2021-04-17 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0007_auto_20210414_0210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='image',
            field=models.ImageField(default='/defaultImage.png', null=True, upload_to=''),
        ),
    ]
