# Generated by Django 3.2.20 on 2023-11-24 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0029_auto_20231111_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='saved_artworks',
            field=models.ManyToManyField(related_name='users_saved', to='artworks.Artwork'),
        ),
    ]