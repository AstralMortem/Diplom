from backend.core.exceptions import MedServiceException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, DBAPIError
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from backend.config import config


engine = create_async_engine(str(config.DATABASE_URL), echo=config.DEBUG)
session_factory = async_sessionmaker(engine)


async def get_session():
    async with session_factory() as session:
        try:
            yield session
        except DBAPIError as e:
            await session.rollback()
            raise MedServiceException(status.HTTP_400_BAD_REQUEST, f"SQLAlchemy Error {e._code_str() if config.DEBUG else ''}", e._message().split('\n')[-1], debug=e)
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


class Model(DeclarativeBase):
    pass
