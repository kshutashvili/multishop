from django import template
from urlparse import urlparse

register = template.Library()


@register.simple_tag
def url_format(url):
    formatted_url = urlparse(url).path
    return formatted_url
