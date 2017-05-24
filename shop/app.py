from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from oscar.app import Shop as DefaultShop
from oscar.views.decorators import login_forbidden

from shop.catalogue.app import application as catalogue_app


class Shop(DefaultShop):
    catalogue_app = catalogue_app

    def get_urls(self):
        urls = [
            url(r'^basket/', self.basket_app.urls),
            url(r'^checkout/', self.checkout_app.urls),
            url(r'^accounts/', self.customer_app.urls),
            url(r'^search/', self.search_app.urls),
            url(r'^dashboard/', self.dashboard_app.urls),
            url(r'^offers/', self.offer_app.urls),

            # Password reset - as we're using Django's default view functions,
            # we can't namespace these urls as that prevents
            # the reverse function from working.
            url(r'^password-reset/$',
                login_forbidden(auth_views.password_reset),
                {'password_reset_form': self.password_reset_form,
                 'post_reset_redirect': reverse_lazy('password-reset-done')},
                name='password-reset'),
            url(r'^password-reset/done/$',
                login_forbidden(auth_views.password_reset_done),
                name='password-reset-done'),
            url(
                r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                login_forbidden(auth_views.password_reset_confirm),
                {
                    'post_reset_redirect': reverse_lazy(
                        'password-reset-complete'),
                    'set_password_form': self.set_password_form,
                },
                name='password-reset-confirm'),
            url(r'^password-reset/complete/$',
                login_forbidden(auth_views.password_reset_complete),
                name='password-reset-complete'),
        ]

        if settings.OSCAR_PROMOTIONS_ENABLED:
            urls.append(url(r'', self.promotions_app.urls))
        urls.append(url(r'^', self.catalogue_app.urls))
        return urls


application = Shop()
