# -*-coding:utf8-*-
import os

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from oscar.apps.catalogue.search_handlers import \
    get_product_search_handler_class
from oscar.apps.catalogue.views import \
    ProductDetailView as OscarProductDetailView, \
    CatalogueView as OscarCatalogueView
from oscar.apps.customer import history

from shop.catalogue.models import Product, ProductClass, Category
from shop.order.forms import OneClickOrderForm
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
        products_in_basket = [line.product for line in
                              self.request.basket.lines.all()]
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
        return super(ProductDetailView, self).render_to_response(context,
                                                                 **response_kwargs)


class CatalogueView(SiteTemplateResponseMixin, OscarCatalogueView):
    template_name = 'browse.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogueView, self).get_context_data()
        site = get_current_site(self.request)
        context['our_products'] = Product.objects.filter(site=site)
        context['product_classes'] = ProductClass.objects.filter(site=site)
        context['categories'] = Category.objects.filter(site=site)
        context['recently_viewed_products'] = history.get(self.request)

        return context


class OneClickOrderCreateView(CreateView):
    form_class = OneClickOrderForm
    product_model = Product

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(
            self.product_model, pk=kwargs['pk'])
        return super(OneClickOrderCreateView, self).dispatch(request, *args,
                                                             **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.product = self.product
        instance.save()

        template = os.path.join(get_current_site(self.request).config.template,
                                'email/oneclick_order.html')
        message = get_template(template).render(
            {'instance': instance})
        subject = u'Заявка на заказ(в один клик) №%s' % instance.id
        msg = EmailMultiAlternatives(subject, message,
                                     settings.DEFAULT_FROM_EMAIL,
                                     [settings.DEFAULT_FROM_EMAIL, ])
        msg.attach_alternative(message, "text/html")
        msg.send()
        return HttpResponse(self.product.get_absolute_url())

    def form_invalid(self, form):
        return HttpResponseBadRequest(form.errors.as_json())


def get_search_count(request):
    """
    usage example:
    $.get('/catalugue/get_search_count', 
    {'selected_facets': 'rating_exact:3'}, 
    function(data){//do something with data//});
    """
    search_hendler = get_product_search_handler_class()(request.POST,
                                                        request.get_full_path)
    return JsonResponse({'count': search_hendler.results.count()})


@require_POST
def delete_item_from_basket(request, *args, **kwargs):
    try:
        request.basket.lines.get(product__id=kwargs['id']).delete()
    except ObjectDoesNotExist:
        pass
    return HttpResponse(status=204)
