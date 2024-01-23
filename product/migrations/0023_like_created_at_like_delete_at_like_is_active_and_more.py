# Generated by Django 5.0.1 on 2024-01-21 17:02

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_alter_discount_expire_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created_at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='like',
            name='delete_at',
            field=models.DateField(blank=True, null=True, verbose_name='delete_at'),
        ),
        migrations.AddField(
            model_name='like',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is_active'),
        ),
        migrations.AddField(
            model_name='like',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='is_deleted'),
        ),
        migrations.AddField(
            model_name='like',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='updated_at'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 23, 1, 7, 18, 433646, tzinfo=datetime.timezone.utc), verbose_name='expire'),
        ),
    ]