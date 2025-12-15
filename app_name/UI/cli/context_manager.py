from contextlib import asynccontextmanager
from app_name.infrastructure.repositories.base_repository import BaseRepository
from app_name.infrastructure.repositories.compressor.database import async_session_maker
from app_name.UI.cli.cli_servise import CLIService

@asynccontextmanager
async def cli_service_context():
    """Контекстный менеджер для работы с CLIService"""

    session = async_session_maker()
    service = CLIService(session)

    try:
        yield service
        await session.commit()
    except Exception:
        await session.rollback()
        raise    
    finally:
        await session.close()

