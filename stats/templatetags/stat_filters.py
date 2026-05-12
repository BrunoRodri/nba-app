"""Custom template filters for NBA stat formatting."""
from django import template

register = template.Library()


@register.filter
def format_pct(value):
    """Format a decimal as a percentage (e.g., 0.485 → '48.5%')."""
    try:
        return f"{float(value) * 100:.1f}%"
    except (ValueError, TypeError):
        return value


@register.filter
def format_stat(value):
    """Round a float stat to 1 decimal place."""
    try:
        return f"{float(value):.1f}"
    except (ValueError, TypeError):
        return value


@register.filter
def season_display(value):
    """Make season string more readable (e.g., '2024-25' stays the same)."""
    if value:
        return str(value)
    return '—'


@register.filter
def get_item(dictionary, key):
    """Access a dictionary key in templates."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''


@register.filter
def fmt_int(value):
    """Format a value as integer (remove .0 decimals). Returns '0' for None/NaN."""
    try:
        if value is None:
            return "0"
        return str(int(float(value)))
    except (ValueError, TypeError):
        return value
