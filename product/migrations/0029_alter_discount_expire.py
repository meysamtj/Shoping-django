# Generated by Django 4.2.9 on 2024-01-25 15:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_alter_discount_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 23, 33, 39, 369179, tzinfo=datetime.timezone.utc), verbose_name='expire'),
        ),
    ]