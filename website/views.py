import os

from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.base import TemplateResponseMixin, TemplateView


class SiteTemplateResponseMixin(TemplateResponseMixin):
    def get_template_names(self):
        template = get_current_site(self.request).site_config.get_template()
        return [os.path.join(template, x) for x in super(SiteTemplateResponseMixin, self).get_template_names()]


class LandingView(SiteTemplateResponseMixin, TemplateView):
    template_name = 'index.html'
