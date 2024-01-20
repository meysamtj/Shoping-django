# Generated by Django 4.2.7 on 2024-01-20 11:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_alter_discount_expire_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='expire',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 21, 19, 53, 39, 838257, tzinfo=datetime.timezone.utc), verbose_name='expire'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, height_field='200', null=True, upload_to='products', verbose_name='image', width_field='400'),
        ),
    ]