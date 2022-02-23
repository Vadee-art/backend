# Generated by Django 3.1.7 on 2021-12-30 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0011_auto_20211230_0212'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artwork',
            name='NFT',
        ),
        migrations.AddField(
            model_name='thetoken',
            name='artwork',
            field=models.ManyToManyField(blank=True, default=None, related_name='token_artwork', to='artworks.Artwork'),
        ),
    ]