from django import template
from urlparse import urlparse
from django.utils.translation import get_language
from contacts.models import FlatPage

register = template.Library()


@register.simple_tag
def url_format(url):
    uk_slug = None
    formatted_url = urlparse(url).path
    current_lang = get_language()

    if current_lang == "uk":
        translated_object = FlatPage.objects.prefetch_related('translations').filter(translations__slug=url)

        for obj in translated_object:
            uk_slug = obj.slug

        if uk_slug:
            return "/uk/%s/" % uk_slug

        return "/uk/%s/" % formatted_url

    return "/%s/" % formatted_url
