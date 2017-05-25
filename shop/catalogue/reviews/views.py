# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.views import View

from oscar.core.utils import redirect_to_referrer
from oscar.apps.catalogue.reviews.forms import VoteForm

from shop.catalogue.models import Product
from shop.catalogue.reviews.forms import ProductReviewForm, ProductQuestionForm
from shop.catalogue.reviews.models import ProductReview, ProductQuestion


class CreateProductReview(View):
    model = ProductReview
    form_class = ProductReviewForm

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        form = self.form_class(product, request.user, request.POST)
        if self.request.user.is_authenticated() and ProductReview.objects.filter(
                user=request.user, product=product).exists():
            return HttpResponse(status=409)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            return redirect_to_referrer(request, product.get_absolute_url())
        else:
            for error_list in form.errors.values():
                for msg in error_list:
                    messages.error(request, msg)
            return HttpResponseBadRequest()


class ProductQuestionView(View):
    model = ProductQuestion
    form_class = ProductQuestionForm

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        form = self.form_class(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.product = product
            question.save()
            return redirect_to_referrer(request, product.get_absolute_url())
        else:
            for error_list in form.errors.values():
                for msg in error_list:
                    messages.error(request, msg)
            return HttpResponseBadRequest()

class AddVoteView(View):
    """
    Simple view for voting on a review.

    We use the URL path to determine the product and review and use a 'delta'
    POST variable to indicate it the vote is up or down.
    """

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        review = get_object_or_404(ProductReview, pk=self.kwargs['pk'])

        form = VoteForm(review, request.user, request.POST)
        if form.is_valid():
            if form.is_up_vote:
                review.vote_up(request.user)
            elif form.is_down_vote:
                review.vote_down(request.user)
            messages.success(request, ("Thanks for voting!"))
        else:
            for error_list in form.errors.values():
                for msg in error_list:
                    messages.error(request, msg)
        return redirect_to_referrer(request, product.get_absolute_url())