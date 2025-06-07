from django import template

register = template.Library()

@register.filter
def split_pipe(value):
    """
    Split a string by pipe character '|'
    Usage: {{ value|split_pipe }}
    """
    if value:
        return value.split('|')
    return []