"""Taskiq broker — shared across all task modules."""

from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from app.core.config import settings

# Create Taskiq broker with Redis
broker = ListQueueBroker(
    url=settings.TASKIQ_BROKER_URL,
).with_result_backend(
    RedisAsyncResultBackend(
        redis_url=settings.TASKIQ_RESULT_BACKEND,
    )
)
