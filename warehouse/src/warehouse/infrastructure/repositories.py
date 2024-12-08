from typing import List
from warehouse.domain.repositories import CustomerDtoRepository, OrderDtoRepository, ProductDtoRepository
from warehouse.domain.dto import CustomerDto, OrderDto, ProductDto
from warehouse.infrastructure.models import Customer, Order, Product


class TortoiseProductRepository(ProductDtoRepository):
    
    async def add(self, product: ProductDto):
        product_db = Product(
            name=product.name,
            price=product.price,
        )
        await product_db.save()

    async def get(self, product_id: int) -> ProductDto:
        p = await Product.get_or_none(id=product_id)
        return await p.as_dto() if p else None

    async def list(self) -> List[ProductDto]:
        pp = await Product.all()
        return [await p.as_dto() for p in pp]

    async def delete(self, product_id: int) -> None:
        await Product.delete(id=product_id)


class TortoiseCustomerRepository(CustomerDtoRepository):
    
    async def add(self, customer: CustomerDto):
        customer_db = Customer(
            name=customer.name,
            address=customer.address,
            email=customer.email,
            phone=customer.phone,
        )
        await customer_db.save()

    async def get(self, customer_id: int) -> CustomerDto:
        c = await Customer.get_or_none(id=customer_id)
        return await c.as_dto() if c else None

    async def list(self) -> List[CustomerDto]:
        cc = await Customer.all()
        return [await c.as_dto() for c in cc]

    async def delete(self, customer_id: int) -> None:
        await Customer.delete(id=customer_id)


class TortoiseOrderRepository(OrderDtoRepository):
    
    async def add(self, order: OrderDto):
        products = [await Product.get(id=product.id) for product in order.products]
        order_db = Order(
            customer=await Customer.get(id=order.customer.id),
            products=products,
        )
        await order_db.save()

    async def get(self, order_id: int) -> OrderDto:
        o = await Order.get_or_none(id=order_id)
        return await o.as_dto() 

    async def list(self) -> List[OrderDto]:
        oo = await Order.all()
        return [await o.as_dto() for o in oo]

    async def delete(self, order_id: int) -> None:
        await Order.delete(id=order_id)
