from django import template
from django.template.defaultfilters import stringfilter
import hashlib
register = template.Library()

@register.filter
@stringfilter
def gravatar(value, size=400):
    return 'https://s.gravatar.com/avatar/{hash}?s={size}'.format(
        hash=hashlib.md5(value).hexdigest(),
        size=size
    )
