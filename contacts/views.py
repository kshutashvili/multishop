from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.base import ContextMixin

from website.views import SiteTemplateResponseMixin
from shop.catalogue.models import Product, Category
from .models import ContactMessage, City
from .models import FlatPage


class CompareAndMenuContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(CompareAndMenuContextMixin, self).get_context_data()
        site = get_current_site(self.request)
        context['side_menu'] = {
            cat: [descendant for descendant in cat.get_descendants()] for cat in
            Category.objects.filter(site=site) if cat.is_root()}
        compare_list = self.request.session.get('compare_list')
        if compare_list:
            compare_products = Product.objects.filter(
                id__in=compare_list)
            compare_categories = []
            for product in compare_products:
                cat = product.categories.all()
                if isinstance(cat, Iterable):
                    compare_categories.extend(cat)
                else:
                    compare_categories.append(cat)
            compare_categories = list(set(compare_categories))

            context['compare_categories'] = compare_categories
            context['compare_products'] = compare_products
        return context


class ContactsView(CompareAndMenuContextMixin, SiteTemplateResponseMixin, TemplateView):
    template_name = 'contacts_main.html'

    def get(self, request, *args, **kwargs):
        current_site = get_current_site(request)
        all_cities_by_site = City.objects.filter(site=current_site)
        context = self.get_context_data(**kwargs)
        context['cities'] = all_cities_by_site
        return self.render_to_response(context)


class ContactsByCity(CompareAndMenuContextMixin, SiteTemplateResponseMixin, TemplateView):
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


class FlatPageView(CompareAndMenuContextMixin, SiteTemplateResponseMixin, DetailView):
    template_name = 'flatpages/default.html'
    context_object_name = 'flatpage'
    model = FlatPage
