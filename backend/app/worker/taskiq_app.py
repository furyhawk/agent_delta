"""Taskiq application configuration."""

from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from app.worker.broker import broker
import app.worker.tasks  # noqa: F401 — register @broker.task decorated functions
import app.worker.tasks.schedules  # noqa: F401 — register scheduled tasks

# Create scheduler for periodic tasks
# LabelScheduleSource auto-discovers @broker.task(schedule=[...]) decorated functions
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


# Startup/shutdown hooks
@broker.on_event("startup")
async def startup() -> None:
    """Initialize broker on startup."""
    pass


@broker.on_event("shutdown")
async def shutdown() -> None:
    """Cleanup on shutdown."""
    pass
