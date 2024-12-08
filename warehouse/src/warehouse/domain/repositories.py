from abc import ABC, abstractmethod
from typing import List
from .dto import CustomerDto, ProductDto, OrderDto


class ProductDtoRepository(ABC):

    @abstractmethod
    async def add(self, product: ProductDto):
        pass

    @abstractmethod
    async def get(self, product_id: int) -> ProductDto:
        pass

    @abstractmethod
    async def list(self) -> List[ProductDto]:
        pass

    @abstractmethod
    async def delete(self, product_id: int) -> None:
        pass


class CustomerDtoRepository(ABC):

    @abstractmethod
    async def add(self, customer: CustomerDto):
        pass

    @abstractmethod
    async def get(self, customer_id: int) -> CustomerDto:
        pass

    @abstractmethod
    async def list(self) -> List[CustomerDto]:
        pass

    @abstractmethod
    async def delete(self, customer_id: int) -> None:
        pass


class OrderDtoRepository(ABC):

    @abstractmethod
    async def add(self, order: OrderDto):
        pass

    @abstractmethod
    async def get(self, order_id: int) -> OrderDto:
        pass

    @abstractmethod
    async def list(self) -> List[OrderDto]:
        pass

    @abstractmethod
    async def delete(self, order_id: int) -> None:
        pass
