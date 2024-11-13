# Generated by Django 5.0.6 on 2024-11-13 12:34

from django.db import migrations
import uuid


def gen_uuid0(apps, schema_editor):
    MyModel = apps.get_model("cart_management", "Cart")
    for row in MyModel.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])

def gen_uuid1(apps, schema_editor):
    MyModel = apps.get_model("cart_management", "CartOrderProduct")
    for row in MyModel.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])

def gen_uuid2(apps, schema_editor):
    MyModel = apps.get_model("cart_management", "WishList")
    for row in MyModel.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])

def gen_uuid3(apps, schema_editor):
    MyModel = apps.get_model("cart_management", "WishListOrderProduct")
    for row in MyModel.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])

class Migration(migrations.Migration):

    dependencies = [
        ('cart_management', '0008_cart_uuid_cartorderproduct_uuid_wishlist_uuid_and_more'),
    ]

    operations = [
        migrations.RunPython(gen_uuid0, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(gen_uuid1, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(gen_uuid2, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(gen_uuid3, reverse_code=migrations.RunPython.noop),
    ]
