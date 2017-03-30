from django.contrib.sites.shortcuts import get_current_site
from oscar.apps.promotions.views import HomeView as OscarHomeView

from shop.catalogue.models import Product, ProductClass, Category
from website.views import LandingView


class HomeView(LandingView, OscarHomeView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        site = get_current_site(self.request)
        context['our_products'] = Product.objects.filter(site=site)
        context['product_classes'] = ProductClass.objects.filter(site=site)
        context['categories'] = Category.objects.filter(site=site)
        return context
