from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from .managers import ProductRatingManager


class ProductRating(models.Model):
    rating = models.DecimalField(max_digits=3, decimal_places=1, editable=False, null=True)
    product = models.OneToOneField('shop.Product', on_delete=models.CASCADE, related_name='product_rating')

    objects = ProductRatingManager()

    # def update_rating(self, item, increase=True):
    #     rating_count = RatingCount.objects.get_or_create(stars=item, product_rating=self)
    #     rating_count.count += 1 if increase else -1
    #     rating_count.save()

    #     ratingcount = self.ratingcount_set.all()

    #     total_reviews = sum(rc.count for rc in ratingcount)
    #     total_rating = sum(rc.stars * rc.count for rc in ratingcount)
    #     self.rating = total_rating / total_reviews if total_reviews > 0 else None
    #     self.save()


# class ProductRating(models.Model):
#     rating = models.DecimalField(max_digits=3, decimal_places=1, editable=False, null=True)
#     one_star = models.PositiveSmallIntegerField(default=0, editable=False)
#     two_star = models.PositiveSmallIntegerField(default=0, editable=False)
#     three_star = models.PositiveSmallIntegerField(default=0, editable=False)
#     four_star = models.PositiveSmallIntegerField(default=0, editable=False)
#     five_star = models.PositiveSmallIntegerField(default=0, editable=False)
#     product = models.OneToOneField('shop.Product', on_delete=models.CASCADE, related_name='product_rating')

#     def update_rating(self, item, increase=True):
#         match item:
#             case 1:
#                 self.one_star += 1 if increase == True else -1
#             case 2:
#                 self.two_star += 1 if increase == True else -1
#             case 3:
#                 self.three_star += 1 if increase == True else -1
#             case 4:
#                 self.four_star += 1 if increase == True else -1
#             case 5:
#                 self.five_star += 1 if increase == True else -1

#         total_reviews = self.one_star + self.two_star + self.three_star + self.four_star + self.five_star
#         total_rating =  1 * self.one_star + 2 * self.two_star + 3 * self.three_star + 4 * self.four_star + 5 * self.five_star

#         self.rating = total_rating / total_reviews if total_reviews > 0 else None

#         self.save()

class Review(models.Model):
    '''
    Model of reviews for products
    '''
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

