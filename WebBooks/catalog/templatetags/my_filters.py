from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(name="parce")
@stringfilter
def parce(path: str) -> str:
    return path.replace('?','&')


@register.filter(name="super_cut")
def super_cut(value: str, arg) -> str:
    return value.replace(str(arg), '')
