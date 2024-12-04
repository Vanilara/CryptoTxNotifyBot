import asyncio
import pytest
from src.db import Base, engine
from src.core.config import settings
from src.db.core.unit_of_work import UnitOfWork

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

# @pytest.fixture(scope="session", autouse=True)
# async def recreate_db(event_loop):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def unit_of_work(event_loop):
    return UnitOfWork()
