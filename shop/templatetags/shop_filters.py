from django import template
from django.http import HttpRequest

from shop.models import Product

from datetime import datetime, timedelta

register = template.Library()

@register.filter
def int_to_range(value: int) -> range:
    return range(int(value))
    
@register.filter
def subtract(value1: int, value2: int) -> int:
    return value1 - value2

@register.filter
def get_price_with_discount(item: Product) -> bool:
    if isinstance(item, Product):
        if item.discount:
            return "{:.2f}".format(item.price - (item.price / 100) * item.discount)
        else:
            return item.price
    return ''
    
@register.filter
def get_status_of_new(item: Product) -> bool:
    if isinstance(item, Product):
        yesterday = datetime.today() - timedelta(weeks=1)
            
        if item.time_created.timestamp() >= yesterday.timestamp():
            return True
        else:
            return False
    return ''
    
@register.filter
def absolute_url(req: HttpRequest, product: Product) -> str:
    if isinstance(product, Product):
        return req.build_absolute_uri(product.get_absolute_url())
    return ''
    