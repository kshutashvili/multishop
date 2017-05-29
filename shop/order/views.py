# -*- coding:utf-8 -*-

import os

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView

from website.views import SiteTemplateResponseMixin
from .forms import OrderForm, CallRequestForm
from .utils import OrderCreator


class SimpleOrderView(SiteTemplateResponseMixin, FormView):
    form_class = OrderForm
    template_name = 'checkout/order.html'
    success_template_name = 'checkout/order_success.html'

    def form_valid(self, form):
        if self.request.basket.num_lines:
            self.request.basket.submit()
            order = OrderCreator().place_order(self.request.basket,
                                               self.request.basket.total_excl_tax,
                                               form.cleaned_data[
                                                   'shipping_method'],
                                               form.cleaned_data[
                                                   'shipping_method'].shipping_price,
                                               user=self.request.user,
                                               request=self.request)
            order.name = form.cleaned_data['name']
            order.payment_method = form.cleaned_data['payment_method']
            order.city = form.cleaned_data['city']
            order.phone = form.cleaned_data['phone']
            order.comment = form.cleaned_data['comment']
            order.guest_email = form.cleaned_data['guest_email']
            order.save()
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
