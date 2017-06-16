# -*- coding: utf-8 -*-
import pymorphy2
from django import template
from django.utils.translation import get_language
from django.contrib.sites.shortcuts import get_current_site

from pymorphy2.tagset import OpencorporaTag
from oscar.apps.partner.strategy import Selector

from config.models import MetaTag

register = template.Library()


@register.inclusion_tag('defro/meta_tags.html')
def meta_tag(page_type, object, request, category=None, filter=None):
    morph = pymorphy2.MorphAnalyzer(lang=get_language())
    meta_tags = MetaTag.objects.get(type=page_type)
    tags = {
        'title': meta_tags.title,
        'title_meta': meta_tags.title_meta,
        'description_meta': meta_tags.description_meta,
        'h1': meta_tags.h1,
    }
    for i in tags:
        tokens = get_tokens(tags[i])
        for k in tokens:
            value = object
            for token in k:
                token_clean = token.replace('[', '').replace(']', '')
                if token_clean in OpencorporaTag.CASES:
                    try:
                        word = morph.parse(unicode(value))[0]
                        value = word.inflect({token_clean}).word
                    except AttributeError:
                        value = ''
                elif token_clean == 'filter':
                    value = ''
                    for item in filter:
                        filter_values = ', '.join([m for m in filter[item]])
                        value += u' {}: {};'.format(item, filter_values)
                elif token_clean == 'category' and category is not None:
                    value = category.name
                elif token_clean == 'site_name':
                    current_site = get_current_site(request)
                    value = current_site.name
                elif token_clean == 'site_domain':
                    current_site = get_current_site(request)
                    value = current_site.domain
                elif (page_type == MetaTag.PRODUCT and
                        (token_clean == 'price' or
                            token_clean == 'availability')):
                    selector = Selector()
                    strategy = selector.strategy()
                    purchase_info = strategy.fetch_for_product(object)
                    if token_clean == 'price':
                        value = unicode(purchase_info.price.incl_tax)
                    elif token_clean == 'availability':
                        value = unicode(purchase_info.availability.message)
                else:
                    if (token_clean == 'name' and
                        (page_type == MetaTag.BRAND or
                            page_type == MetaTag.BRAND_FILTER)):
                        token_clean = 'option'
                    try:
                        value = getattr(value, token_clean)
                    except AttributeError:
                        value = ''
            tags[i] = tags[i].replace(''.join(k), value)
    return tags


def get_tokens(text):
    tokens = [[]]
    current = ''
    position = 0
    take = False
    for i in text:
        if i == '[':
            current += i
            take = True
        elif i == ']':
            tokens[-1].append(current + i)
            take = False
            current = ''
            try:
                if not text[position + 1] == '[':
                    tokens.append([])
            except IndexError:
                pass
        elif take is True:
            current += i
        position += 1
    if tokens[-1] == []:
        del tokens[-1]
    return tokens
