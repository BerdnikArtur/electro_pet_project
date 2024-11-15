# Generated by Django 5.0.6 on 2024-07-11 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_remove_productrating_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.CreateModel(
            name='MultipleProductParameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=225, null=True)),
                ('size', models.CharField(max_length=225, null=True)),
                ('length', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('width', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('height', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
            ],
        ),
    ]
