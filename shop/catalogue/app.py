from django.conf.urls import url
from django.views.generic import RedirectView

from oscar.apps.catalogue.app import (
    BaseCatalogueApplication as DefaultCatApp,
    ReviewsApplication as DefaultReviewsApp
)

from shop.catalogue.views import product_or_category


class BaseCatalogueApplication(DefaultCatApp):
    def get_urls(self):
        urlpatterns = [
            url(
                r'^catalogue/$',
                self.catalogue_view.as_view(),
                name='index'
            ),
            url(
                r'^category/(?P<category_slug>[\w-]+(/[\w-]+)*)_(?P<pk>\d+)/$',
                RedirectView.as_view(
                    permanent=True,
                    pattern_name='product_or_category'
                ),
                name='category'
            ),
            url(
                r'^catalogue/ranges/(?P<slug>[\w-]+)/$',
                self.range_view.as_view(),
                name='range'
            ),
            url(
                r'^(?P<slug>[\w-]+(/[\w-]+)*)(?:/(?P<query>(?:\w+:\S+)(?:-\w+:\S+)*))?/$',
                product_or_category,
                name='product_or_category'
            ),
        ]
        return self.post_process_urls(urlpatterns)


class ReviewsApplication(DefaultReviewsApp):
    def get_urls(self):
        urlpatterns = [
            url(r'^(?P<product_slug>[\w-]*)_(?P<product_pk>\d+)/reviews/',
                self.reviews_app.urls)
        ]
        urlpatterns += super(ReviewsApplication, self).get_urls()
        return self.post_process_urls(urlpatterns)


class CatalogueApplication(ReviewsApplication, BaseCatalogueApplication):
    name = 'catalogue'


application = CatalogueApplication()
