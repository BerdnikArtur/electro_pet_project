# Generated by Django 5.0.6 on 2024-07-05 07:40

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='country',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='order',
            name='long',
        ),
        migrations.RemoveField(
            model_name='order',
            name='telephone',
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='stripe_payment_intent_id',
            field=models.CharField(default='2', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=5.55, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=225)),
                ('last_name', models.CharField(max_length=225)),
                ('address', models.CharField(max_length=225)),
                ('city', models.CharField(max_length=225)),
                ('country', models.CharField(max_length=225)),
                ('telephone', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(regex='^(05)\\d{9}$')])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.order')),
            ],
        ),
    ]
