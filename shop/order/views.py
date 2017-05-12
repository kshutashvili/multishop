# -*-coding:utf-8-*-

import os

from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from website.views import SiteTemplateResponseMixin
from .forms import SimpleOrderForm, CallRequestForm


class SimpleOrderView(SiteTemplateResponseMixin, CreateView):
    form_class = SimpleOrderForm
    template_name = 'checkout/order.html'
    success_template_name = 'checkout/order_success.html'

    def form_valid(self, form):
        if self.request.basket.num_lines:
            instance = form.save(commit=False)
            instance.basket = self.request.basket
            instance.save()
            self.request.basket.submit()
            return render(self.request, self.get_success_template_name(),
                          {'order': instance})
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
