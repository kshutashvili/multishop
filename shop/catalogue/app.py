from django.conf.urls import url

from oscar.apps.catalogue.app import (
    BaseCatalogueApplication as DefaultApp, ReviewsApplication
)

from shop.catalogue.views import product_or_category


class BaseCatalogueApplication(DefaultApp):
    def get_urls(self):
        urlpatterns = [
            url(r'^catalogue/$', self.catalogue_view.as_view(), name='index'),
            url(r'^(?P<slug>[\w-]+(/[\w-]+)*)/$', product_or_category,
                name='product_or_category'),
            url(r'^catalogue/ranges/(?P<slug>[\w-]+)/$',
                self.range_view.as_view(), name='range')
        ]
        return self.post_process_urls(urlpatterns)


class CatalogueApplication(BaseCatalogueApplication, ReviewsApplication):
    pass


application = CatalogueApplication()
