from django import forms
from django.forms.models import inlineformset_factory

from django.contrib.sites.models import Site
from config.models import SiteConfig


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'


class SiteConfigForm(forms.ModelForm):

    class Meta:
        model = SiteConfig
        fields = '__all__'
        exclude = ('site', )

