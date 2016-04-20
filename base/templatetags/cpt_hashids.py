import cptids
from django import template
register = template.Library()

@register.filter
def cptids_encode(value, arg):
    return cptids.encode(arg, value)
