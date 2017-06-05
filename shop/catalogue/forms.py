from __future__ import unicode_literals

from django import forms

from shop.catalogue.models import (AttributeOptionGroup, Product,
                                   ProductAttribute)
from shop.catalogue.widgets import CustomFilterCheckboxSelectMultiple
from shop.catalogue.fields import CustomFilterMultipleChoiceField


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
        for group in AttributeOptionGroup.objects.filter(site=self.site):
            self.fields[u'filter_%s' % group.name] = \
                CustomFilterMultipleChoiceField(
                    widget=CustomFilterCheckboxSelectMultiple(),
                    label=group.name,
                    choices=[
                        (i.id, i.option, Product.objects.filter(
                            attribute_values__value_option=i).count())
                        for i in group.options.all()],
                    required=False
            )
