import os

from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.list import MultipleObjectMixin

from shop.order.forms import InstallmentPaymentForm


class SiteTemplateResponseMixin(TemplateResponseMixin):
    def get_template_names(self):
        template = get_current_site(self.request).config.template
        return [os.path.join(template, x) for x in
                super(SiteTemplateResponseMixin, self).get_template_names()]


class LandingView(SiteTemplateResponseMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data()
        context['installment_form'] = InstallmentPaymentForm()
        return context


class SiteMultipleObjectMixin(MultipleObjectMixin):
    def get_queryset(self):
        return super(SiteMultipleObjectMixin, self).get_queryset().filter(
            site=get_current_site(self.request))
