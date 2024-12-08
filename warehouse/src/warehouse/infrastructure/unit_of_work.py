import logging
from warehouse.domain.unit_of_work import UnitOfWork

from tortoise.transactions import in_transaction


class Uow(UnitOfWork):

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)
    
    async def __enter__(self):
        self._logger.info('Enter transaction')
        async with in_transaction() as transaction:
            yield transaction

    async def __exit__(self):
        self._logger.info('Exit transaction')
