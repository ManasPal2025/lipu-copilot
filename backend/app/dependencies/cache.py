"""Cache dependencies exposed to FastAPI routes."""

from redis.asyncio import Redis

from app.db.redis import get_redis_client


async def get_cache() -> Redis:
    return await get_redis_client()

