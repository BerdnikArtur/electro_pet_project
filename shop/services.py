from django.db.models.manager import BaseManager
from django.http import HttpRequest, Http404
from django.forms import BaseForm
from django.db.models import QuerySet, Q
from django.utils.translation import gettext as _
from django.utils import timezone

from typing import Any
from datetime import timedelta

from .models import Product, Category, MultipleProductImages, ProductSizes
from .forms import FiltersAside

from cart_management.forms import AddToCartForm, AddToWishlistForm
from review_management.models import Review
from review_management.services import ProductPageReviewsService

from utils.mixins.cache_mixin import BaseCachingMixin
from utils.services.base_service import BaseService


class HomePageService(BaseService):

    def _get_hot_deals(self) -> BaseManager[Product]:
        hot_week = timezone.now() - timedelta(days=7)
        hot_deals = Product.objects.filter(time_created__gte=hot_week).select_related('category').prefetch_related('product_sizes')
        return hot_deals
    
    def _get_slick_tablet(self, amount: int) -> list:
        slick_tablet = []
        for i in range(3, amount+3, 3):
            slick_tablet.append(self.get_top_selling(i, i-3))

        return slick_tablet

    def get_context_data(self, request: HttpRequest, context: dict[str: Any]) -> dict[str: Any]:
        
        header_and_footer_context = self.get_header_and_footer(request)

        context['hot_deals'] = self._get_hot_deals()
        context['top_selling'] = self.get_top_selling(5)
        context['slick_tablet'] = self._get_slick_tablet(6)

        return {**header_and_footer_context, **context}

class StorePageService(BaseService):
    
    def get_context_data(self, request: HttpRequest, context: dict[str: Any], form_class: type[BaseForm]) -> dict[str: Any]:
        
        header_and_footer_context = self.get_header_and_footer(request)

        context['filters_aside'] = form_class
        context['category_aside'] = self.get_cached_query("category_aside", Category.objects.all()[:6])
        context['brands'] = ['SAMSUNG', 'LG', 'SONY', 'POCO', 'NVIDIA', 'AMD']
        context['tablet_aside'] = self.get_top_selling(3)
        
        cookie = request.session.get('additional_data', None)
        if request.method == "GET" and cookie:
            context['checkbox_categories'] = [str(Category.objects.get(slug=request.session.get('category')).pk)]
        elif request.method == "POST":
            context['select_option_sort_by'] = request.POST.get('sort_by')
            context['checkbox_categories'] = request.POST.getlist('category', [])
            context['checkbox_brands'] = request.POST.getlist('brand', [])

        return {**header_and_footer_context, **context}
    
    def _get_session_data(self, request):
            return {
                "query": request.session.get("search-query"),
                "category_id": request.session.get("search-category", '0')
            }

    def _clear_session_data(self, request):
        request.session.pop("search-query", None)
        request.session.pop("search-category", '0')

    def _handle_post_request(self, request):
        form = FiltersAside(request.POST.copy())
        if form.is_valid():
            self._clear_session_data(request)
            return self._filter_products(form.cleaned_data)
        return self.get_top_selling()

    def _handle_get_request(self, request, **kwargs):
        self._clear_session_data(request)
        if kwargs:
            return self._filter_products_by_slug_of_category(**kwargs)
        return self.get_top_selling()

    def _handle_session_data(self, session_data):
        query = session_data["query"]
        category_id = session_data["category_id"]

        filters = Q()
        if query:
            filters &= Q(name__icontains=query)
        if category_id and category_id != '0':
            filters &= Q(category_id=category_id)
        
        if filters:
            return Product.objects.filter(filters).select_related('category').prefetch_related('product_sizes')
        
        return self.get_top_selling()
    
    def _filter_products(data: dict[str, Any]) -> BaseManager[Product]:
        if data['category'] and data['brand']:
            return Product.objects.all().order_by(data['sort_by']).filter(Q(price__gt=data['price__min']) & Q(price__lt=data['price__max']) & Q(category__in=data['category']) & Q(brand__in=data['brand']))
        elif not data['category'] and not data['brand']:
            return Product.objects.all().order_by(data['sort_by']).filter(Q(price__gt=data['price__min']) & Q(price__lt=data['price__max']))
        elif not data['category']:
            return Product.objects.all().order_by(data['sort_by']).filter(Q(price__gt=data['price__min']) & Q(price__lt=data['price__max']) & Q(brand__in=data['brand']))
        elif not data['brand']:
            return Product.objects.all().order_by(data['sort_by']).filter(Q(price__gt=data['price__min']) & Q(price__lt=data['price__max']) & Q(category__in=data['category']))
        
    def _filter_products_by_slug_of_category(*args, **kwargs) -> BaseManager[Product]:
        return Product.objects.filter(category__slug=kwargs['category'])

    def get_queryset(self, request: HttpRequest, *args, **kwargs) -> BaseManager[Product]:
        
        if request.method == 'POST':
            return self._handle_post_request(request)

        if request.method == 'GET':
            session_data = self._get_session_data(request)

            clear_session = request.GET.get('clear_session', 'false').lower() == 'true'
            
            if clear_session:
                self._clear_session_data(request)
                return self._handle_get_request(request, **kwargs)

            if session_data["query"] or session_data["category_id"] != '0':
                return self._handle_session_data(session_data)
            return self._handle_get_request(request, **kwargs)

        return self.get_top_selling()

    def post(self, request: HttpRequest) -> dict[str: Any]:
        return {
            'select_option_sort_by': request.POST.get('sort_by'),
            'checkbox_categories': request.POST.getlist('category', []),
            'checkbox_brands': request.POST.getlist('brand', []),
        }
    
class ProductPageService(BaseService):

    def get_context_data(self, request: HttpRequest, context: dict[str: Any], object: Any) -> dict[str: Any]:
        header_and_footer = self.get_header_and_footer(request)

        context['product_images'] = MultipleProductImages.objects.filter(product=object)
        context['related_products'] = Product.objects.filter(brand=object.brand)[:10].select_related('category')
        context['reviews'] = self.get_cached_query("reviews", Review.objects.filter(product_rating=object.product_rating).order_by("-date_created").select_related('user')[:5])
        context['rating'] = object.product_rating
        context['stars'] = ProductPageReviewsService.get_list_of_all_stars_by_product_rating(object.product_rating)[::-1]

        if request.user.is_authenticated:
            context['add_to_cart'] = AddToCartForm(object=object, cart_pk=request.user.cart.pk)
            context['add_to_wishlist'] = AddToWishlistForm(object=object, wishlist_pk=request.user.wishlist.pk) 
 
        return {**header_and_footer, **context}

    @BaseCachingMixin.cache_result("get_object_{data_kwargs}")
    def get_object(self, data_kwargs: Any, queryset: QuerySet[Any]) -> Any:
        category_slug = data_kwargs.get('category', None)
        product_slug = data_kwargs.get('product', None)
        try:
            obj = queryset.prefetch_related("product_sizes").get(category__slug=category_slug, slug=product_slug)
        except queryset.model.DoesNotExist:
            raise Http404(_("No product found matching the query"))
        return obj

    def post(self, request: HttpRequest, object: Any) -> None:
        data = request.POST.copy()
        data['product'] = object.pk
        data['cart'] = request.user.cart.pk
        form = AddToCartForm(data, object=object, cart_pk=request.user.cart.pk)
        if form.is_valid():
            form.save() 


def pop_session_data(request: HttpRequest, key: str, exception: Any):
    value = request.session.get(key, exception)
    if key in request.session:
        del request.session[key]
    return value