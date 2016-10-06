from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from lims_app.templatetags.gravatar import gravatarUrl

import account.models
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


def _baseCard(image, title, data):
    return """
    <div class="panel panel-default">
        <div class="panel-heading">{title}</div>
        <div class="panel-body">
            <div class="row">
                <div class="col-sm-3">
                    <img src="{image}" />
                </div>
                <div class="col-sm-9">
                    {data}
                </div>
            </div>
        </div>
    </div>
    """.format(image=image, title=title, data=data)

def org2url(org):
    return reverse('directory:org-detail', args=[org.id])

def person2url(person):
    return reverse('directory:person-detail', args=[person.id])

def hrefize(url, text):
    return '<a href="{url}">{text}</a>'.format(url=url, text=text)

@register.filter
def card(value):
    if isinstance(value, account.models.Account):
        orgs = ""
        if value.orgs.count() > 0:
            orgs = "Member of " + ', '.join(hrefize(org2url(x), x.name) for x in value.orgs.all())

        tags = ''.join([persontag(x) for x in value.tags.all()])

        return mark_safe(
            _baseCard(
                gravatarUrl(value.primaryEmail().email, size=200),
                value.name,
                orgs + "<hr />" + tags,
            ),
        )
    else:
        return None

@register.filter
def cptids_encode(value, arg):
    return cptids.encode(arg, value)

@register.filter
def persontag(value):
    tag_type = 'default'
    if value.name.startswith('BICH464'):
        tag_type = 'info'
    elif value.name == 'PI':
        tag_type = 'primary'
    elif value.name == 'Staff':
        tag_type = 'success'

    result = """
<a href="{url}" class="noUnderline">
    <span class="label label-{tag_type}">{tag.name}</span>
</a>
&nbsp;
    """.format(
        url=reverse('directory:tag-detail', args=[value.id]),
        tag_type=tag_type,
        tag=value
    )
    return mark_safe(result)
