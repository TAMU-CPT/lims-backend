from django import template
from django.template.defaultfilters import stringfilter
import hashlib
import cptids
register = template.Library()

@register.filter
@stringfilter
def barcode(value, type='code128'):
    return 'https://cpt.tamu.edu/barcodes/i/{type}/CPT_{data}.png'.format(
        data=value, type=type
)

@register.filter
def cptids_encode(value, arg):
    return cptids.encode(arg, value)
