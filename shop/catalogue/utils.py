from django.db import connection
from django.http import Http404
from django.utils.translation import get_language

from contacts.models import FlatPage
from shop.catalogue.models import Product, Category


def get_view_type(slug):
    """
    Based on url's slug value identifies which object to render a view for.
    Uses localized slug field value when querying database

    :param slug: url of object
    :return: (object_type, object_id) pair
    """
    query = [
        'SELECT "product" AS ctype, id FROM {ptable} WHERE slug_{lang_code}="{slug}"',
        'SELECT "category", id FROM {ctable} WHERE slug_{lang_code}="{slug}"',
        'SELECT "flatpage", id FROM {ftable} WHERE slug_{lang_code}="{slug}";'
    ]
    query = ' UNION '.join(query)
    query = query.format(ptable=Product._meta.db_table,
                         ctable=Category._meta.db_table,
                         ftable=FlatPage._meta.db_table,
                         slug=slug,
                         lang_code=get_language())

    with connection.cursor() as cur:
        cur.execute(query)
        view_type = cur.fetchone()

    if view_type is None:
        raise Http404

    return view_type
