from dataclasses import dataclass
from typing import Any, TypeVar
import uuid

@dataclass(kw_only=True)
class Entity:
    id: uuid.uuid4 = uuid.uuid4()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self.id == other.id
        else:
            return False
        
EntityType = TypeVar("EntityType", bound=Entity)