from django.conf.urls import url
from oscar.apps.dashboard.catalogue.app import (
    CatalogueApplication as CoreCatalogueApplication)

from oscar.core.loading import get_class


class CatalogueApplication(CoreCatalogueApplication):

    meta_tag_create_view = get_class('shop.dashboard.catalogue.views',
                                     'MetaTagCreateView')

    meta_tag_update_view = get_class('shop.dashboard.catalogue.views',
                                     'MetaTagUpdateView')

    def get_urls(self):
        processed_urls = super(CatalogueApplication, self).get_urls()
        urls = [
            url(
                r'^meta-tag/create/$',
                self.meta_tag_create_view.as_view(),
                name='meta-tag-create',
            ),
            url(
                r'^meta-tag/(?P<pk>\d+)/update/$',
                self.meta_tag_update_view.as_view(),
                name='meta-tag-update',
            ),
        ]
        return processed_urls + self.post_process_urls(urls)


application = CatalogueApplication()
