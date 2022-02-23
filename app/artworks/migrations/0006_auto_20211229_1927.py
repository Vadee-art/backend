# Generated by Django 3.1.7 on 2021-12-29 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0005_auto_20211229_0734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='deliveredAt',
            new_name='delivered_at',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='shippingPrice',
            new_name='fee_eth',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='isDelivered',
            new_name='is_delivered',
        ),
        migrations.AddField(
            model_name='order',
            name='price_eth',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=7, null=True),
        ),
    ]