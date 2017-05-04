# -*-coding:utf8-*-

from django import forms

from shop.order.models import SimpleOrder, ShippingMethod, PaymentMethod
from .models import OneClickOrder


class OneClickOrderForm(forms.ModelForm):
    phone = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_message=(
            "Phone number must be entered in the format: '+999999999'. "
            "Up to 15 digits allowed."),
        label=''
    )

    class Meta:
        model = OneClickOrder
        fields = ['phone']


class SimpleOrderForm(forms.ModelForm):
    phone = forms.RegexField(
        widget=forms.TextInput(attrs={'placeholder': u'Телефон*'}),
        regex=r'^\+?1?\d{9,15}$',
        error_message=(
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    shipping_method = forms.ModelChoiceField(
        queryset=ShippingMethod.objects.all(), empty_label='Способ доставки')
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.all(), empty_label='Способ оплаты')

    class Meta:
        model = SimpleOrder
        exclude = ('basket', 'check_blank', 'order_status')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': u'Имя и фамилия*'}),
            'comment': forms.Textarea(
                attrs={'placeholder': u'Комментарий к заказу'}),
            'email': forms.TextInput(attrs={'placeholder': u'E-mail'}),
            'city': forms.TextInput(attrs={'placeholder': u'Город'}),
            'address': forms.TextInput(attrs={'placeholder': u'Адрес'}),
        }
