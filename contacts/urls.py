from django.conf.urls import url
from .views import ContactsView, ContactMessageCreateView, FlatPageView, ContactsByCity

urlpatterns = [
    url(r'^$', ContactsView.as_view(), name='contacts'),
    url(r'^detail/$', ContactsByCity.as_view(), name='contact_by_city'),
    url(r'^message/$', ContactMessageCreateView.as_view(),
        name='contact_message'),
]
