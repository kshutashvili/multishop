from oscar.apps.catalogue.search_handlers import \
    SolrProductSearchHandler as OscarSolrProductSearchHandler


def get_product_search_handler_class():
    return SolrProductSearchHandler


class SolrProductSearchHandler(OscarSolrProductSearchHandler):
    def __init__(self, request_data, full_path, categories=None, options=[]):
        self.options = options
        super(SolrProductSearchHandler, self).__init__(request_data, full_path,
                                                       categories)

    def get_search_queryset(self):
        sqs = super(SolrProductSearchHandler, self).get_search_queryset()
        if self.options:
            for k in self.options:
                if k.startswith('filter_') and self.options[k]:
                    name = k.replace('filter_', '')
                    sqs = sqs.filter(attributes=name,
                                     attribute_values__in=
                                     self.options[k])

        return sqs
