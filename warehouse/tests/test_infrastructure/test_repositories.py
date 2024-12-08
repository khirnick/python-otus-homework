from unittest.mock import AsyncMock
import pytest

from warehouse.infrastructure.repositories import TortoiseProductRepository


@pytest.mark.asyncio
async def test_TortoiseProductRepository__add(mocker):
    # arrange
    mocked_Product = mocker.patch('warehouse.infrastructure.repositories.Product')
    mocked_Product.return_value.save = AsyncMock()
    repo = TortoiseProductRepository()

    # act
    mocker_product_dto = mocker.Mock()
    await repo.add(mocker_product_dto)

    # assert
    mocked_Product.assert_called_once_with(name=mocker_product_dto.name, price=mocker_product_dto.price)
    mocked_Product().save.assert_called_once()


@pytest.mark.asyncio
async def test_TortoiseProductRepository__get(mocker):
    # arrange
    mocked_Product = mocker.patch('warehouse.infrastructure.repositories.Product')
    mocked_p = mocker.Mock()
    mocked_p.as_dto = AsyncMock(return_value='dto')
    mocked_Product.get_or_none = AsyncMock(return_value=mocked_p)
    repo = TortoiseProductRepository()

    # act
    result = await repo.get('some id')

    # assert
    mocked_Product.get_or_none.assert_called_once_with(id='some id')
    assert result == 'dto'


@pytest.mark.asyncio
async def test_TortoiseProductRepository__list(mocker):
    # arrange
    mocked_Product = mocker.patch('warehouse.infrastructure.repositories.Product')
    product1 = mocker.Mock()
    product1.as_dto = AsyncMock(return_value='dto1')
    product2 = mocker.Mock()
    product2 = mocker.Mock()
    product2.as_dto = AsyncMock(return_value='dto2')
    mocked_Product.all = AsyncMock(return_value=[product1, product2])
    repo = TortoiseProductRepository()

    # act
    result = await repo.list()

    # assert
    mocked_Product.all.assert_called_once()
    assert result == ['dto1', 'dto2']
