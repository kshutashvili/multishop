# -*- coding: utf-8 -*-
from collections import defaultdict
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q

from config.models import SiteConfig, MenuItem


def show_site_email(request):
    site_obj = get_current_site(request)
    site_conf = SiteConfig.objects.get(site=site_obj)
    site_email = site_conf.email
    return {'site_email': site_email}


def menu_processor(request):
    site_obj = get_current_site(request)
    menu_items = MenuItem.objects.active().filter(
                                                Q(site=None) | Q(site=site_obj))
    header_menu = menu_items.in_header()
    footer_objects = menu_items.in_footer().select_related('category')
    menu_by_cat = defaultdict(lambda: [])
    for item in footer_objects:
        menu_by_cat[item.category].append(item)
    footer_menu = sorted(menu_by_cat.items(), key=lambda item: item[0].order)
    return {'header_menu': header_menu, 'footer_menu': footer_menu}
