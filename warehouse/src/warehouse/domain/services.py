from typing import List
from .dto import ProductDto, CustomerDto, OrderDto
from .repositories import CustomerDtoRepository, ProductDtoRepository, OrderDtoRepository


class WarehouseService:

    def __init__(self, product_repo: ProductDtoRepository, customer_repo: CustomerDtoRepository, order_repo: OrderDtoRepository):
        self.product_repo = product_repo
        self.customer_repo = customer_repo
        self.order_repo = order_repo

    async def create_product(self, name: str, price: float) -> ProductDto:
        product = ProductDto(id=None, name=name, price=price)
        await self.product_repo.add(product)
        return product
    
    async def create_customer(self, name: str, address: str, email: str, phone: str) -> CustomerDto:
        customer = CustomerDto(id=None, name=name, address=address, email=email, phone=phone)
        await self.customer_repo.add(customer)
        return customer

    async def create_order(self, products: List[ProductDto], customer: CustomerDto) -> OrderDto:
        order=OrderDto(id=None, products=products, customer=customer)
        await self.order_repo.add(order)
        return order
