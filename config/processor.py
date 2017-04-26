# -*- coding: utf-8 -*-
from django.contrib.sites.shortcuts import get_current_site

from config.models import SiteConfig


def show_site_email(request):
    site_obj = get_current_site(request)
    site_conf = SiteConfig.objects.get(site=site_obj)
    site_email = site_conf.email
    return {'site_email': site_email}
