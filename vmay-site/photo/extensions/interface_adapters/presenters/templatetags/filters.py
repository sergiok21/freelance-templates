from django import template
from django.utils.html import escape, mark_safe

register = template.Library()


@register.filter(name='to_p')
def to_p(value: str) -> str:
    """Розбиває текст на абзаци по порожньому рядку."""
    paragraphs = [
        f"<p>{escape(line.strip())}</p>"
        for line in value.splitlines()
        if line.strip()
    ]
    return mark_safe(''.join(paragraphs))
