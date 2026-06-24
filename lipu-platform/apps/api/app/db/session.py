"""SQLAlchemy engine and session management."""

from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import Settings, get_settings


settings = get_settings()

engine: AsyncEngine = create_async_engine(
    str(settings.database_url),
    echo=settings.database_echo,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_timeout=settings.database_pool_timeout,
    pool_recycle=settings.database_pool_recycle,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a request-scoped database session."""

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_connection() -> bool:
    """Return True when PostgreSQL responds to a lightweight query."""

    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    return True


async def close_database_connections() -> None:
    """Dispose all SQLAlchemy pooled connections."""

    await engine.dispose()


def make_engine(database_url: str | None = None, config: Settings | None = None) -> AsyncEngine:
    """Create an async engine for tools or tests that need isolated engines."""

    selected_settings = config or settings
    return create_async_engine(
        database_url or str(selected_settings.database_url),
        echo=selected_settings.database_echo,
        pool_pre_ping=True,
    )

