from shared.entity import *
from .value_objects import *

@dataclass
class Category(Entity):
    name: CategoryName
    slug: CategorySlug
    count_of_deals: int = 0
