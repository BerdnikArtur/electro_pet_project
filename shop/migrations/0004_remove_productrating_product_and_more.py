# Generated by Django 5.0.6 on 2024-06-16 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_orderproduct_cart_alter_order_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productrating',
            name='product',
        ),
        migrations.RemoveField(
            model_name='review',
            name='product_rating',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='ProductRating',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]
