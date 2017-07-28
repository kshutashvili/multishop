from django.shortcuts import reverse
from django.views.generic import CreateView
from django.utils.translation import ugettext_lazy as _

from shop.dashboard.site.forms import SiteForm, SiteConfigForm
from django.contrib.sites.models import Site


class SiteCreateView(CreateView):
    model = Site
    form_class = SiteForm
    template_name = 'shop/dashboard/site/site.html'

    def get_context_data(self, **kwargs):
        context = super(SiteCreateView, self).get_context_data(**kwargs)
        context['title'] = _('Create Site')
        if self.request.POST:
            context['site_config_form'] = SiteConfigForm(self.request.POST,
                                                         self.request.FILES)
        else:
            context['site_config_form'] = SiteConfigForm()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        site_config = context['site_config_form']
        self.object = form.save()
        site_config.instance = self.object.config

        if site_config.is_valid():
            site_config.save()

        return super(SiteCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard:index')
