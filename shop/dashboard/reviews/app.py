from oscar.apps.dashboard.reviews.app import (
    ReviewsApplication as CoreReviewsApplication)

from .views import ReviewUpdateView, ReviewListView


class ReviewsApplication(CoreReviewsApplication):

    list_view = ReviewListView
    update_view = ReviewUpdateView

application = ReviewsApplication()
