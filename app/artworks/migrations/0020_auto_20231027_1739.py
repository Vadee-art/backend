# Generated by Django 3.2.20 on 2023-10-27 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('artworks', '0019_auto_20231015_2318'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Genre',
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'genre',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.RemoveField(
            model_name='artwork',
            name='category',
        ),
        migrations.RemoveField(
            model_name='artwork',
            name='origin',
        ),
        migrations.RemoveField(
            model_name='artwork',
            name='sub_category',
        ),
        migrations.AddField(
            model_name='artwork',
            name='genre',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='genre',
                to='artworks.genre',
                null=True,
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='SubCategory',
        ),
    ]