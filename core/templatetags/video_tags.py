from django import template
from django.forms.utils import flatatt

from django.utils.html import format_html_join, format_html

register = template.Library()


@register.simple_tag
def render_video(block):
    if not block:
        return ''
    sources = format_html_join('\n', '<source{0}>', [[flatatt(source)] for source in block['video'].sources])
    return format_html(
        f"""
            <video controls>
                {sources}
                Your browser does not support the video tag.
            </video>
        """
    )
