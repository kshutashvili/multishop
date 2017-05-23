from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from website.views import SiteTemplateResponseMixin
from .models import ContactMessage


class ContactsView(SiteTemplateResponseMixin, TemplateView):
    template_name = 'contacts.html'


class ContactMessageCreateView(SiteTemplateResponseMixin, CreateView):
    model = ContactMessage
    fields = '__all__'
    success_url = '/'
    template_name = 'contacts.html'
    context_object_name = 'form'

    def form_valid(self, form):
        form.instance.site = get_current_site(self.request)
        return super(ContactMessageCreateView, self).form_valid(form)