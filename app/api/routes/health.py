from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="", tags=["Health"])


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()}