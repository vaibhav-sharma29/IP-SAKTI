"""
Database connection — AWS RDS PostgreSQL

Local dev:  postgresql://postgres:password@localhost:5432/ipsakti
AWS RDS:    postgresql://user:pass@<rds-endpoint>.amazonaws.com:5432/ipsakti

Set DATABASE_URL in .env — app connects automatically.
SQLAlchemy async engine so FastAPI stays non-blocking.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# asyncpg driver — async PostgreSQL
engine = create_async_engine(
    settings.database_url,
    echo=False,          # True for SQL debug logs
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Test connection before use (important for RDS)
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass


async def get_db():
    """FastAPI dependency — use in route with Depends(get_db)"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all tables on startup — called from main.py lifespan"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
