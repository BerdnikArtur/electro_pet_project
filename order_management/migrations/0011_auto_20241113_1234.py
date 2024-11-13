# Generated by Django 5.0.6 on 2024-11-13 12:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0010_auto_20241113_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]