from abc import abstractmethod
from typing import List
from core.domain.entities import *

from ..base_repository import BaseRepository

class ICategoryRepository(BaseRepository):
    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        pass

    @abstractmethod
    def get_category_by_slug(self, slug: str) -> Category:
        pass

    @abstractmethod
    def get_categories_by_ids(self, ids: List[int]) -> List[Category]:
        pass