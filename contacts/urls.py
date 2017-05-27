from django.conf.urls import url
from .views import ContactsView, ContactMessageCreateView, FlatPageView

urlpatterns = [
    url(r'^$', ContactsView.as_view(), name='contacts'),
    url(r'^message/$', ContactMessageCreateView.as_view(),
        name='contact_message'),
]
