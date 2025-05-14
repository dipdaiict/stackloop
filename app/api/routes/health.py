import logging
from sqlalchemy import text
from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import db
from app.db.redis import redis_client  

logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["Health"])


@router.get("/health")
async def health_check(session: AsyncSession = Depends(db.get_session)):
    db_status = "unknown"
    redis_status = "unknown"

    # PostgreSQL check
    try:
        result = await session.execute(text("SELECT 1;"))
        db_status = "ok" if result.scalar() == 1 else "fail"
    except SQLAlchemyError as e:
        logger.error(f"Database check failed: {e}")
        db_status = "fail"

    # Redis check
    try:
        client = await redis_client.get_client()
        key = "health_check_key"
        await client.set(key, "alive", ex=300)
        ttl = await client.ttl(key)
        redis_status = "ok" if ttl > 0 else "fail"
    except Exception as e:
        logger.error(f"Redis check failed: {e}")
        redis_status = "fail"

    return {
        "status": "ok",
        "db_status": db_status,
        "redis_status": redis_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
