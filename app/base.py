from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models_gdh import *
from typing import Generic, TypeVar, List
from app.database import Base

class BaseMethods(Base):
    __abstract__ = True

    @classmethod
    async def create_data(cls, session: AsyncSession, **values):
        new_instance = cls(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance


    @classmethod
    async def get_read_data(cls, session: AsyncSession, id: int):
        await session.query(cls).get(id)
        

    async def update_data(self, session: AsyncSession, **values):
        for key, value in values.items():
            setattr(self, key, value)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        

    async def delete_data(self, session: AsyncSession, data_id: int):
        try:
            data = await session.get(self, data_id)
            if data:
                await session.delete(self)
                await session.flush()
        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            raise
