# -*- coding:utf-8 -*-

import os

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from django.db import transaction

from website.views import SiteTemplateResponseMixin
from .forms import OrderForm, CallRequestForm, InstallmentPaymentForm
from .utils import OrderCreator


class SimpleOrderView(SiteTemplateResponseMixin, FormView):
    form_class = OrderForm
    template_name = 'checkout/order.html'
    success_template_name = 'checkout/order_success.html'

    def form_valid(self, form):
        if self.request.basket.num_lines:
            self.request.basket.submit()
            with transaction.atomic():
                order = OrderCreator().place_order(
                    basket=self.request.basket,
                    total=self.request.basket.total_excl_tax,
                    shipping_method=form.cleaned_data['shipping_method'],
                    shipping_charge=form.cleaned_data['shipping_method'].shipping_price,
                    user=self.request.user,
                    name=form.cleaned_data['name'],
                    payment_method=form.cleaned_data['payment_method'],
                    city=form.cleaned_data['city'],
                    phone=form.cleaned_data['phone'],
                    comment=form.cleaned_data['comment'],
                    guest_email=form.cleaned_data['guest_email'],
                    request=self.request)

            return render(self.request, self.get_success_template_name(),
                          {'order': order})
        else:
            return redirect('/')

    def get_success_template_name(self):
        template = get_current_site(self.request).config.template
        return os.path.join(template, self.success_template_name)


class CallRequestCreateView(CreateView):
    form_class = CallRequestForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        site = get_current_site(self.request)
        instance.site = site
        instance.save()
        return HttpResponse(status=201)

    def form_invalid(self, form):
        return HttpResponse(status=403)


class InstallmentPaymentCreateView(CreateView):
    form_class = InstallmentPaymentForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        site = get_current_site(self.request)
        instance.site = site
        instance.save()
        return HttpResponse(status=201)

    def form_invalid(self, form):
        return HttpResponse(status=403)
