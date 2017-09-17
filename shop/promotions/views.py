from django.contrib.sites.shortcuts import get_current_site
from django.apps import apps
from oscar.apps.promotions.views import HomeView as OscarHomeView

from shop.catalogue.models import Product
from shop.catalogue.views import CompareAndMenuContextMixin
# from config.models import SiteConfig
from website.views import LandingView


SiteConfig = apps.get_model('config', 'SiteConfig')


class HomeView(LandingView, CompareAndMenuContextMixin, OscarHomeView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data()
        site = get_current_site(self.request)
        context['our_products'] = Product.objects.filter(site=site)
        context['power_attribute'] = SiteConfig.objects.get(site=site) \
            .power_attribute
        return context
