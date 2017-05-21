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
        self.searchqueryset = self.searchqueryset.models(Product).filter(
            site=site.pk)
        return super(FacetedSearchView, self).__call__(request)

    def extra_context(self, **kwargs):
        context = super(FacetedSearchView, self).extra_context()
        site = get_current_site(self.request)
        context['side_menu'] = {
            cat: [descendant for descendant in cat.get_descendants()] for cat in
            Category.objects.filter(site=site) if cat.is_root()}

        cats = []
        for p in self.results.all():
            cats.extend(p.object.categories.all())

        leafs = [x for x in cats if x.is_leaf()]
        roots = [x if x.is_root() else x.get_root() for x in cats]

        categories_count = {
            root: [(leaf, self.results.filter(category=leaf.pk).count())
                   for
                   leaf in leafs if leaf.is_descendant_of(root)] for root in
        roots}

        context['categories_count'] = categories_count

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
