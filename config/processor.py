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
    site_copyright = site_conf.copyright
    site_config, _ = Configuration.objects.get_or_create(site=site_obj)
    return {'site_email': site_email,
            'site_display_name': site_obj.name,
            'site_logo': site_conf.logo,
            'site_copyright': site_copyright,
            'site_id': site_obj.pk,
            'site_favicon': site_conf.favicon,
            'site_config': site_config,
            'google_webmaster_code': site_conf.code_webmaster_google,
            'yandex_webmaster_code': site_conf.code_webmaster_yandex,
            'google_tag_manager_script': site_conf.google_tag_manager_script,
            'google_tag_manager_noscript': site_conf.google_tag_manager_noscript}


def menu_processor(request):
    site_obj = get_current_site(request)
    menu_items = MenuItem.objects.active().filter(
                                                Q(site=None) | Q(site=site_obj))
    header_menu = menu_items.in_header()
    footer_objects = menu_items.in_footer().select_related('category')
    menu_by_cat = defaultdict(lambda: [])
    for item in footer_objects:
        menu_by_cat[item.category].append(item)
    footer_menu = sorted(menu_by_cat.items(), key=lambda item: -1 if item[0] is None else item[0].order)
    return {'header_menu': header_menu, 'footer_menu': footer_menu}


def show_undercat_block(request):
    site_obj = get_current_site(request)
    text_one = TextOne.objects.filter(
        (Q(site=None) | Q(site=site_obj) & Q(is_active=True))).first()
    text_two = TextTwo.objects.filter(
        (Q(site=None) | Q(site=site_obj) & Q(is_active=True))).first()
    text_three = TextThree.objects.filter(
        (Q(site=None) | Q(site=site_obj) & Q(is_active=True))).first()
    text_four = TextFour.objects.filter(
        (Q(site=None) | Q(site=site_obj) & Q(is_active=True))).first()
    conf_obj, _ = Configuration.objects.get_or_create(site=site_obj)
    return {'text_one': text_one if text_one else '',
            'text_two': text_two if text_two else '',
            'text_three': text_three if text_three else '',
            'text_four': text_four if text_four else '',
            'text_url': conf_obj.undercat_block_url}
