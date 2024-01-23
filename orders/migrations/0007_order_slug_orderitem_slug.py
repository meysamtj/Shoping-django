# Generated by Django 4.2.7 on 2024-01-21 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='slug'),
        ),
    ]