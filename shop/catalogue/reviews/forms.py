# -*- coding: utf-8 -*-
from django import forms
from django.forms import CheckboxInput
from django.forms import HiddenInput
from oscar.apps.catalogue.reviews.forms import ProductReviewForm as \
    CoreProductReviewForm

from shop.catalogue.reviews.models import ProductReview, ProductQuestion, ReviewAnswer


class ProductReviewForm(CoreProductReviewForm):

    class Meta:
        model = ProductReview
        fields = ('score', 'body', 'name', 'email', 'site', 'advantage',
                  'disadvantage', 'get_notification')
        widgets = {
            'site': HiddenInput(),
            'get_notification': CheckboxInput(),
        }

    def __init__(self, product, user=None, *args, **kwargs):
        super(ProductReviewForm, self).__init__(product, user, *args, **kwargs)
        self.fields['advantage'].required = False
        self.fields['disadvantage'].required = False
        self.fields['get_notification'].required = False


class ProductQuestionForm(forms.ModelForm):
    class Meta:
        model = ProductQuestion
        fields = ['name', 'email', 'phone', 'text']


class ReviewAnswerForm(forms.ModelForm):

    class Meta:
        model = ReviewAnswer
        fields = ('name', 'email', 'body', 'site', 'get_notification')
        widgets = {
            'site': HiddenInput(),
            'get_notification': CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewAnswerForm, self).__init__(*args, **kwargs)
        self.fields['get_notification'].required = False
