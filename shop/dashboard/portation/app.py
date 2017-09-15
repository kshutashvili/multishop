from django.conf.urls import url
from oscar.core.application import Application

from shop.dashboard.portation.views import ExportView
from shop.dashboard.portation.views import ImportView
from shop.dashboard.portation.views import AttrubitesListView


class PortationDashboardApplication(Application):
    name = None
    default_permissions = ['is_staff', ]

    import_view = ImportView
    export_view = ExportView
    attributes_view = AttrubitesListView

    def get_urls(self):
        urls = [
            url(r'^import/$', self.import_view.as_view(),
                name='portation-import'),
            url(r'^export/$', self.export_view.as_view(),
                name='portation-export'),
            url(r'^get-attributes/$', self.attributes_view.as_view(),
                name='portation-get-attributes'),
        ]
        return self.post_process_urls(urls)


application = PortationDashboardApplication()
