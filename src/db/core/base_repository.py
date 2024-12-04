from typing import Iterable, Any

from sqlalchemy import insert, delete, select, update, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from db.core.base_model import Base


class SQLAlchemyRepository[M: Base, S: BaseModel = Any]:
    model: type[M]
    schema: type[S] | None = None

    def __init__(self, 
            session: AsyncSession, 
        ) -> None:
        self.session = session

    async def select_all(self) -> list[S]:
        return await self._select_all()

    async def select_all_by(self, **filter_by) -> list[S]:
        return await self._select_all(filter_by=filter_by)
    
    async def select_all_in(self, key: str, value: list) -> list[S]:
        return await self._select_all(filter_by={key: value})

    async def select_one_or_raise(self, **filter_by) -> S:
        """Raise on multiple rows, raise on no rows"""
        res = await self._select_one(**filter_by)
        if res is None: 
            raise ValueError(f"No {self.model.__name__} found for filters {filter_by}")
        return res
    
    async def select_one_or_none(self, **filter_by) -> S | None:
        """Raise on multiple rows, None on no rows"""
        return await self._select_one(**filter_by)

    async def add_one(self, data: BaseModel):
        query = insert(self.model).values(data.model_dump()).returning(self.model)
        res = await self.session.execute(query)
        await self.session.commit()
        return res.scalar_one()
    
    async def update_one(self, id: int, schema: BaseModel):
        pk_name = inspect(self.model).primary_key[0].name
        stmt = (
            update(self.model)
            .where(getattr(self.model, pk_name) == id)
            .values({
                k: v for k, v in schema.model_dump(exclude_none=True).items()
            })
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def add_all(self, data: Iterable[BaseModel]) -> None:
        data_dicts = [item.model_dump() for item in data]
        query = insert(self.model)
        await self.session.execute(statement = query, params = data_dicts)
        await self.session.commit()

    async def delete_by(self, **filter_by) -> int:
        stmt = delete(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.rowcount
    
    async def _select_one(self, **filter_by) -> S | None:
        if self.schema is None:
            raise NotImplementedError(f'Not set pydantic schema for {self.model.__tablename__}')
        
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        results = res.scalars().all()
        if len(results) > 1:
            raise ValueError(f"Multiple {self.model.__name__} found for filters {filter_by}")
        if len(results) == 0:
            return None
        return self.schema.model_validate(results[0], from_attributes=True)

    async def _select_all(self, filter_by: dict | None = None) -> list[S]:
        if self.schema is None:
            raise NotImplementedError(f'Not set pydantic schema for {self.model.__tablename__}')
        
        stmt = select(self.model)
        if filter_by:
            stmt = stmt.filter_by(**filter_by)
        res = await self.session.execute(stmt)
        return [
            self.schema.model_validate(row, from_attributes=True)
            for row in res.scalars().all()
        ]
    
    async def _select_by_stmt(self, stmt) -> list[S]:
        if self.schema is None:
            raise NotImplementedError(f'Not set pydantic schema for {self.model.__tablename__}')
        
        res = await self.session.execute(stmt)
        
        return [
            self.schema.model_validate(row, from_attributes=True)
            for row in res.scalars().all()
        ]

    