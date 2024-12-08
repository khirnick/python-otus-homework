from unittest.mock import AsyncMock
import pytest

from warehouse.domain.services import WarehouseService


@pytest.mark.asyncio
async def test_WarehouseService__create_product(mocker):
    # arrange
    mocked_product_repo = mocker.Mock()
    mocked_product_repo.add = AsyncMock()
    mocked_ProductDto = mocker.patch('warehouse.domain.services.ProductDto')
    service = WarehouseService(mocked_product_repo, 'no matter', 'no matter')

    # act
    result = await service.create_product('some name', 'some price')

    # assert
    mocked_ProductDto.assert_called_once_with(id=None, name='some name', price='some price')
    mocked_product_repo.add.assert_called_once_with(mocked_ProductDto())
    assert result is mocked_ProductDto()


@pytest.mark.asyncio
async def test_WarehouseService__create_customer(mocker):
    # arrange
    mocked_customer_repo = mocker.Mock()
    mocked_customer_repo.add = AsyncMock()
    mocked_CustomerDto = mocker.patch('warehouse.domain.services.CustomerDto')
    service = WarehouseService('no matter', mocked_customer_repo, 'no matter')

    # act
    result = await service.create_customer('some name', 'some address', 'some email', 'some phone')

    # assert
    mocked_CustomerDto.assert_called_once_with(id=None, name='some name', address='some address', email='some email', phone='some phone')
    mocked_customer_repo.add.assert_called_once_with(mocked_CustomerDto())
    assert result is mocked_CustomerDto()


@pytest.mark.asyncio
async def test_WarehouseService__create_order(mocker):
    # arrange
    mocked_order_repo = mocker.Mock()
    mocked_order_repo.add = AsyncMock()
    mocked_OrderDto = mocker.patch('warehouse.domain.services.OrderDto')
    service = WarehouseService('no matter', 'no matter', mocked_order_repo)

    # act
    result = await service.create_order('some products', 'some customer')

    # assert
    mocked_OrderDto.assert_called_once_with(id=None, products='some products', customer='some customer')
    mocked_order_repo.add.assert_called_once_with(mocked_OrderDto())
    assert result is mocked_OrderDto()
