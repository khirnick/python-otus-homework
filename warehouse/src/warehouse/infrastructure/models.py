from tortoise import fields
from tortoise import Model

from warehouse.domain.dto import CustomerDto, OrderDto, ProductDto


class Product(Model):

    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    price = fields.FloatField()

    async def as_dto(self) -> ProductDto:
        return ProductDto(
            id=self.id,
            name=self.name,
            price=self.price,
        )


class Customer(Model):
    
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    address = fields.TextField()
    email = fields.TextField()
    phone = fields.TextField()

    async def as_dto(self) -> CustomerDto:
        return CustomerDto(
            id=self.id,
            name=self.name,
            address=self.address,
            email=self.email,
            phone=self.phone,
        )


class Order(Model):
    
    id = fields.IntField(primary_key=True)
    customer = fields.ForeignKeyField(
        model_name='models.Customer',
        related_name='orders',
        on_delete=fields.CASCADE,
    )
    products = fields.ManyToManyField('models.Product', related_name='orders', through='order_product')

    async def as_dto(self) -> OrderDto:
        customer = await self.customer
        products = await self.products
        products = [product.as_dto() for product in products]
        return OrderDto(
            id=self.id,
            products=products,
            customer=customer.as_dto(),
        )
