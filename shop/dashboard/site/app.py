from django.conf.urls import url
from oscar.core.application import Application

from shop.dashboard.site.views import SiteCreateView


class SiteDashboardApplication(Application):
    name = None
    default_permissions = ['is_staff', ]

    site_create_view = SiteCreateView

    def get_urls(self):
        urls = [
            url(r'^add/$', self.site_create_view.as_view(),
                name='site-add'),
        ]
        return self.post_process_urls(urls)


application = SiteDashboardApplication()
