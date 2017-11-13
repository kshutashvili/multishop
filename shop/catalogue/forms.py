# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import math
from django import forms
from django.utils.translation import ugettext_lazy as _

from shop.catalogue.models import AttributeOptionGroup, ProductAttribute
from shop.catalogue.models import ProductClass
from shop.catalogue.widgets import CustomFilterCheckboxSelectMultiple
from shop.catalogue.fields import CustomFilterMultipleChoiceField
from shop.catalogue.fields import NonValidationMultipleChoiceField
from shop.catalogue.search_handlers import SolrProductSearchHandler


class FilterForm(forms.Form):
    attr_fields = {
        ProductAttribute.INTEGER: forms.IntegerField,
        ProductAttribute.FLOAT: forms.FloatField,
    }

    def __init__(self, site, categories, request, *args, **kwargs):
        self.site = site
        self.categories = categories
        self.categories_products = []
        for category in categories:
            self.categories_products.extend(category.product_set.all())

        self.request = request
        super(FilterForm, self).__init__(*args, **kwargs)
        self.make_filter()

    def make_filter(self):

        # Product class filter
        widget_choices = []
        p_clases = ProductClass.objects.filter(site=self.site)
        for p_class in p_clases:
            product_count = self.product_count_class(p_class)
            if product_count > 0:
                widget_choices.append((
                    '%s' % p_class.id,
                    '%s' % p_class.name,
                    {
                        'product_count': product_count,
                        'attrs': {},
                    }
                ))


        # Filter by attributes
        for attr in ProductAttribute.objects.filter(
                product_class__site=self.site,
                type__in=self.attr_fields,
                product_class__products__in=self.categories_products,
        ):
            code = 'filter_%s' % attr.code
            values = list(attr.productattributevalue_set
                .filter(product__in=self.categories_products)
                .values_list(
                'value_%s' % attr.type, flat=True))
            values.sort()

            widget_choices = []
            choices = []
            if values:
                first = values[0]
                number = int(math.ceil((values[-1] - values[0]) / 5.0))
                for i in range(5):
                    choices.append(
                        [first if i == 0 else first + 1, first + number])
                    first = first + number

                for i in choices:
                    product_count = self.product_count_attr(attr.code, i)
                    if product_count > 0:
                        widget_choices.append((
                            '%s-%s' % (i[0], i[1]),
                            '%s - %s' % (i[0], i[1]),
                            {
                                'product_count': product_count,
                                'attrs': {'data-min': i[0], 'data-max': i[1]},
                            }
                        ))

            if widget_choices:
                self.fields[code] = NonValidationMultipleChoiceField(
                    widget=CustomFilterCheckboxSelectMultiple(),
                    label=attr.name,
                    required=False,
                    choices=widget_choices,
                )

        # Filter by groups
        for group in AttributeOptionGroup.objects.filter(site=self.site):
            code = group.get_filter_param()

            widget_choices = []
            for i in group.options.all():
                product_count = self.product_count_group(code, i)
                if product_count > 0:
                    widget_choices.append((
                        i.id,
                        i.option,
                        {
                            'product_count': product_count,
                            'attrs': {},
                        }
                    ))

            if widget_choices:
                self.fields[code] = \
                    CustomFilterMultipleChoiceField(
                        widget=CustomFilterCheckboxSelectMultiple(),
                        label=group.name,
                        required=False,
                        choices=widget_choices,
                )

    def query(self, without=None):
        path_to_request = self.request.get_full_path()
        options = dict(self.data)
        if without and options.get(without):
            del options[without]
        handler = SolrProductSearchHandler(
            self.request.GET, path_to_request, self.request,
            options=options, categories=self.categories)
        return handler.get_search_queryset()

    def product_count_attr(self, code, option):
        sqs = self.query(without='filter_%s' % code)
        values = range(int(option[0]), int(option[1]) + 1)
        sqs = sqs.filter(
            attribute_codes=code,
            attribute_values__in=values,
        )
        return sqs.count()

    def product_count_group(self, code, option):
        sqs = self.query(without=code)
        sqs = sqs.filter(
            attribute_option_values__in=[option.id],
        )
        return sqs.count()

    def product_count_class(self, product_class_value):
        sqs = self.query(without='product_class')
        sqs = sqs.filter(
            product_class__in=[product_class_value.id],
        )
        return sqs.count()

    def get_form_selected(self):
        data = self.cleaned_data
        result = {}
        for data_item in data:
            field = self.fields[data_item]
            for selected in data[data_item]:
                for choice in field.choices:
                    if str(choice[0]) == str(selected):
                        if result.get(field.label) is None:
                            result[field.label] = []
                        result[field.label].append(choice[1])
        price_range_min = self.request.GET.get('price_range_min')
        price_range_max = self.request.GET.get('price_range_max')
        if price_range_min or price_range_max:
            result[_(u'Цена')] = ['{0} - {1}'.format(
                price_range_min, price_range_max)]
        return result


class PaginateByForm(forms.Form):

    PAGINATE_BY_CHOICES = [
        (12, "12"),
        (8, "8"),
        (6, "6"),
        (24, "24"),
    ]

    paginate_by = forms.ChoiceField(
        label="Paginate by", choices=PAGINATE_BY_CHOICES,
        widget=forms.Select(), required=False)
