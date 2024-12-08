from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class ProductDto:

    id: int
    name: str
    price: float


@dataclass(frozen=True)
class CustomerDto:

    id: int
    name: str
    address: str
    email: str
    phone: str


@dataclass(frozen=True)
class OrderDto:

    id: int
    customer: CustomerDto
    products: List[ProductDto] = field(default_factory=list)

    def add_product(self, product: ProductDto):
        self.products.append(product)
