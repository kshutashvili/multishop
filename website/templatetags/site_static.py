import os

from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static

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
    site = request.site
    path = os.path.join(site.config.template, filename)
    return static(path)
