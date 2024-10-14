# Generated by Django 5.0.6 on 2024-07-08 07:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0003_billingaddress_zip_code_alter_billingaddress_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.DecimalField(decimal_places=2, max_digits=10)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10)),
                ('height', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
                ('distance_unit', models.CharField(default='in', max_length=10)),
                ('mass_unit', models.CharField(default='lb', max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='address',
            field=models.CharField(default='qwerty', max_length=225),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(default='qwerty', max_length=225),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='country',
            field=models.CharField(default='qwerty', max_length=225),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='processing', max_length=20),
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('label_url', models.URLField(blank=True, null=True)),
                ('carrier', models.CharField(blank=True, max_length=50, null=True)),
                ('shipping_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('from_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_shipments', to='order_management.billingaddress')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.order')),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.parcel')),
                ('to_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_shipments', to='order_management.billingaddress')),
            ],
        ),
    ]