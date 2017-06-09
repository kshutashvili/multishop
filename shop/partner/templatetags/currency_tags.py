# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from urlparse import urlparse

register = template.Library()


@register.filter
def format_currency(currency):
    currency_dict = {'UAH': 'грн',}
    return currency_dict[currency] or currency


@register.filter
def humanize_price(price):
    reversed_price = price[::-1]
    new_price = " ".join([reversed_price[i:i+3] for i in range(0, len(reversed_price), 3)])
    return new_price[::-1]
