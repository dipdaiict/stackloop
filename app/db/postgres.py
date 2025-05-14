import logging
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession, 
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker
from app.core.config import postgres_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
Logger = logging.getLogger(__name__)

# Build the connection URL for async SQLAlchemy
DATABASE_URL = (
    f"postgresql+asyncpg://{postgres_settings.postgres_username}:"
    f"{postgres_settings.postgres_password}@"
    f"{postgres_settings.postgres_hostname}:"
    f"{postgres_settings.postgres_port}/"
    f"{postgres_settings.postgres_dbname}")

# Create the engine with pre_ping
engine: AsyncEngine = create_async_engine(
    DATABASE_URL, echo=False, future=True,
    pool_pre_ping=True)

# Async session factory
async_session_factory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession)


# Database utility class
# Database utility class
class Database:
    def __init__(self):
        self._engine = engine
        self._session_factory = async_session_factory

    async def connect(self):
        """Placeholder for future connection management."""
        Logger.info("✅ Async SQLAlchemy engine is ready.")

    async def disconnect(self):
        """Dispose of the SQLAlchemy engine."""
        await self._engine.dispose()
        Logger.info("🛑 SQLAlchemy engine disposed.")

    async def get_session(self) -> AsyncSession:
        """Dependency function to be used in routes or services."""
        async with self._session_factory() as session:
            yield session


# Create a singleton instance
db = Database()
# Logger.info("Async SQLAlchemy database initialized.")
