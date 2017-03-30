from oscar.apps.catalogue.views import ProductDetailView as OscarProductDetailView
from oscar.apps.customer import history

from website.views import SiteTemplateResponseMixin


class ProductDetailView(SiteTemplateResponseMixin, OscarProductDetailView):
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        current_product = self.get_object()
        products = history.get(self.request)
        if current_product:
            products = [p for p in products if p != current_product]
        context['recently_viewed_products'] = products
        return context
