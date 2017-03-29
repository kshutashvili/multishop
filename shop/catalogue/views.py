from oscar.apps.catalogue.views import ProductDetailView as OscarProductDetailView
from website.views import SiteTemplateResponseMixin


class ProductDetailView(SiteTemplateResponseMixin, OscarProductDetailView):
    template_name = 'detail.html'
