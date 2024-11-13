from pydantic import BaseModel
from typing import Type
from core.domain.entities import Category as CategoryEntity
import uuid


class CategoryDTO(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    count_of_deals: int

    @classmethod
    def from_entity(cls: Type["CategoryDTO"], category: CategoryEntity) -> "CategoryDTO":
        return cls(
            id=uuid.UUID(str(category.id)) if not isinstance(category.id, uuid.UUID) else category.id,
            name=category.name,
            slug=category.slug,
            count_of_deals=category.count_of_deals,
        )
    
    class Config:
        orm_mode = True
