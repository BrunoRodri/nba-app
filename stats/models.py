from django.db import models


class CachedPlayer(models.Model):
    """Cached NBA player info for fast local search."""
    nba_id = models.IntegerField(unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, db_index=True)
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Cached Player'
        verbose_name_plural = 'Cached Players'

    def __str__(self):
        return self.full_name

    @classmethod
    def search(cls, query):
        """Search players by name (case-insensitive partial match)."""
        return cls.objects.filter(full_name__icontains=query)

    @property
    def headshot_url(self):
        return f"https://cdn.nba.com/headshots/nba/latest/1040x760/{self.nba_id}.png"


class CachedTeam(models.Model):
    """Cached NBA team info for fast local search."""
    nba_id = models.IntegerField(unique=True, db_index=True)
    full_name = models.CharField(max_length=200, db_index=True)
    abbreviation = models.CharField(max_length=10)
    nickname = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    year_founded = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Cached Team'
        verbose_name_plural = 'Cached Teams'

    def __str__(self):
        return self.full_name

    @classmethod
    def search(cls, query):
        """Search teams by name, city, or abbreviation (case-insensitive)."""
        from django.db.models import Q
        return cls.objects.filter(
            Q(full_name__icontains=query) |
            Q(city__icontains=query) |
            Q(nickname__icontains=query) |
            Q(abbreviation__icontains=query)
        )

    @property
    def logo_url(self):
        return f"https://cdn.nba.com/logos/nba/{self.nba_id}/global/L/logo.svg"
