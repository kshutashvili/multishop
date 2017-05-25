# -*- coding: utf-8 -*-
from collections import defaultdict
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q

from config.models import (SiteConfig, MenuItem, Configuration,
                           TextOne, TextTwo, TextThree, TextFour)


def show_site_email(request):
    site_obj = get_current_site(request)
    site_conf = SiteConfig.objects.get(site=site_obj)
    site_email = site_conf.email
    return {'site_email': site_email, 'site_display_name': site_obj.name}


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


def show_undercat_block(request):
    site_obj = get_current_site(request)
    text_one = TextOne.objects.filter(
        (Q(site=None) | Q(site=site_obj) & Q(is_active=True)))
    text_two = TextTwo.objects.filter(
        (Q(site=None) | Q(site=site_obj) & Q(is_active=True)))
    text_three = TextThree.objects.filter(
        (Q(site=None) | Q(site=site_obj) & Q(is_active=True)))
    text_four = TextFour.objects.filter(
        (Q(site=None) | Q(site=site_obj) & Q(is_active=True)))
    text_url = Configuration.get_solo().undercat_block_url
    return {'text_one': text_one, 'text_two': text_two,
            'text_three': text_three, 'text_four': text_four,
            'text_url': text_url}
