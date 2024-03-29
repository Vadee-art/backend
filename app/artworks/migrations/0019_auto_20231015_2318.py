# Generated by Django 3.2.20 on 2023-10-15 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0018_auto_20231005_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='show_in_homepage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='origin',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='voucher',
            name='artwork_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vouchers', to='artworks.artwork'),
        ),
    ]
