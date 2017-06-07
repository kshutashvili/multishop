from __future__ import unicode_literals

import math
from django import forms

from shop.catalogue.models import (AttributeOptionGroup, Product,
                                   ProductAttribute)
from shop.catalogue.widgets import CustomFilterCheckboxSelectMultiple
from shop.catalogue.fields import CustomFilterMultipleChoiceField
from shop.catalogue.fields import NonValidationMultipleChoiceField


class FilterForm(forms.Form):
    attr_fields = {
        ProductAttribute.INTEGER: forms.IntegerField,
        ProductAttribute.FLOAT: forms.FloatField,
    }

    def __init__(self, site, categories, *args, **kwargs):
        self.site = site
        self.categories = categories
        super(FilterForm, self).__init__(*args, **kwargs)

        self.make_filter()

    def make_filter(self):
        for attr in ProductAttribute.objects.filter(
                product_class__site=self.site, type__in=self.attr_fields):
            code = 'filter_%s' % attr.code
            values = list(attr.productattributevalue_set.values_list(
                'value_%s' % attr.type, flat=True))
            values.sort()
            first = values[0]
            number = int(math.ceil((values[-1] - values[0]) / 5.0))
            choices = []
            for i in range(5):
                choices.append(
                    [first if i == 0 else first + 1, first + number])
                first = first + number

            self.fields[code] = NonValidationMultipleChoiceField(
                widget=CustomFilterCheckboxSelectMultiple(),
                label=attr.name,
                required=False,
                choices=[(
                    '%s,%s' % (i[0], i[1]),
                    '%s - %s' % (i[0], i[1]),
                    {
                        'product_count': self.query().filter(
                            attribute_values__value_integer__gte=i[0],
                            attribute_values__value_integer__lte=i[1],
                        ).count(),
                        'attrs': {'data-min': i[0], 'data-max': i[1]},
                    }
                )for i in choices],
            )

        for group in AttributeOptionGroup.objects.filter(site=self.site):
            self.fields[group.get_filter_param()] = \
                CustomFilterMultipleChoiceField(
                    widget=CustomFilterCheckboxSelectMultiple(),
                    label=group.name,
                    required=False,
                    choices=[(
                        i.id,
                        i.option,
                        {
                            'product_count': self.query().filter(
                                attribute_values__value_option=i).count(),
                            'attrs': {},
                        }
                    )for i in group.options.all()],
            )

    def query(self):
        query = Product.objects.filter(site=self.site)
        if self.categories:
            return query.filter(categories__in=self.categories)
        return query
