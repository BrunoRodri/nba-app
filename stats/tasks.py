from celery import shared_task
from . import services
import logging

logger = logging.getLogger(__name__)

@shared_task(name="stats.tasks.update_player_cache_task")
def update_player_cache_task():
    """Task to periodically refresh the player cache from NBA API."""
    logger.info("Starting player cache update...")
    try:
        from .management.commands.populate_cache import Command
        cmd = Command()
        cmd.handle()
        logger.info("Player cache updated successfully!")
        return "Success"
    except Exception as e:
        logger.error(f"Failed to update player cache: {str(e)}")
        return f"Error: {str(e)}"

@shared_task(name="stats.tasks.debug_ping")
def debug_ping():
    """Simple ping task to verify Celery is working."""
    logger.info("Celery PING received!")
    return "PONG"
