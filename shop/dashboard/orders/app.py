from oscar.apps.dashboard.orders.app import OrdersDashboardApplication as OscarOrdersDashboardApplication
from oscar.core.loading import get_class
from django.conf.urls import url


class OrdersDashboardApplication(OscarOrdersDashboardApplication):

    oneclickorder_list_view = get_class('shop.dashboard.orders.views', 'OneClickOrderListView')
    oneclickorder_update_view = get_class('shop.dashboard.orders.views', 'OneClickOrderUpdateView')
    oneclickorder_delete_view = get_class('shop.dashboard.orders.views', 'OneClickOrderDeleteView')
    callrequest_list_view = get_class('shop.dashboard.orders.views', 'CallRequestListView')
    callrequest_delete_view = get_class('shop.dashboard.orders.views', 'CallRequestDeleteView')

    def get_urls(self):
        urls = [
            url(r'^oneclickorder/$', self.oneclickorder_list_view.as_view(), name='oneclickorder-list'),
            url(r'^oneclickorder/edit/(?P<pk>[\d]+)/$', self.oneclickorder_update_view.as_view(),
                name='oneclickorder-detail'),
            url(r'^oneclickorder/delete/(?P<pk>[\d]+)/$', self.oneclickorder_delete_view.as_view(),
                name='oneclickorder-delete'),
            url(r'^callrequest/$', self.callrequest_list_view.as_view(), name='callrequest-list'),
            url(r'^callrequest/delete/(?P<pk>[\d]+)/$', self.callrequest_delete_view.as_view(),
                name='callrequest-delete'),
        ]

        urls = self.post_process_urls(urls)

        urls += super(OrdersDashboardApplication, self).get_urls()

        return urls

application = OrdersDashboardApplication()
