from oscar.apps.dashboard.orders.forms import *
from django import forms
from oscar.core.loading import get_model
from django.forms.models import inlineformset_factory

OneClickOrder = get_model('order', 'OneClickOrder')
Basket = get_model('basket', 'basket')
Line = get_model('basket', 'line')


class OneClickOrderForm(forms.ModelForm):

    class Meta:
        model = OneClickOrder
        exclude = ('site', )

BasketItemsFormSet = inlineformset_factory(Basket,
                                           Line,
                                           fields=('quantity', ),
                                           extra=0)
