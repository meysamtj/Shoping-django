# Generated by Django 4.2.9 on 2024-01-25 13:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_alter_discount_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 21, 7, 41, 37912, tzinfo=datetime.timezone.utc), verbose_name='expire'),
        ),
    ]