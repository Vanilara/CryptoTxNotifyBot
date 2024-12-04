from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import settings


engine = create_async_engine(settings.db.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)