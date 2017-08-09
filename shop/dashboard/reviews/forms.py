# -*- coding: utf-8 -*-
from django import forms
from oscar.core.loading import get_model
from django.utils.translation import ugettext_lazy as _

ProductReview = get_model('reviews', 'productreview')
ProductQuestion = get_model('reviews', 'ProductQuestion')
ProductReviewAnswer = get_model('reviews', 'ReviewAnswer')


class DashboardProductReviewForm(forms.ModelForm):
    choices = (
        (ProductReview.APPROVED, _('Approved')),
        (ProductReview.REJECTED, _('Rejected')),
    )
    status = forms.ChoiceField(choices=choices, label=_("Status"))

    class Meta:
        model = ProductReview
        fields = ('title', 'body', 'advantage', 'disadvantage',
                  'get_notification', 'score', 'status', )


class ProductQuestionForm(forms.ModelForm):

    class Meta:
        model = ProductQuestion
        fields = '__all__'


class ProductReviewAnswerForm(forms.ModelForm):

    class Meta:
        model = ProductReviewAnswer
        fields = ('review', 'user', 'name', 'email',
                  'body', 'reply_to', 'get_notification', )


class ProductReviewAnswerSearchForm(forms.Form):
    keyword = forms.CharField(required=False, label=_("Keyword"))
    date_from = forms.DateTimeField(required=False, label=_("Date from"))
    date_to = forms.DateTimeField(required=False, label=_('to'))
    name = forms.CharField(required=False, label=_('Customer name'))
