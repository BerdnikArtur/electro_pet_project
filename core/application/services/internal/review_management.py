from django.http import HttpRequest, JsonResponse
from django.db import transaction
from django.db.models import Count
from django.core.paginator import Paginator

from review_management.forms import ReviewForm
from review_management.models import Review, ProductRating

import json

class ProductPageReviewsService:

    @staticmethod
    def create_review(request: HttpRequest) -> JsonResponse:
        data = json.load(request)
        form = ReviewForm(data)
        if form.is_valid():
            review = form.save()

            rating_list = ProductPageReviewsService.get_list_of_all_stars_by_product_rating(review.product_rating)
            
            response_data = {
                'rating': review.product_rating.rating,
                'rating_list': rating_list,
            }
            return JsonResponse(response_data)
        
    @staticmethod
    def get_list_of_all_stars_by_product_rating(product_rating):
        rating_counts = Review.objects.filter(product_rating=product_rating)\
                .values('rating')\
                .annotate(count=Count('rating'))

        # Create a list of review counts for each star (1 to 5)
        return [next((rc['count'] for rc in rating_counts if rc['rating'] == i), 0) for i in range(1, 6)]

        
    @staticmethod
    def load_reviews(request: HttpRequest) -> JsonResponse:
        product_rating_id = request.GET.get("product_rating_id")
        reviews = Review.objects.filter(product_rating=product_rating_id).order_by("-date_created")

        paginator = Paginator(reviews, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        reviews_data = list(page_obj.object_list.values('text', 'rating', 'date_created', 'user__username'))
        for review in reviews_data:
            review['date_created'] = review['date_created'].strftime("%d %B %Y, %-I:%M %p")

        data = {
            'reviews_data': reviews_data,
            'num_pages': [i for i in paginator.page_range],
            'current_page': page_number,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(), 
        }

        return JsonResponse(data)