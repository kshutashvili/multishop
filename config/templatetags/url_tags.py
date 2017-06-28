from django import template
from urlparse import urlparse
from django.utils.translation import get_language
from django.conf import settings
from contacts.models import FlatPage


register = template.Library()


@register.simple_tag
def url_format(url):
    if url == '#':
        return url
    current_lang = get_language()
    default_lang = settings.LANGUAGE_CODE
    formatted_url = urlparse(url).path

    if current_lang != default_lang:
        # get localized slug for flat page
        try:
            kwargs = {'slug_%s' % default_lang: url}
            formatted_url = FlatPage.objects.get(**kwargs).slug
        except FlatPage.DoesNotExist:
            pass

        return "/%s/%s/" % (current_lang, formatted_url)

    return "/%s/" % formatted_url
