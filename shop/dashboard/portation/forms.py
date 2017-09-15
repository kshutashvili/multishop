from django import forms
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from shop.catalogue.models import ProductClass
from shop.catalogue.models import ProductAttribute


class ImportForm(forms.Form):

    file = forms.FileField(
        label=_('File with backup'),
    )


class ExportForm(forms.Form):
    FIELDS = (
        ('upc', _('UPC')),
        ('title', _('Title')),
        ('description', _('Description')),
        ('categories', _('Categories')),
    )

    product_class = forms.ModelChoiceField(
        queryset=None,
        label=_('Product class'),
    )
    fields = forms.MultipleChoiceField(
        choices=FIELDS,
        label=_('Fields'),
    )
    attributes = forms.ModelMultipleChoiceField(
        queryset=ProductAttribute.objects.all(),
        label=_('Attributes'),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.site = Site.objects.get_current(self.request)
        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields['product_class'].queryset = ProductClass.objects.filter(
            site=self.site)
