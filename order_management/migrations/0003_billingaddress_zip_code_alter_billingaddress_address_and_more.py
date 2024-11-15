# Generated by Django 5.0.6 on 2024-07-05 08:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0002_remove_order_address_remove_order_cart_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='zip_code',
            field=models.CharField(default='123', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='address',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='country',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='telephone',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex='^(071)\\d{9}$')]),
        ),
    ]
