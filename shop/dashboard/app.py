from django.conf.urls import url
from oscar.apps.dashboard.app import (
    DashboardApplication as CoreDashboardApplication)

from shop.dashboard.portation.app import application as portation_app
from shop.dashboard.site.app import application as site_app


class DashboardApplication(CoreDashboardApplication):
    portation_app = portation_app
    site_app = site_app

    def get_urls(self):
        processed_urls = super(DashboardApplication, self).get_urls()
        urls = [
            url(r'^portation/', self.portation_app.urls),
            url(r'^site/', self.site_app.urls),
        ]
        return processed_urls + self.post_process_urls(urls)


application = DashboardApplication()
