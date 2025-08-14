from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from app.database import async_session_maker
from app.models.models_gdh import EqCompressorUnit
from app.repositories.base_repository import BaseRepository
from app.repositories.compressor.unit_repository import CompressorUnitRepository
from app.services.compressor_unit_service import CompressorUnitServise

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

def get_model_repo(model):
    async def _get_repo(session: AsyncSession = Depends(get_db_session)):
        return BaseRepository(session, model)
    return _get_repo

async def get_unit_repo(session: AsyncSession = Depends(get_db_session)):
    yield CompressorUnitRepository(session)

async def get_unit_service(session: AsyncSession = Depends(get_db_session)):
    yield CompressorUnitServise(session)