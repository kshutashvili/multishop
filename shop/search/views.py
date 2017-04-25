import os
from collections import Counter
from collections import Iterable

from django.contrib.sites.shortcuts import get_current_site
from oscar.apps.search.views import FacetedSearchView as OscarFacetedSearchView

from shop.catalogue.models import Product
from shop.catalogue.models import ProductClass, Category


class FacetedSearchView(OscarFacetedSearchView):
    template = 'search/results.html'

    def __call__(self, request):
        site = get_current_site(request)
        template = site.config.template
        self.template = os.path.join(template, FacetedSearchView.template)
        self.searchqueryset = self.searchqueryset.models(Product)
        return super(FacetedSearchView, self).__call__(request)

    def extra_context(self, **kwargs):
        context = super(FacetedSearchView, self).extra_context()
        site = get_current_site(self.request)
        product_classes = ProductClass.objects.filter(site=site)
        categories = Category.objects.filter(site=site)
        context['product_classes'] = product_classes
        context['categories'] = categories

        result = self.get_results().all()
        search_categories = []
        search_product_classes = []
        category_class = {}

        for res in result:
            search_categories.extend(res.object.categories.all())
            search_product_classes.append(res.object.product_class)
            category_class[res.object.product_class] = {cat for cat in
                                                        res.object.categories.all()}

        context['search_categories'] = Counter(search_categories)
        context['search_product_classes'] = Counter(
            search_product_classes).items()
        context['category_class'] = category_class.items()

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
