from django import template

register = template.Library()

@register.filter
def sum(value, args):
    result = round(value + args, 2)
    return result

@register.filter
def rest(value, args):
    result = round(value-args, 2)
    return result

@register.filter
def isinstance(value, args):
    result = isinstance(value, args)
    return result