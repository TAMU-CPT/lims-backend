from django import template
from django.template.defaultfilters import stringfilter
import hashlib
register = template.Library()

def gravatarUrl(email, size=400):
    return 'https://s.gravatar.com/avatar/{hash}?s={size}'.format(
        hash=hashlib.md5(email).hexdigest(),
        size=size
    )

@register.filter
@stringfilter
def gravatar(value, size=400):
    return gravatarUrl(value, size=size)
