# Generated by Django 4.2.7 on 2024-01-31 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_address_created_at_alter_customuser_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='created_at'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='is_active'),
        ),
    ]