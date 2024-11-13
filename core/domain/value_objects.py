from dataclasses import dataclass

@dataclass(frozen=True)
class CategoryName:
    value: str

    def __post_init__(self):
        if len(self.value) < 3:
            raise ValueError(f"{self.__class__.__name__}: Category name must contain 3 characters at least")
        
@dataclass(frozen=True)
class CategorySlug:
    value: str

    def __post_init__(self):
        if len(self.value) < 3:
            raise ValueError(f"{self.__class__.__name__}: Category slug must contain 3 characters at least")