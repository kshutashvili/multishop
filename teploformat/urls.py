"""teploformat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_view
from django.contrib.staticfiles import views
from oscar.app import application

from shop.basket.views import delete_item_from_basket, update_items_quantity
from shop.catalogue.reviews.views import ProductQuestionView
from shop.catalogue.views import get_search_count, \
    OneClickOrderCreateView, CompareView, remove_item_from_compare_list, \
    remove_category_from_compare_list, CompareCategoryView
from shop.order.views import CallRequestCreateView
from website.sitemaps import base_sitemaps
from contacts.views import ContactsView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^basket/delete_item_from_basket/(?P<id>[0-9]+)/$',
        delete_item_from_basket,
        name='delete_item_from_basket'),

    # include a basic sitemap
    url(r'^sitemap\.xml$', sitemap_view.index,
        {'sitemaps': base_sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_view.sitemap,
        {'sitemaps': base_sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^contacts/$', ContactsView.as_view(), name='contacts')
]

urlpatterns += [
                   url(r'^static/(?P<path>.*)$', views.serve),
               ] + static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'', include(application.urls)),
    url(r'^catalugue/get_search_count/$', get_search_count,
        name='get_search_count'),
    url(
        r'^catalogue/(?P<product_slug>[\w-]*)_(?P<pk>\d+)/oneclick/$',
        OneClickOrderCreateView.as_view(), name='oneclick'),
    url(
        r'^catalogue/oneclick/$',
        OneClickOrderCreateView.as_view(), name='oneclick_basket'),

    url(r'^catalogue/compare/$', CompareView.as_view(),
        name='compare'),
    url(r'^catalogue/compare/(?P<category>\d+)$', CompareCategoryView.as_view(),
        name='compare_category'),
    url(r'^catalogue/compare/remove/$', remove_item_from_compare_list,
        name='remove_from_compare_list'),
    url(r'^catalogue/compare/remove_category/$',
        remove_category_from_compare_list,
        name='remove_category_from_compare_list'),
    url(
        r'^catalogue/(?P<product_slug>[\w-]*)_(?P<pk>\d+)/question/$',
        ProductQuestionView.as_view(), name='question'),
    url(r'^basket/update_items_quantity', update_items_quantity,
        name='update_items_quantity'),
    url(r'^basket/', include('shop.order.urls', namespace='order')),
    url('^call_request', CallRequestCreateView.as_view(), name='call_request'),
    prefix_default_language=False

)
