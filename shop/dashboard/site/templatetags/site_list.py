from __future__ import unicode_literals

from django import template
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def site_list(context):

    sites = Site.objects.all()
    output = []
    selected = False

    for site in sites:

        if not selected and Site.objects.get_current(context['request']) == site:
            s = '<option value="{site_url}" selected="selected">' \
                '{site_url}</option>'.format(site_url=site.domain)
            selected = True
        else:
            s = '<option value="{site_url}">' \
                '{site_url}</option>'.format(site_url=site.domain)

        output.append(s)

    return mark_safe('\n'.join(output))
