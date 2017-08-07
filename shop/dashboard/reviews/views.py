# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (ListView, UpdateView, DeleteView)
from oscar.core.loading import get_class, get_model
from website.views import SiteMultipleObjectMixin

ProductQuestion = get_model('reviews', 'ProductQuestion')

OscarReviewUpdateView = get_class('dashboard.reviews.views',
                                  'ReviewUpdateView')
OscarReviewListView = get_class('dashboard.reviews.views',
                                'ReviewListView')
DashboardProductReviewForm = get_class('dashboard.reviews.forms',
                                       'DashboardProductReviewForm')
ProductQuestionForm = get_class('dashboard.reviews.forms',
                                'ProductQuestionForm')


class ReviewListView(SiteMultipleObjectMixin, OscarReviewListView):
    pass


class ReviewUpdateView(OscarReviewUpdateView):
    form_class = DashboardProductReviewForm


class ProductQuestionListView(ListView):

    model = ProductQuestion
    context_object_name = 'questions'
    template_name = 'dashboard/reviews/productquestion_list.html'

    def get_queryset(self):

        qs = super(ProductQuestionListView, self).get_queryset()
        qs = qs.filter(product__site=get_current_site(self.request))

        return qs


class ProductQuestionCreateUpdateView(UpdateView):
    model = ProductQuestion
    context_object_name = 'question'
    form_class = ProductQuestionForm
    template_name = 'dashboard/reviews/productquestion_detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(ProductQuestionCreateUpdateView, self).get_context_data(
            *args, **kwargs)

        ctx["title"] = self.get_title()

        return ctx


class ProductQuestionUpdateView(ProductQuestionCreateUpdateView):

    def get_title(self):
        return _(u"Изменение вопроса о товаре '%s'") % self.object

    def get_success_url(self):
        messages.info(self.request, _(u"Вопрос о товаре успешно сохранен"))
        return reverse("dashboard:productquestion-list")

    def get_object(self):
        obj = get_object_or_404(ProductQuestion, pk=self.kwargs['pk'])
        return obj

    def form_valid(self, form):

        ctx = self.get_context_data()

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())

        return self.render_to_response(ctx)


class ProductQuestionDeleteView(DeleteView):
    template_name = 'dashboard/reviews/productquestion_delete.html'
    model = ProductQuestion
    form_class = ProductQuestionForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(ProductQuestionDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _(u"Удаление вопроса о товаре '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.info(self.request, _(u"Вопрос о товаре успешно удален"))
        return reverse("dashboard:productquestion-list")
