# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext as _

from shop.order.models import Order, \
    OneClickOrder, CallRequest, ShippingMethod, PaymentMethod, InstallmentPayment


PHONE_ERROR_MESSAGE = _(
    "Phone number must be entered in the format: '+999999999'. "
    "Up to 15 digits allowed."
)


class OneClickOrderForm(forms.ModelForm):
    phone = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_message=PHONE_ERROR_MESSAGE,
        label=''
    )

    class Meta:
        model = OneClickOrder
        fields = ['phone']


class InstallmentPaymentForm(forms.ModelForm):
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                             error_message=PHONE_ERROR_MESSAGE,
                             label='')

    class Meta:
        model = InstallmentPayment
        fields = ['phone', ]

    def __init__(self, *args, **kwargs):
        super(InstallmentPaymentForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs = {'placeholder': u'+380(__)_______'}


class OrderForm(forms.ModelForm):
    phone = forms.RegexField(
        widget=forms.TextInput(attrs={'placeholder': _(u'Телефон')}),
        regex=r'^\+?1?\d{9,15}$',
        error_message=PHONE_ERROR_MESSAGE,
    )
    shipping_method = forms.ModelChoiceField(
        queryset=ShippingMethod.objects.all(),
        empty_label=_(u'Способ доставки')
    )
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(), empty_label=_(u'Способ оплаты'))

    class Meta:
        model = Order
        exclude = ('basket', 'check_blank', 'order_status', 'number',)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _(u'Имя и фамилия*')}),
            'comment': forms.Textarea(
                attrs={'placeholder': _(u'Комментарий к заказу')}),
            'guest_email': forms.TextInput(attrs={'placeholder': _('E-mail')}),
            'city': forms.TextInput(
                attrs={'placeholder': _(u'Город')}),
        }


class CallRequestForm(forms.ModelForm):
    phone = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_message=PHONE_ERROR_MESSAGE,
        label=''
    )

    class Meta:
        model = CallRequest
        fields = ['name', 'phone']
