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
from django.contrib.staticfiles import views
from django.shortcuts import redirect
from oscar.app import application
from shop.catalogue.views import delete_item_from_basket, get_search_count

urlpatterns = [
    url(r'^$', lambda r: redirect('/{}/'.format(r.LANGUAGE_CODE)), name="home"),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('website.urls')),
]

urlpatterns += [
                   url(r'^static/(?P<path>.*)$', views.serve),
               ] + static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'', include(application.urls)),
    url(r'^delete_item_from_basket/(?P<id>[0-9]+)/$', delete_item_from_basket,
        name='delete_item_from_basket'),
    url(r'^catalugue/get_search_count/$', get_search_count,
        name='get_search_count'),
)
