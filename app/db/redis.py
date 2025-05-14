import asyncio
import logging
from typing import Optional
import redis.asyncio as redis
from app.core.config import redis_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
Logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self._client: Optional[redis.Redis] = None

    async def connect(self) -> redis.Redis:
        if self._client:
            return self._client

        self._client = redis.Redis(
            host=redis_settings.redis_host,
            port=redis_settings.redis_port,
            password=redis_settings.redis_password,
            db=redis_settings.redis_db,
            decode_responses=True
        )

        retries = 3
        for attempt in range(1, retries + 1):
            try:
                await self._client.ping()
                Logger.info("✅ Redis client connected successfully.")
                return self._client
            except redis.ConnectionError:
                Logger.warning(f"""❌ Redis connection failed 
                            (attempt {attempt}/{retries})""")
                if attempt < retries:
                    await asyncio.sleep(2)
                else:
                    Logger.error("""🚨 Failed to connect to " \
                                Redis after all retries.""")
                    raise

    async def get_client(self) -> redis.Redis:
        if not self._client:
            await self.connect()
        return self._client


# Instantiate
redis_client = RedisClient()
# Logger.info("📦 Redis client instance created.")
