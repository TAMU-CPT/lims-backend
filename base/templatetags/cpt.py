from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

import hashlib
import cptids
register = template.Library()

@register.filter
@stringfilter
def barcode(value, type='code128'):
    return 'https://cpt.tamu.edu/barcodes/i/{type}/CPT_{data}.png'.format(
        data=value, type=type
)

@register.filter(needs_autoescape=True)
def ibarcode(url, value='20x200', autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    width, height = value.split('x')

    result = '<img src="https://cpt.tamu.edu/barcodes/i/{type}/CPT_{data}.png?w={w}&h={h}" width="{w}px" height="{h}px" />'.format(
        type='code128',
        data=esc(url),
        w=width,
        h=height,
    )
    return mark_safe(result)


@register.filter
def cptids_encode(value, arg):
    return cptids.encode(arg, value)
