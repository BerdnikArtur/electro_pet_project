# Generated by Django 5.0.6 on 2024-09-28 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review_management', '0002_remove_productrating_five_star_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RatingCount',
        ),
    ]
