# Generated by Django 5.0.1 on 2024-01-25 03:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_alter_discount_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 11, 7, 52, 383480, tzinfo=datetime.timezone.utc), verbose_name='expire'),
        ),
    ]
