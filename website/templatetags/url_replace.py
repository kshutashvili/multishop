from django.template import Library
from django.core.urlresolvers import resolve, reverse

register = Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    path = context['request'].path
    url_parts = resolve(path)

    if int(kwargs.get('page') or 0) == 1:
        kwargs['page'] = None

    url_parts.kwargs.update(**kwargs)
    # remove empty params
    url_parts.kwargs = {k: v for k, v in url_parts.kwargs.iteritems() if v is not None}
    return reverse(url_parts.view_name, kwargs=url_parts.kwargs)
