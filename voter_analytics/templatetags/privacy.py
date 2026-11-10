"""Template filters that mask voters' personal details on public pages.

Every record is a real voter, but names, street numbers, apartments and
exact birth dates are starred out so no one can be identified or located.
"""
from django import template

register = template.Library()


@register.filter
def mask_name(value):
    """'Jane' -> 'J***'. Names the dataset already starred out are kept as-is."""
    value = (value or "").strip()
    if not value or "*" in value:
        return value
    return value[0].upper() + "*" * max(len(value) - 1, 3)


@register.filter
def mask_street(voter):
    """Hide the house number and apartment, keep the street name."""
    return f"*** {voter.street_name}".strip()


@register.filter
def mask_dob(value):
    """Show only the birth year: '**/**/1985'."""
    return f"**/**/{value.year}" if value else ""
