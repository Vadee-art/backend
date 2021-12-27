# Generated by Django 3.1.7 on 2021-12-26 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voucher',
            old_name='price',
            new_name='edition',
        ),
        migrations.AddField(
            model_name='voucher',
            name='editionNumber',
            field=models.CharField(default='', max_length=350),
        ),
        migrations.AddField(
            model_name='voucher',
            name='priceDollar',
            field=models.CharField(default='', max_length=350),
        ),
        migrations.AddField(
            model_name='voucher',
            name='priceWei',
            field=models.CharField(default='', max_length=350),
        ),
    ]
