# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import get_language, activate
from oscar.core.loading import get_model

Product = get_model('catalogue', 'Product')
Category = get_model('catalogue', 'Category')
ProductClass = get_model('catalogue', 'ProductClass')
FlatPage = get_model('contacts', 'FlatPage')
ProductCategory = get_model('catalogue', 'ProductCategory')



class I18nSitemap(Sitemap):
    """
    A language-specific Sitemap class. Returns URLS for items for passed
    language.
    """

    def __init__(self, language):
        self.language = language
        self.original_language = get_language()

    def get_obj_location(self, obj):
        return obj.get_absolute_url()

    def location(self, obj):
        activate(self.language)
        location = self.get_obj_location(obj)
        activate(self.original_language)
        return location


class LandingSitemap(I18nSitemap):
    changefreq = 'always'
    priority = 1.0

    def items(self):
        return ['promotions:home', ]

    def get_obj_location(self, obj):
        return reverse(obj)


class ProductSitemap(I18nSitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Product.browsable.all()


class CategorySitemap(I18nSitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Category.objects.all()


class ProductClassSitemap(I18nSitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return ProductClass.objects.all()


class FlatPageSitemap(I18nSitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return FlatPage.objects.all()


class ContactsSitemap(I18nSitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['contacts',]

    def location(self, item):
        return reverse(item)


def html_sitemap(request):
    #flat_pages = FlatPage.objects.all()
    #products = Product.objects.all()
    #product_classes = ProductClass.objects.all()
    cat = request.GET.get('category_id', None)
    if cat:
        current_category = get_object_or_404(Category, pk=cat)
        current_category_children = current_category.get_children()
        if current_category_children:
            return render(request, "defro/html_sitemap.html", {
                'products': None,
                'current_category_children': current_category_children,
                'categories': None
        })
        products = ProductCategory.objects.filter(category__id=cat)
        return render(request, "defro/html_sitemap.html", {
            'products': products,
            'current_category_children': None,
            'categories': None
        })
    categories = Category.objects.all()
    return render(request, "defro/html_sitemap.html", {
            'products': None,
            'current_category_children': None,
            'categories': categories
        })


language_neutral_sitemaps = {
    'landing': LandingSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'product_classes': ProductClassSitemap,
    'static_pages': FlatPageSitemap,
    'contacts': ContactsSitemap
}

# Construct the sitemaps for every language
base_sitemaps = {}
for language, __ in settings.LANGUAGES:
    for name, sitemap_class in language_neutral_sitemaps.items():
        base_sitemaps['{0}-{1}'.format(name, language)] = sitemap_class(
            language)
