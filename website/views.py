from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.base import TemplateResponseMixin


class SiteTemplateResponseMixin(TemplateResponseMixin):
    def get_template_names(self):
        template = get_current_site(self.request).get_template()
        return [template + '/' + x for x in super(SiteTemplateResponseMixin, self).get_template_names()]
