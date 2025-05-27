# posts/templatetags/time_filters.py

from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

def pluralize(value, one, few, many):
    value = abs(int(value))
    if value % 10 == 1 and value % 100 != 11:
        return one
    elif 2 <= value % 10 <= 4 and not (12 <= value % 100 <= 14):
        return few
    else:
        return many

@register.filter
def ru_timesince(value):
    if not value:
        return ''

    now = timezone.now()
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())

    diff = now - value

    if diff < timedelta(minutes=1):
        return 'только что'
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() // 60)
        return f'{minutes} {pluralize(minutes, "минуту", "минуты", "минут")} назад'
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() // 3600)
        return f'{hours} {pluralize(hours, "час", "часа", "часов")} назад'
    else:
        return value.strftime('%d.%m.%Y %H:%M')
