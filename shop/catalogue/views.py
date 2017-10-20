# -*- coding: utf-8 -*-
import os
from collections import Iterable, OrderedDict

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.checks import messages
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import InvalidPage, EmptyPage
from django.http import HttpResponse, Http404, JsonResponse
from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template, render_to_string
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
from oscar.apps.partner.strategy import Selector
from django.apps import apps

from contacts.views import FlatPageView
from shop.catalogue.models import Product, Category, FilterDescription
from shop.catalogue.models import ProductAttributeValue
from shop.order.forms import OneClickOrderForm
from website.views import SiteTemplateResponseMixin
from .forms import FilterForm, PaginateByForm
from .utils import get_view_type, dict_to_query, query_to_dict

MetaTag = apps.get_model('config', 'MetaTag')
SiteConfig = apps.get_model('config', 'SiteConfig')
MenuItem = apps.get_model('config', 'MenuItem')


class CompareAndMenuContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(CompareAndMenuContextMixin, self).get_context_data()
        site = get_current_site(self.request)

        context['side_menu'] = MenuItem.objects.filter(site=site).in_side().active()

        context['side_menu_categories'] = {
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

    def get_meta_tokens(self):
        tokens = {}
        tokens['page_type'] = MetaTag.PRODUCT
        tokens['product'] = self.object
        return tokens

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
        context.update(self.get_meta_tokens())
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

    def dispatch(self, request, *args, **kwargs):

        # disallow root URL /catalogue get
        if not (kwargs or request.GET):
            return redirect('404')

        return super(CatalogueView, self).dispatch(request, *args, **kwargs)

    def get_meta_tokens(self):
        tokens = {}
        site_config = SiteConfig.objects.get(site=self.site)
        brand_attribute = site_config.brand_attribute
        brand_attribute_code = brand_attribute.option_group.get_filter_param()
        if (brand_attribute_code in self.request.GET and
                len(self.request.GET.getlist(brand_attribute_code)) == 1 and
                len(self.request.GET) <= 4):
            tokens['page_type'] = MetaTag.BRAND
            tokens['page_object'] = brand_attribute.option_group.options.all() \
                .get(pk=self.request.GET.get(brand_attribute_code))
            tokens['category'] = self.category
        elif self.category and len(self.request.GET) == 0:
            tokens['page_type'] = MetaTag.CATEGORY
            tokens['page_object'] = self.category
        else:
            tokens['page_type'] = MetaTag.BRAND_FILTER
            tokens['page_object'] = None
            tokens['category'] = self.category
            tokens['filter'] = self.form.get_form_selected()
        return tokens

    def get(self, request, *args, **kwargs):

        self.site = get_current_site(request)
        try:
            slug = kwargs.get('category_slug') or kwargs['slug']
            self.category = Category.objects.get(slug=slug,
                                                 site=self.site)
        except (KeyError, Category.DoesNotExist):
            self.category = None
            categories = Category.objects.none()
        else:
            categories = (self.category,)

        if kwargs.get('query'):
            request.GET = query_to_dict(kwargs.get('query'), prepared=True)
            current_query = kwargs.get('query').split(':')
            if 'sort_by' in current_query:
                self.current_sort = current_query[current_query.index('sort_by')+1]

        self.current_path = self.request.path[0:self.request.path.find('sort_by')]

        self.basket_product_ids = []
        for line in request.basket.lines.all():
            self.basket_product_ids.append(line.product.id)

        page_num = kwargs.get('page')
        if page_num:
            request.GET._mutable = True
            request.GET['page'] = page_num

        try:
            self.form = FilterForm(
                self.site, data=request.GET, request=request, categories=categories)
        except EmptyPage:
            raise Http404

        self.paginate_form = PaginateByForm(data=request.GET)

        options = []
        if self.form.is_valid():
            options = self.form.cleaned_data
        path_to_request = request.get_full_path()

        new_path = path_to_request.split('/')
        if 'uk' in new_path:
            path_to_request = "/%s" % '/'.join(new_path[2:])
        else:
            path_to_request = '/'.join(new_path)
        try:
            self.filter_descr = FilterDescription.objects.get(filter_url=path_to_request)
        except FilterDescription.DoesNotExist:
            # page without applied filter
            pass
        try:
            self.search_handler = self.get_search_handler(
                self.request.GET, path_to_request, request,
                options=options, categories=categories)
        except InvalidPage:
            raise Http404

        if request.is_ajax():
            template_name = "defro/partials/products.html"
            context_data = self.get_context_data(**kwargs)
            content = render_to_string(template_name, context_data, request)

            return JsonResponse({"content": content,
                                 "has_more_pages": context_data['page_obj'].has_next()})

        else:
            return super(OscarCatalogueView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CatalogueView, self).get_context_data()
        context.update(self.get_meta_tokens())
        context['recently_viewed_products'] = history.get(self.request)
        context['filter_form'] = self.form
        context['paginate_form'] = self.paginate_form
        if hasattr(self, 'filter_descr'):
            context['filter_descr'] = self.filter_descr
        if hasattr(self, 'current_sort'):
            context['current_sort'] = self.current_sort
        if hasattr(self, 'current_path'):
            context['current_path'] = self.current_path
        if hasattr(self, 'basket_product_ids'):
            context['basket_product_ids'] = self.basket_product_ids
        context['filter_reset_url'] = self.request.path
        if hasattr(self, 'category'):
            context['category'] = self.category
            if self.category:
                context['filter_reset_url'] = self.category.get_absolute_url()
        price_range = [x.price for x in SearchQuerySet().models(Product).filter(
            site=self.site.pk) if x.price is not None]
        try:
            context['max_price'] = int(max(price_range))
            context['price_range_min'] = int(self.request.GET.get(
                'price_range_min'))
            context['price_range_max'] = int(self.request.GET.get(
                'price_range_max'))
        except (ValueError, TypeError):
            pass
        return context


class UpdateFilterCatalogueView(CatalogueView):
    template_name = 'defro/partials/filters.html'

    def get(self, request, *args, **kwargs):
        categroy_id = request.GET.get('category_id')
        if categroy_id:
            category = Category.objects.get(pk=categroy_id)
            kwargs['slug'] = category.slug
        else:
            category = None
        super(UpdateFilterCatalogueView, self).get(request, *args, **kwargs)
        context = self.get_context_data()
        context.update({'form': self.form, 'category': category})
        html = render_to_string(self.template_name, context)
        return JsonResponse({
            'result': html,
            'products_count': self.search_handler.get_search_queryset().count()
        })


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
        site_obj = get_current_site(self.request)
        instance.site = site_obj
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
        self.basket_product_ids = []
        for line in self.request.basket.lines.all():
            self.basket_product_ids.append(line.product.id)
        context = super(CompareCategoryView, self).get_context_data()
        context['basket_product_ids'] = self.basket_product_ids
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
        #attr_vals = {}
        attr_vals = OrderedDict()
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


class ProductCategoryView(CompareAndMenuContextMixin, SiteTemplateResponseMixin,
                          OscarProductCategoryView):
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryView, self).get_context_data()
        products_in_basket = [line.product for line in
                              self.request.basket.lines.all()]
        context['already_in_basket'] = products_in_basket
        depth = self.category.depth
        if depth == 1:
            context['page_type'] = MetaTag.SECTION
        elif depth == 2:
            context['page_type'] = MetaTag.SUB_SECTION
        return context

    def get(self, request, *args, **kwargs):
        # Fetch the category; return 404 or redirect as needed
        if request.GET:
            if kwargs.get('query'):
                d = query_to_dict(kwargs.get('query'), request.GET)
            else:
                d = request.GET.copy()
            redirect_kwargs = {'slug': kwargs['category_slug']}
            query = dict_to_query(d)
            if query:
                redirect_kwargs['query'] = query
            return redirect('catalogue:product_or_category',
                            permanent=True,
                            **redirect_kwargs)

        # redirect page 1 to root
        if int(kwargs.get('page') or 0) == 1:
            redirect_kwargs = {'slug': kwargs['category_slug']}
            if kwargs.get('query'):
                redirect_kwargs['query'] = kwargs['query']

            return redirect('catalogue:product_or_category',
                            permanent=True,
                            **redirect_kwargs)

        self.category = self.get_category()
        if not self.category.get_children().exists():
            # Crutch oriented programming: we show products on the category url
            # with a catalog view
            slug = kwargs.pop('category_slug')
            kwargs['slug'] = slug.split(Category._slug_separator)[-1]
            kwargs['page_type'] = MetaTag.CATEGORY
            return product_category_view(request, *args, **kwargs)

        potential_redirect = self.redirect_if_necessary(
            request.path, self.category)
        if potential_redirect is not None:
            return potential_redirect

        query = kwargs.get('query')
        if query:
            query = query_to_dict(query)
            query.update(request.GET)
        else:
            query = request.GET
        try:
            self.search_handler = self.get_search_handler(
                query, request.get_full_path(), request,
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

    view_type = get_view_type(last_slug)
    ctype = view_type[0]
    if ctype == 'product':
        kwargs['slug'] = kwargs['slug'].split(Category._slug_separator)[-1]
        kwargs['pk'] = view_type[1]
        return product_view(request, *args, **kwargs)
    elif ctype == 'flatpage':
        kwargs['slug'] = kwargs.pop('slug')
        kwargs['pk'] = view_type[1]
        return flatpage_view(request, *args, **kwargs)
    else:
        kwargs['pk'] = view_type[1]
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
