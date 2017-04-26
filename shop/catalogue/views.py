# -*-coding:utf8-*-
import os
from collections import Iterable

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.views.decorators.http import require_POST
from django.views.generic.base import ContextMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from oscar.apps.catalogue.search_handlers import \
    get_product_search_handler_class
from oscar.apps.catalogue.views import \
    ProductDetailView as OscarProductDetailView, \
    CatalogueView as OscarCatalogueView, \
    ProductCategoryView as OscarProductCategoryView
from oscar.apps.customer import history

from shop.catalogue.models import Product, ProductClass, Category
from shop.catalogue.models import ProductAttributeValue
from shop.order.forms import OneClickOrderForm
from website.views import SiteTemplateResponseMixin


class CompareAndMenuContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(CompareAndMenuContextMixin, self).get_context_data()
        site = get_current_site(self.request)
        context['product_classes'] = ProductClass.objects.filter(site=site)
        context['categories'] = Category.objects.filter(site=site)
        compare_list = self.request.session.get('compare_list')
        if compare_list:
            compare_products = Product.objects.filter(
                id__in=compare_list)
            compare_categories = []
            for product in compare_products:
                cat = product.categories.all()
                if isinstance(cat, Iterable):
                    compare_categories.extend(cat)
                else:
                    compare_categories.append(cat)
            compare_categories = list(set(compare_categories))

            context['compare_categories'] = compare_categories
            context['compare_products'] = compare_products
        return context


class ProductDetailView(CompareAndMenuContextMixin, SiteTemplateResponseMixin,
                        OscarProductDetailView):
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

        return context

    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()
        recent_products = [p for p in history.get(self.request) if p != obj]
        obj.change_similar_products(recent_products)
        return super(ProductDetailView, self).render_to_response(context,
                                                                 **response_kwargs)


class CatalogueView(CompareAndMenuContextMixin, SiteTemplateResponseMixin,
                    OscarCatalogueView):
    template_name = 'browse.html'

    def get_context_data(self, **kwargs):
        context = super(CatalogueView, self).get_context_data()
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


class CompareView(CompareAndMenuContextMixin, SiteTemplateResponseMixin,
                  TemplateView):
    template_name = 'compare.html'

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=request.POST.get('id'))
        if product:  # we have to use list and do check, because set is not JSON serializable
            if hasattr(self.request.session,
                       'compare_list') and product in self.request.session.get(
                'compare_list'):
                return HttpResponse(status=409)
            self.request.session.setdefault('compare_list', []).append(
                product.id)
            request.session.modified = True  # to save changes
        return HttpResponse(status=201)


class CompareCategoryView(CompareAndMenuContextMixin, SiteTemplateResponseMixin,
                          TemplateView):
    template_name = 'compare_table.html'

    def get_context_data(self, **kwargs):
        context = super(CompareCategoryView, self).get_context_data()
        category = get_object_or_404(Category, pk=kwargs['category'])
        context['category'] = category
        products = Product.objects.filter(
            id__in=self.request.session['compare_list'], categories=category)
        context['products'] = products
        attrs = ProductAttributeValue.objects.filter(product__in=products)
        attr_vals = {}
        for val in attrs:
            temp = []
            for product in products:
                if val.attribute in product.attributes.all():
                    temp.append(product.attribute_values.get(
                        attribute_id=val.attribute.id).value_as_html)
                else:
                    temp.append('-')
            attr_vals[val.attribute.name] = temp[:]
            temp[:] = []

        context['attributes'] = attr_vals.items()
        context['unique_attributes'] = {cat: attrs for cat, attrs in
                                        attr_vals.items() if
                                        len(set(attrs)) > 1}.items()

        return context


class ProductCategoryView(SiteTemplateResponseMixin, CompareAndMenuContextMixin,
                          OscarProductCategoryView):
    template_name = 'category.html'


@require_POST
def remove_item_from_compare_list(request):
    request.session['compare_list'].remove(int(request.POST.get('id')))
    request.session.modified = True  # to save changes
    return HttpResponse(status=204)


@require_POST
def remove_category_from_compare_list(request):
    category = get_object_or_404(Category, pk=request.POST.get('pk'))
    request.session['compare_list'] = list(Product.objects.filter(
        id__in=request.session['compare_list']).exclude(
        categories=category).values_list('id', flat=True))
    request.session.modified = True  # to save changes
    return HttpResponse(status=204)


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
