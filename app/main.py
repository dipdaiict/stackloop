import logging
from fastapi import FastAPI
from app.api.routes import health
from contextlib import asynccontextmanager

from app.db.postgres import db
from app.db.redis import redis_client  

logger = logging.getLogger(__name__)


# Startup & Shutdown Lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🔄 Starting up services...")

    # Connect to PostgreSQL
    await db.connect()
    logger.info("🗄️ PostgreSQL connection initialized.")

    # Connect to Redis
    await redis_client.connect()
    logger.info("📦 Redis connection initialized.")

    yield

    logger.info("🔻 Shutting down services...")

    # Disconnect PostgreSQL
    await db.disconnect()
    logger.info("🗄️ PostgreSQL connection closed.")


# Initialize FastAPI app
app = FastAPI(title="Stackloop API", lifespan=lifespan)

# Register all API routes
app.include_router(health.router)