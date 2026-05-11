"""
Management command to populate the local SQLite cache with
player and team data from nba_api static module.
"""
from django.core.management.base import BaseCommand
from stats.services import populate_player_cache, populate_team_cache


class Command(BaseCommand):
    help = 'Populate the local cache with NBA players and teams from nba_api'

    def handle(self, *args, **options):
        self.stdout.write('Populating player cache...')
        player_count = populate_player_cache()
        self.stdout.write(self.style.SUCCESS(f'  - {player_count} players cached'))

        self.stdout.write('Populating team cache...')
        team_count = populate_team_cache()
        self.stdout.write(self.style.SUCCESS(f'  - {team_count} teams cached'))

        self.stdout.write(self.style.SUCCESS('\nCache populated successfully!'))
