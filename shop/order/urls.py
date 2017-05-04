from django.conf.urls import url

from .views import SimpleOrderView

urlpatterns = [
    url(r'^create_order/$', SimpleOrderView.as_view(), name='create_order')
]
