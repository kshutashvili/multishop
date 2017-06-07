from django.contrib.sites.shortcuts import get_current_site
from oscar.apps.catalogue.search_handlers import \
    SolrProductSearchHandler as OscarSolrProductSearchHandler
from oscar.core.loading import get_model

from haystack.query import SQ


def get_product_search_handler_class():
    return SolrProductSearchHandler


class SolrProductSearchHandler(OscarSolrProductSearchHandler):
    def __init__(self, request_data, full_path, request=None, categories=None,
                 options=[]):
        self.options = options
        self.request = request
        if request_data.get('price_range_min') and request_data.get(
                'price_range_max'):
            self.price_range = {'min': request_data.get('price_range_min'),
                                'max': request_data.get('price_range_max')}
        else:
            self.price_range = None
        self.power = request_data.get('power')
        super(SolrProductSearchHandler, self).__init__(request_data, full_path,
                                                       categories)

    def get_search_queryset(self):
        site = get_current_site(self.request)
        sqs = super(OscarSolrProductSearchHandler,
                    self).get_search_queryset().filter(site=site.pk)
        if self.price_range:
            sqs = sqs.filter(
                price__range=[self.price_range['min'], self.price_range['max']])
        if self.options:
            group_attributes = []
            attributes = []
            for k in self.options:
                if k.startswith('filter_') and self.options[k]:
                    code = k.replace('filter_', '')
                    for item in self.options[k]:
                        values = item.split(',')
                        values = range(int(values[0]), int(values[1]) + 1)
                        attributes.append({
                            'attribute_codes': code,
                            'attribute_values__in': values,
                        })
                if k.startswith('group_filter_') and self.options[k]:
                    group_attributes += self.options[k]
            if attributes:
                sq_objetcs = SQ()
                i = 0
                for attribute in attributes:
                    if i == 0:
                        sq_objetcs = SQ(**attribute)
                    else:
                        sq_objetcs |= SQ(**attribute)
                    i += 1
                sqs = sqs.filter(sq_objetcs)
            if group_attributes:
                sqs = sqs.filter(attribute_option_values__in=group_attributes)
        if self.categories:
            # We use 'narrow' API to ensure Solr's 'fq' filtering is used as
            # opposed to filtering using 'q'.
            pattern = ' OR '.join([
                '"%s"' % c.pk for c in self.categories])
            sqs = sqs.narrow('category_exact:(%s)' % pattern)
        return sqs
