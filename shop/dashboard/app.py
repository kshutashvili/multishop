from django.conf.urls import url
from oscar.apps.dashboard.app import (
    DashboardApplication as CoreDashboardApplication)

from shop.dashboard.portation.app import application as portation_app


class DashboardApplication(CoreDashboardApplication):
    portation_app = portation_app

    def get_urls(self):
        processed_urls = super(DashboardApplication, self).get_urls()
        urls = [
            url(r'^portation/', self.portation_app.urls),
        ]
        return processed_urls + self.post_process_urls(urls)


application = DashboardApplication()
