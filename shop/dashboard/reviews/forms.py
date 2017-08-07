from django import forms
from oscar.core.loading import get_model
from django.utils.translation import ugettext_lazy as _

ProductReview = get_model('reviews', 'productreview')


class DashboardProductReviewForm(forms.ModelForm):
    choices = (
        (ProductReview.APPROVED, _('Approved')),
        (ProductReview.REJECTED, _('Rejected')),
    )
    status = forms.ChoiceField(choices=choices, label=_("Status"))

    class Meta:
        model = ProductReview
        fields = ('title', 'body', 'advantage', 'disadvantage', 'get_notification', 'score', 'status', )
