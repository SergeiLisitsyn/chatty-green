from django import template
import re

register = template.Library()

@register.filter
def youtube_id(value):
    # твой уже готовый код для извлечения ID
    if not value:
        return ''
    pattern = r'(?:v=|be/|embed/)([0-9A-Za-z_-]{11})'
    match = re.search(pattern, value)
    if match:
        return match.group(1)
    return ''

@register.filter
def embed_youtube(value):
    """
    Возвращает HTML iframe с YouTube видео, подставляя ID из ссылки.
    """
    if not value:
        return ''
    video_id = youtube_id(value)
    if not video_id:
        return ''
    iframe_html = f'<iframe width="840" height="473" src="https://www.youtube.com/embed/{video_id}" ' \
                  f'frameborder="0" allowfullscreen></iframe>'
    return iframe_html

@register.filter
def is_youtube_url(value):
    if not value:
        return False
    return 'youtube.com' in value or 'youtu.be' in value


