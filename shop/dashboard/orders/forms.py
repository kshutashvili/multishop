from oscar.apps.dashboard.orders.forms import *
from django import forms
from oscar.core.loading import get_model
from django.forms.models import inlineformset_factory

OneClickOrder = get_model('order', 'OneClickOrder')
Basket = get_model('basket', 'basket')
Line = get_model('basket', 'line')
CallRequest = get_model('order', 'CallRequest')


class OneClickOrderForm(forms.ModelForm):

    class Meta:
        model = OneClickOrder
        exclude = ('site', )

BasketItemsFormSet = inlineformset_factory(Basket,
                                           Line,
                                           fields=('quantity', ),
                                           extra=0)


class CallRequestForm(forms.ModelForm):

    class Meta:
        model = CallRequest
        exclude = ('site', )
