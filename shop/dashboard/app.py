from django.conf.urls import url
from oscar.apps.dashboard.app import (
    DashboardApplication as CoreDashboardApplication)

from shop.dashboard.portation.app import application as portation_app
from shop.dashboard.site.app import application as site_app
from oscar.core.loading import get_class
from shop.dashboard.reviews.app import application as reviews_app


class DashboardApplication(CoreDashboardApplication):
    portation_app = portation_app
    site_app = site_app
    reviews_app = reviews_app #get_class('dashboard.reviews.app', 'application')

    def get_urls(self):
        processed_urls = super(DashboardApplication, self).get_urls()
        urls = [
            url(r'^portation/', self.portation_app.urls),
            url(r'^site/', self.site_app.urls),
        ]
        return processed_urls + self.post_process_urls(urls)


application = DashboardApplication()
