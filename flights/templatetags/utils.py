from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()

@register.filter
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except:
        return 0


@register.filter
def replace(value, args):
    """
    جایگزینی متن
    استفاده: {{ "Turkish Airlines"|replace:" :-" }}
    خروجی: Turkish-Airlines
    """
    if not value:
        return ''
    old, new = args.split(':')
    return value.replace(old, new)
