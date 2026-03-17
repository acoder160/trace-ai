from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
from sqlalchemy.pool import NullPool

# --- Initialize the async engine using the Supabase URL ---
# pool_pre_ping=True helps prevent connection drops with cloud databases
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool 
)

# Create a robust session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    """
    Dependency generator for FastAPI endpoints to get a DB session.
    Automatically handles opening and closing the connection.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()