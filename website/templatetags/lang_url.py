from django.core.urlresolvers import resolve, reverse
from django.template import Library
from django.utils.translation import activate, get_language
from shop.catalogue.utils import get_view_type
from shop.catalogue.models import Product, Category
from contacts.models import FlatPage


register = Library()


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    """
    Get active page's url by a specified language
    Usage: {% change_lang 'en' %}
    """

    path = context['request'].path
    url_parts = resolve(path)

    cur_language = get_language()

    try:

        if url_parts.url_name == "product_or_category" and cur_language != lang:
            # product_or_category special routing with localized slugs
            slugs = url_parts.kwargs['slug'].split(Category._slug_separator)
            last_slug = slugs[-1]
            view_type = get_view_type(last_slug)[0]
            attr = 'full_slug'

            # get slug based on view_type
            if view_type == "product":
                model = Product
            elif view_type == "flatpage":
                model = FlatPage
                attr = 'slug'
            elif view_type == "category":
                model = Category

            obj = model.objects.get(slug=last_slug)
            activate(lang)

            url_parts.kwargs['slug'] = getattr(obj, attr)
        else:
            activate(lang)

        # remove empty params
        url_parts.kwargs = {k: v for k, v in url_parts.kwargs.iteritems() if v is not None}

        url = reverse(url_parts.view_name, kwargs=url_parts.kwargs)
    finally:
        activate(cur_language)

    return "%s" % url
