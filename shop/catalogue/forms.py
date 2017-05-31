from __future__ import unicode_literals

from collections import defaultdict

from django import forms

from shop.catalogue.models import (AttributeOptionGroup, Product,
                                   ProductAttribute)


class FilterForm(forms.Form):
    attr_fields = {ProductAttribute.INTEGER: forms.IntegerField,
                   ProductAttribute.BOOLEAN: forms.BooleanField,
                   ProductAttribute.FLOAT: forms.FloatField,
                   ProductAttribute.DATE: forms.DateField,
                   ProductAttribute.TEXT: forms.CharField}

    def __init__(self, site, *args, **kwargs):
        self.site = site
        super(FilterForm, self).__init__(*args, **kwargs)

        self.make_filter()

    def make_filter(self):
        for attr in ProductAttribute.objects.filter(type__in=self.attr_fields):
            self.fields['filter_%s' % attr.code] = self.attr_fields[attr.type](
                label=attr.name,
                required=False
            )
        for group in AttributeOptionGroup.objects.filter(site=self.site):
            self.fields[u'filter_%s' % group.name] = \
                forms.MultipleChoiceField(
                    widget=forms.CheckboxSelectMultiple(),
                    label=group.name,
                    choices=[
                        (i.id, u'%s (%s)' % (i.option, Product.objects.filter(
                            attribute_values__value_option=i).count()))
                        for i in group.options.all()],
                    required=False
                )
