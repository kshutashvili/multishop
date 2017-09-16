from django import template
from urlparse import urlparse
from django.utils.translation import get_language
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from contacts.models import FlatPage


register = template.Library()


@register.simple_tag(takes_context=True)
def url_format(context, url):
    if url == '#':
        return url
    current_lang = get_language()
    default_lang = settings.LANGUAGE_CODE
    formatted_url = urlparse(url).path

    if current_lang != default_lang:
        # get localized slug for flat page
        site = get_current_site(context['request'])
        try:
            kwargs = {'slug_%s' % default_lang: url,
                      'site': site}
            formatted_url = FlatPage.objects.filter(**kwargs).first().slug
        except AttributeError:
            pass

        return "/%s/%s/" % (current_lang, formatted_url)

    return "/%s/" % formatted_url


@register.filter
def phone_number_filter(phone):
    phone_with_minus = "-".join([phone[0:3], phone[4:6], phone[6:8]])
    return phone_with_minus
