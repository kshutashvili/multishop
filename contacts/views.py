from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from website.views import SiteTemplateResponseMixin
from .models import ContactMessage, City
from .models import FlatPage


class ContactsView(SiteTemplateResponseMixin, TemplateView):
    template_name = 'contacts_main.html'

    def get(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        all_cities_by_site = City.objects.filter(site=current_site)
        context = self.get_context_data(**kwargs)
        context['cities'] = all_cities_by_site
        return self.render_to_response(context)


class ContactsByCity(SiteTemplateResponseMixin, TemplateView):
    template_name = 'contacts.html'

    def get(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        all_cities_by_site = City.objects.filter(site=current_site)
        current_city = request.GET.get('city', None)
        context = self.get_context_data(**kwargs)
        context['current_city'] = current_city
        context['cities'] = all_cities_by_site
        return self.render_to_response(context)


class ContactMessageCreateView(SiteTemplateResponseMixin, CreateView):
    model = ContactMessage
    fields = '__all__'
    success_url = '/'
    template_name = 'contacts.html'
    context_object_name = 'form'

    def form_valid(self, form):
        form.instance.site = get_current_site(self.request)
        return super(ContactMessageCreateView, self).form_valid(form)


class FlatPageView(SiteTemplateResponseMixin, DetailView):
    template_name = 'flatpages/default.html'
    context_object_name = 'flatpage'
    model = FlatPage
