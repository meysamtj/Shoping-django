# Generated by Django 4.2.9 on 2024-01-25 14:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_alter_discount_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 26, 22, 47, 31, 738546, tzinfo=datetime.timezone.utc), verbose_name='expire'),
        ),
    ]