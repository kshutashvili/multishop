from oscar.apps.dashboard.reviews.app import (
    ReviewsApplication as CoreReviewsApplication)

from oscar.core.loading import get_class


class ReviewsApplication(CoreReviewsApplication):

    list_view = get_class('dashboard.reviews.views',
                          'ReviewListView')
    update_view = get_class('dashboard.reviews.views',
                            'ReviewUpdateView')

application = ReviewsApplication()
