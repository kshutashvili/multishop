import os

from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.functional import SimpleLazyObject

register = template.Library()


@register.simple_tag(takes_context=True)
def get_static(context, filename, *args, **kwargs):
    """
    template tag, that allows to get staticfiles depending on site
    The SimpleLazyObject wrapper makes sure the DB call only happens when
    the template actually uses the site object.
    This removes the query from the admin pages. It also caches the result
    """
    request = context['request']
    site = SimpleLazyObject(lambda: get_current_site(request))
    path = os.path.join(site.config.template, filename)
    return static(path)
