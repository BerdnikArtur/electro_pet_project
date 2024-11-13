from typing import List
from shop.models import Category as CategoryModel  # Import your Django model
from core.domain.entities import Category as CategoryEntity  # Import your entity
from .i_shop_management import ICategoryRepository

class CategoryRepository(ICategoryRepository):
    def get_all_categories(self, amount=None) -> List[CategoryEntity]:
        categories = CategoryModel.objects.all()[:amount] if amount else CategoryModel.objects.all()
        return [CategoryEntity(id=cat.id, name=cat.name, slug=cat.slug, count_of_deals=cat.count_of_deals) for cat in categories]

    def get_category_by_slug(self, slug: str) -> CategoryEntity:
        try:
            category = CategoryModel.objects.get(slug=slug)
            return CategoryEntity(id=category.slug, name=category.name, slug=category.slug, count_of_deals=category.count_of_deals)
        except CategoryModel.DoesNotExist:
            return None
        
    def get_categories_by_ids(self, ids: List[int]) -> List[CategoryEntity]:
        categories = [CategoryModel.objects.get(id=category_id) for category_id in ids]
        return [CategoryEntity(id=cat.id, name=cat.name, slug=cat.slug, count_of_deals=cat.count_of_deals) for cat in categories]

        