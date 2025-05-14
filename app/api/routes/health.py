import logging
from sqlalchemy import text
from fastapi import APIRouter, Depends
from datetime import datetime, timezone
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import db

logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["Health"])


@router.get("/health")
async def health_check(session: AsyncSession = Depends(db.get_session)):
    db_status = "unknown"
    try:
        result = await session.execute(text("SELECT 1;"))  # 👈 wrap query in text()
        db_status = "ok" if result.scalar() == 1 else "fail"
    except SQLAlchemyError as e:
        logger.error(f"Database check failed: {e}")
        db_status = "fail"

    return {
        "status": "ok",
        "db_status": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }