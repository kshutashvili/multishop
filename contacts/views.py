from django.views.generic import TemplateView
from website.views import SiteTemplateResponseMixin

class ContactsView(SiteTemplateResponseMixin, TemplateView):
    template_name = 'contacts.html'
