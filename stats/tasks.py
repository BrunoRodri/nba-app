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

@shared_task(name="stats.tasks.warm_up_teams_cache_task")
def warm_up_teams_cache_task():
    """Background task to pre-fetch data for all teams into Redis."""
    from .models import CachedTeam
    from . import services
    
    teams = CachedTeam.objects.all()
    logger.info(f"Starting warm-up for {teams.count()} teams...")
    
    count = 0
    for team in teams:
        try:
            # These calls will trigger the cache.set in services.py
            services.get_team_info(team.nba_id)
            services.get_team_roster(team.nba_id)
            services.get_team_season_record(team.nba_id)
            count += 1
            if count % 5 == 0:
                logger.info(f"Warmed up {count} teams...")
        except Exception as e:
            logger.error(f"Failed to warm up team {team.full_name}: {e}")
            
    logger.info("Team cache warm-up completed!")
    return f"Warmed up {count} teams."
