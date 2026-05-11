from django.contrib import admin
from .models import CachedPlayer, CachedTeam


@admin.register(CachedPlayer)
class CachedPlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'nba_id', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('full_name', 'first_name', 'last_name')


@admin.register(CachedTeam)
class CachedTeamAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'abbreviation', 'city', 'nba_id', 'updated_at')
    search_fields = ('full_name', 'city', 'abbreviation')
