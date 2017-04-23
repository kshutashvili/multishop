from oscar.apps.search.search_handlers import \
    SearchHandler as OscarSearchHandler


class SearchHandler(OscarSearchHandler):
    def __init__(self, request_data, full_path):
        if request_data.get('paginate_by'):
            self.paginate_by = request_data.get('paginate_by')
        super(SearchHandler, self).__init__(request_data, full_path)
