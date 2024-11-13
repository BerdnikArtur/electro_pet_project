from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from .managers import ProductRatingManager

import uuid

class ProductRating(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, editable=False, null=True)
    product = models.OneToOneField('shop.Product', on_delete=models.CASCADE, related_name='product_rating')

    objects = ProductRatingManager()


class Review(models.Model):
    '''
    Model of reviews for products
    '''
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("user_management.CustomUser", on_delete=models.CASCADE)
    product_rating = models.ForeignKey(ProductRating, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('review', kwargs={'category': self.product.category.slug, 'product': self.product.slug})

    def delete(self, *args, **kwargs):
        ProductRating.objects.update_rating(self.product_rating)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ProductRating.objects.update_rating(self.product_rating)

