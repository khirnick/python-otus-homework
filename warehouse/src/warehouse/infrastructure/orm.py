
from tortoise import Tortoise

DATABASE_URL = 'sqlite://warehouse.sqlite3'


async def init():
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': ['warehouse.infrastructure.models']}
    )
    await Tortoise.generate_schemas()
