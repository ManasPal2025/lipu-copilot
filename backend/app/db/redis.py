"""Redis client lifecycle and health checks."""

from redis.asyncio import Redis

from app.core.config import get_settings


settings = get_settings()

redis_client: Redis = Redis.from_url(
    str(settings.redis_url),
    decode_responses=settings.redis_decode_responses,
    health_check_interval=settings.redis_health_check_interval,
)


async def get_redis_client() -> Redis:
    """Return the shared Redis client."""

    return redis_client


async def check_redis_connection() -> bool:
    """Return True when Redis responds to PING."""

    response = await redis_client.ping()
    return bool(response)


async def close_redis_connection() -> None:
    """Close Redis connections during application shutdown."""

    await redis_client.aclose()

