# -*- coding: utf-8 -*-
import datetime
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (ListView, UpdateView, DeleteView)
from oscar.core.loading import get_class, get_model
from website.views import SiteMultipleObjectMixin
from oscar.views.generic import BulkEditMixin
from oscar.core.utils import format_datetime
from oscar.views import sort_queryset

ProductQuestion = get_model('reviews', 'ProductQuestion')
ReviewAnswer = get_model('reviews', 'ReviewAnswer')

OscarReviewUpdateView = get_class('dashboard.reviews.views',
                                  'ReviewUpdateView')
OscarReviewListView = get_class('dashboard.reviews.views',
                                'ReviewListView')
DashboardProductReviewForm = get_class('dashboard.reviews.forms',
                                       'DashboardProductReviewForm')
ProductQuestionForm = get_class('dashboard.reviews.forms',
                                'ProductQuestionForm')
ProductReviewAnswerForm = get_class('dashboard.reviews.forms',
                                    'ProductReviewAnswerForm')
ProductReviewAnswerSearchForm = get_class('dashboard.reviews.forms',
                                          'ProductReviewAnswerSearchForm')


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


class ReviewAnswerListView(SiteMultipleObjectMixin, BulkEditMixin, ListView):
    model = ReviewAnswer
    template_name = 'dashboard/reviews/reviewanswer_list.html'
    context_object_name = 'reviewanswers_list'
    form_class = ProductReviewAnswerSearchForm
    review_form_class = ProductReviewAnswerForm
    checkbox_object_name = 'review'
    desc_template = _("%(main_filter)s %(date_filter)s"
                      "%(kw_filter)s %(name_filter)s")

    def get(self, request, *args, **kwargs):
        response = super(ReviewAnswerListView, self).get(request, **kwargs)
        self.form = self.form_class()
        return response

    def get_date_from_to_queryset(self, date_from, date_to, queryset=None):
        """
        Get a ``QuerySet`` of ``ReviewAnswer`` items that match the time
        frame specified by *date_from* and *date_to*. Both parameters are
        expected to be in ``datetime`` format with *date_from* < *date_to*.
        If *queryset* is specified, it will be filtered according to the
        given dates. Otherwise, a new queryset for all ``ReviewAnswer``
        items is created.
        """
        if queryset is None:
            queryset = self.model.objects.all()

        if date_from and date_to:
            # Add 24 hours to make search inclusive
            date_to = date_to + datetime.timedelta(days=1)
            queryset = queryset.filter(
                date_created__gte=date_from
            ).filter(
                date_created__lt=date_to
            )
            self.desc_ctx['date_filter'] \
                = _(" created between %(start_date)s and %(end_date)s") % {
                    'start_date': format_datetime(date_from),
                    'end_date': format_datetime(date_to)}
        elif date_from:
            queryset = queryset.filter(date_created__gte=date_from)
            self.desc_ctx['date_filter'] \
                = _(" created after %s") % format_datetime(date_from)
        elif date_to:
            # Add 24 hours to make search inclusive
            date_to = date_to + datetime.timedelta(days=1)
            queryset = queryset.filter(date_created__lt=date_to)
            self.desc_ctx['date_filter'] \
                = _(" created before %s") % format_datetime(date_to)

        return queryset

    def get_queryset(self):
        queryset = self.model.objects.select_related('review').select_related('reply_to').all()
        queryset = sort_queryset(queryset, self.request,
                                 ['score', 'total_votes', 'date_created'])
        self.desc_ctx = {
            'main_filter': _('All review answers'),
            'date_filter': '',
            'kw_filter': '',
            'name_filter': '',
        }

        self.form = self.form_class(self.request.GET)
        if not self.form.is_valid():
            return queryset

        data = self.form.cleaned_data

        if data['keyword']:
            queryset = queryset.filter(
                Q(body__icontains=data['keyword'])
            ).distinct()
            self.desc_ctx['kw_filter'] \
                = _(" with keyword matching '%s'") % data['keyword']

        queryset = self.get_date_from_to_queryset(data['date_from'],
                                                  data['date_to'], queryset)

        if data['name']:
            # If the value is two words, then assume they are first name and
            # last name
            parts = data['name'].split()
            if len(parts) >= 2:
                queryset = queryset.filter(
                    user__first_name__istartswith=parts[0],
                    user__last_name__istartswith=parts[1]
                ).distinct()
            else:
                queryset = queryset.filter(
                    Q(user__first_name__istartswith=parts[0]) |
                    Q(user__last_name__istartswith=parts[-1])
                ).distinct()
            self.desc_ctx['name_filter'] \
                = _(" with customer name matching '%s'") % data['name']

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ReviewAnswerListView, self).get_context_data(**kwargs)
        context['review_form'] = self.review_form_class()
        context['form'] = self.form
        context['description'] = self.desc_template % self.desc_ctx
        return context


class ReviewAnswerUpdateView(UpdateView):
    model = ReviewAnswer
    template_name = 'dashboard/reviews/reviewanswer_update.html'
    form_class = ProductReviewAnswerForm
    context_object_name = 'review'

    def get_success_url(self):
        return reverse('dashboard:reviewanswers-list')


class ReviewAnswerDeleteView(DeleteView):
    model = ReviewAnswer
    template_name = 'dashboard/reviews/reviewanswer_delete.html'
    context_object_name = 'review'

    def get_success_url(self):
        return reverse('dashboard:reviewanswers-list')
