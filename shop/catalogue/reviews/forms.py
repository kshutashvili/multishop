# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from django.forms import HiddenInput
from oscar.apps.catalogue.reviews.forms import ProductReviewForm as \
    CoreProductReviewForm
from oscar.core.compat import user_is_authenticated

from shop.catalogue.reviews.models import ProductReview


class ProductReviewForm(CoreProductReviewForm):

    class Meta:
        model = ProductReview
        fields = ('score', 'body', 'name', 'email', 'site', 'advantage',
                  'disadvantage')
        widgets = {
            'site': HiddenInput(),
        }

    def __init__(self, product, user=None, *args, **kwargs):
        super(ProductReviewForm, self).__init__(product, user, *args, **kwargs)
        self.fields['advantage'].required = False
        self.fields['disadvantage'].required = False
