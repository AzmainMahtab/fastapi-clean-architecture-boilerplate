from collections.abc import AsyncGenerator

from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.settings import settings

engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=settings.DEBUG)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


# This is what injects into our FastAPI routes: `db: Session = Depends(get_db)`
async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    This class is used to define the declarative base for the ORM models
    in the application.
    It provides a common base for all models to inherit from,
    allowing them to be recognized by SQLAlchemy's ORM system.
    """

    pass


class BaseModelMixin:
    """
    Base mixin class for all SQLAlchemy models.
    This class provides common fields and functionality for all models
    that inherit from it, such as id, created_at, and updated_at and deleted_at fields.
    """

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    deleted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
