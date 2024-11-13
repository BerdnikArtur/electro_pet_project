from typing import Any

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect

from .forms import *
from core.application.services.internal.shop_management import *

from shared.mixins.base_service_mixin import BaseViewMixin
from core.infrastructure.repositories.shop_management.shop_management import *


class HomePage(ListView, BaseViewMixin):
    model = Product
    service_class = HomePageService
    repository_classes = {}
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return self.service.get_context_data(request=self.request, context=context)
    

class StorePage(ListView, FormMixin, BaseViewMixin):
    model = Product
    service_class = StorePageService
    repository_classes = {
        'category_repository': CategoryRepository,
    } 
    template_name = 'shop/store.html'
    slug_url_kwargs = 'category'
    paginate_by = 9
    form_class = FiltersAside

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return self.service.get_context_data(self.request, context, self.form_class)
    
    def get_queryset(self):
        return self.service.get_queryset(self.request, *self.args, **self.kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()

        self.service.post(request)
        
        return self.render_to_response(context)

class ProductPage(DetailView, BaseViewMixin):
    model = Product
    service_class = ProductPageService
    template_name = 'shop/product.html'
    slug_field = "slug" 
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(ProductPage, self).get_context_data(**kwargs)

        return self.service.get_context_data(self.request, context, self.object)
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return self.service.get_object(self.kwargs, queryset)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.get_context_data(object=self.object)
        
        if request.method == 'POST':
            self.service.post(request, self.object)

        return HttpResponseRedirect(self.object.get_absolute_url())


def search(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)

    #Any logic

    request.session['search-query'] = query
    request.session['search-category'] = category_id

    return HttpResponseRedirect(reverse_lazy('store'))