from oscar.apps.dashboard.reviews.app import (
    ReviewsApplication as CoreReviewsApplication)

from oscar.core.loading import get_class
from django.conf.urls import url


class ReviewsApplication(CoreReviewsApplication):

    list_view = get_class('dashboard.reviews.views',
                          'ReviewListView')
    update_view = get_class('dashboard.reviews.views',
                            'ReviewUpdateView')
    product_question_list_view = get_class('dashboard.reviews.views',
                                           'ProductQuestionListView')
    product_question_update_view = get_class('dashboard.reviews.views',
                                             'ProductQuestionUpdateView')
    product_question_delete_view = get_class('dashboard.reviews.views',
                                             'ProductQuestionDeleteView')
    reviewanswers_list_view = get_class('dashboard.reviews.views',
                                        'ReviewAnswerListView')
    reviewanswers_update_view = get_class('dashboard.reviews.views',
                                          'ReviewAnswerUpdateView')
    reviewanswers_delete_view = get_class('dashboard.reviews.views',
                                          'ReviewAnswerDeleteView')

    def get_urls(self):

        urls = [
            url(r'^productquestion/$',
                self.product_question_list_view.as_view(),
                name='productquestion-list'),
            url(r'^productquestion/edit/(?P<pk>[\d]+)/$',
                self.product_question_update_view.as_view(),
                name='productquestion-detail'),
            url(r'^productquestion/delete/(?P<pk>[\d]+)/$',
                self.product_question_delete_view.as_view(),
                name='productquestion-delete'),
            url(r'^answers/$',
                self.reviewanswers_list_view.as_view(),
                name='reviewanswers-list'),
            url(r'^answers/edit/(?P<pk>[\d]+)/$',
                self.reviewanswers_update_view.as_view(),
                name='reviewanswers-update'),
            url(r'^answers/delete/(?P<pk>[\d]+)/$',
                self.reviewanswers_delete_view.as_view(),
                name='reviewanswers-delete'),
        ]

        urls = self.post_process_urls(urls)
        processed_urls = super(ReviewsApplication, self).get_urls()
        return urls + processed_urls

application = ReviewsApplication()
