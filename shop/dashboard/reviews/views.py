from . import forms
from oscar.core.loading import get_class
from website.views import SiteMultipleObjectMixin


OscarReviewUpdateView = get_class('dashboard.reviews.views',
                                  'ReviewUpdateView')
OscarReviewListView = get_class('dashboard.reviews.views',
                                'ReviewListView')


class ReviewListView(SiteMultipleObjectMixin, OscarReviewListView):
    pass


class ReviewUpdateView(OscarReviewUpdateView):
    form_class = forms.DashboardProductReviewForm
