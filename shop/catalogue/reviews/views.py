# -*- coding: utf-8 -*-
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from oscar.apps.catalogue.reviews.views import CreateProductReview as \
    CoreCreateProductReview
from oscar.core.utils import redirect_to_referrer

from shop.catalogue.models import Product
from shop.catalogue.reviews.forms import ProductReviewForm
from shop.catalogue.reviews.models import ProductReview


class CreateProductReview(View):
    model = ProductReview
    form_class = ProductReviewForm

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        form = self.form_class(product, request.user, request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            return redirect_to_referrer(request, product.get_absolute_url())
        else:
            for error_list in form.errors.values():
                for msg in error_list:
                    messages.error(request, msg)
            return HttpResponseBadRequest()
