from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from oscar.apps.catalogue.views import ProductDetailView as OscarProductDetailView
from oscar.apps.customer import history

from shop.catalogue.models import Product, ProductClass, Category
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
        similar_products = current_product.get_similar_products()
        products_in_basket = [line.product for line in self.request.basket.lines.all()]
        context['already_in_basket'] = current_product in products_in_basket
        context['similar_products'] = similar_products
        site = get_current_site(self.request)
        context['product_classes'] = ProductClass.objects.filter(site=site)
        context['categories'] = Category.objects.filter(site=site)

        return context

    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        recent_products = [p for p in history.get(self.request) if p != obj]
        obj.change_similar_products(recent_products)
        return super(ProductDetailView, self).render_to_response(context, **response_kwargs)


@require_POST
def delete_item_from_basket(request, *args, **kwargs):
    try:
        request.basket.lines.get(product__id=kwargs['id']).delete()
    except ObjectDoesNotExist:
        pass
    return HttpResponse(status=204)
