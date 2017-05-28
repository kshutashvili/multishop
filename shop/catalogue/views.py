# -*- coding: utf-8 -*-
import os
from collections import Iterable

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.checks import messages
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import InvalidPage
from django.db import connection
from django.http import HttpResponse, Http404
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic.base import ContextMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from haystack.query import SearchQuerySet
from oscar.apps.catalogue.views import \
    ProductDetailView as OscarProductDetailView, \
    CatalogueView as OscarCatalogueView, \
    ProductCategoryView as OscarProductCategoryView
from oscar.apps.customer import history

from contacts.models import FlatPage
from contacts.views import FlatPageView
from shop.catalogue.models import Product, Category
from shop.catalogue.models import ProductAttributeValue
from shop.order.forms import OneClickOrderForm
from website.views import SiteTemplateResponseMixin
from .forms import FilterForm


class CompareAndMenuContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(CompareAndMenuContextMixin, self).get_context_data()
        site = get_current_site(self.request)
        context['side_menu'] = {
            cat: [descendant for descendant in cat.get_descendants()] for cat in
            Category.objects.filter(site=site) if cat.is_root()}
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

    def get(self, request, *args, **kwargs):
        self.site = get_current_site(request)
        self.form = FilterForm(self.site, request.GET)
        try:
            slug = kwargs.get('category_slug') or kwargs['slug']
            self.category = Category.objects.get(slug=slug)
        except (KeyError, Category.DoesNotExist):
            self.category = None
            categories = Category.objects.none()
        else:
            categories = (self.category,)
        options = []
        if self.form.is_valid():
            options = self.form.cleaned_data
        full_path = request.get_full_path()
        if int(request.GET.get('page', 0)) == 1:
            path_to_request = full_path.split('?')[0]
        else:
            path_to_request = full_path
        try:
            self.search_handler = self.get_search_handler(
                self.request.GET, path_to_request, request,
                options=options, categories=categories)
        except InvalidPage:
            raise Http404
        return super(OscarCatalogueView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CatalogueView, self).get_context_data()
        context['recently_viewed_products'] = history.get(self.request)
        context['filter_form'] = self.form
        if hasattr(self, 'category'):
            context['category'] = self.category
        price_range = [x.price for x in SearchQuerySet().models(Product).filter(
            site=self.site.pk) if x.price is not None]
        try:
            context['min_price'] = int(min(price_range))
            context['max_price'] = int(max(price_range))
        except ValueError:
            pass

        facet_data = context['facet_data']

        for i in facet_data.keys():
            facet_data[i]['results'] = [facet_dict for facet_dict in
                                        facet_data[i]['results'] if
                                        facet_dict['count'] != 0]

        context['facet_data'] = facet_data
        return context


class OneClickOrderCreateView(CreateView):
    form_class = OneClickOrderForm
    product_model = Product
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            self.product = get_object_or_404(
                self.product_model, pk=kwargs['pk'])
        self.basket = self.request.basket
        return super(OneClickOrderCreateView, self).dispatch(request, *args,
                                                             **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        if hasattr(self, 'product'):
            instance.product = self.product
            self.success_url = self.product.get_absolute_url()
        elif self.basket.num_lines:
            instance.basket = self.basket
            self.request.basket.submit()
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
        msg.send(fail_silently=True)
        return HttpResponse(self.success_url)

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
        try:
            products = self.request.session['compare_list']
        except KeyError:
            products = Product.objects.none()
        else:
            products = Product.objects.filter(id__in=products,
                                              categories=category)
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


product_category_view = CatalogueView.as_view()


class ProductCategoryView(SiteTemplateResponseMixin, CompareAndMenuContextMixin,
                          OscarProductCategoryView):
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryView, self).get_context_data()
        products_in_basket = [line.product for line in
                              self.request.basket.lines.all()]
        context['already_in_basket'] = products_in_basket
        return context

    def get(self, request, *args, **kwargs):
        # Fetch the category; return 404 or redirect as needed
        self.category = self.get_category()
        if not self.category.get_children().exists():
            # Crutch oriented programming: we show products on the category url
            # with a catalog view
            slug = kwargs.pop('category_slug')
            kwargs['slug'] = slug.split(Category._slug_separator)[-1]
            return product_category_view(request, *args, **kwargs)

        potential_redirect = self.redirect_if_necessary(
            request.path, self.category)
        if potential_redirect is not None:
            return potential_redirect

        try:
            self.search_handler = self.get_search_handler(
                request.GET, request.get_full_path(), request,
                self.get_categories(), [])
        except InvalidPage:
            messages.error(request, _('The given page number was invalid.'))
            return redirect(self.category.get_absolute_url())

        return super(OscarProductCategoryView, self).get(request, *args,
                                                         **kwargs)


category_view = ProductCategoryView.as_view()
product_view = ProductDetailView.as_view()
flatpage_view = FlatPageView.as_view()


def product_or_category(request, *args, **kwargs):
    slug = kwargs['slug']
    slugs = slug.split(Category._slug_separator)
    try:
        last_slug = slugs[-1]
    except IndexError:
        raise Http404
    query = [
        'SELECT "product" AS ctype FROM {ptable} WHERE slug="{slug}"',
        'SELECT "category" AS ctype FROM {ctable} WHERE slug="{slug}"',
        'SELECT "flatpage" AS ctype FROM {ftable} WHERE slug="{slug}";'
    ]
    query = ' UNION '.join(query)
    query = query.format(ptable=Product._meta.db_table,
                         ctable=Category._meta.db_table,
                         ftable=FlatPage._meta.db_table,
                         slug=last_slug)
    with connection.cursor() as cur:
        cur.execute(query)
        ctype = cur.fetchone()
    if ctype is None:
        raise Http404
    ctype = ctype[0]
    if ctype == 'product':
        kwargs['slug'] = kwargs['slug'].split(Category._slug_separator)[-1]
        return product_view(request, *args, **kwargs)
    elif ctype == 'flatpage':
        kwargs['slug'] = kwargs.pop('slug')
        return flatpage_view(request, *args, **kwargs)
    else:
        kwargs['category_slug'] = kwargs.pop('slug')
        return category_view(request, *args, **kwargs)


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
