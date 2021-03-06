# -*- coding: utf-8 -*-
import pymorphy2
from django import template
from django.utils.translation import get_language
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.contenttypes.models import ContentType

from pymorphy2.tagset import OpencorporaTag
from oscar.apps.partner.strategy import Selector

from config.models import MetaTag
from config.models import ModelMetaTag
from shop.catalogue.models import Product
from shop.catalogue.models import Category

register = template.Library()


@register.simple_tag
def meta_tag(page_type, tag, object, request, category=None, filter=None):
    # Return ModelMetaTag if exists
    if isinstance(object, Product) or isinstance(object, Category):
        model_meta_tag = ModelMetaTag.objects.filter(
            content_type=ContentType.objects.get_for_model(object),
            object_id=object.id,
        )
        if model_meta_tag.exists():
            tag = getattr(model_meta_tag[0], tag)
            return tag

    # else return tag from tokens
    morph = pymorphy2.MorphAnalyzer(lang=get_language())
    meta_tags = MetaTag.objects.get(type=page_type)
    tag = getattr(meta_tags, tag)
    tokens = get_tokens(tag)
    for k in tokens:
        value = object
        for token in k:
            token_clean = token.replace('[', '').replace(']', '')
            if token_clean in OpencorporaTag.CASES:
                try:
                    word = morph.parse(unicode(value))[0]
                    value = word.inflect({token_clean}).word
                except AttributeError:
                    value = value
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
        tag = tag.replace(''.join(k), value)
    if tag[0:2] == ' .':
        tag = tag[2:]
    tag = tag.replace(' . ', '. ')
    return tag


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
