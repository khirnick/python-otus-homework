from warehouse.domain.services import WarehouseService
from warehouse.infrastructure.orm import init
from warehouse.infrastructure.unit_of_work import Uow
from warehouse.infrastructure.repositories import TortoiseCustomerRepository, TortoiseOrderRepository, TortoiseProductRepository


async def main():
    await init()
    product_repository = TortoiseProductRepository()
    customer_repository = TortoiseCustomerRepository()
    order_repository = TortoiseOrderRepository()
    service = WarehouseService(product_repository, customer_repository, order_repository)

    async with Uow() as _:
        product_player = await service.create_product(name='Player X', price=100)
        product_headphones = await service.create_product(name='Headphones', price=20)
        product_cable = await service.create_product(name='Cable USB-C', price=5)
        customer = await service.create_customer(name='Ivan', address='Moscow', email='ivan@ivan.ru', phone='123456')
        products = [product_player, product_headphones, product_cable]
        await service.create_order(products, customer)

    async with Uow() as uow:
        product_screw = await service.create_product(name='Screw', price=5)
        product_puck = await service.create_product(name='Puck', price=3)
        product_wrench = await service.create_product(name='Wrench', price=10)
        customer = await service.create_customer(name='Sergey', address='Moscow', email='sergey@sergey.ru', phone='123456')
        products = [product_screw, product_puck, product_wrench]
        await service.create_order(products, customer)
        if product_wrench.price > 8:
            await uow.rollback()


if __name__ == "__main__":
    main()


