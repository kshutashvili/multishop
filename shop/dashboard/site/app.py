# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf.urls import url
from oscar.core.application import Application

from shop.dashboard.site.views import (SiteCreateView, SiteUpdateView,
                                       SiteDeleteView, SiteListView,
                                       CityListView, CityUpdateView,
                                       CityCreateView, CityDeleteView,
                                       SocialNetRefListView,
                                       SocialNetRefCreateView,
                                       SocialNetRefUpdateView,
                                       SocialNetRefDeleteView,
                                       FlatPageListView, FlatPageCreateView,
                                       FlatPageUpdateView, FlatPageDeleteView,
                                       ContactMessageListView,
                                       ContactMessageUpdateView,
                                       ContactMessageDeleteView,
                                       SiteContactConfigView,
                                       TimetableListView,
                                       TimetableCreateView,
                                       TimetableUpdateView,
                                       TimetableDeleteView,
                                       MetaTagListView,
                                       MetaTagCreateView,
                                       MetaTagUpdateView,
                                       MetaTagDeleteView,
                                       FilterDescriptionListView,
                                       FilterDescriptionCreateView,
                                       FilterDescriptionUpdateView,
                                       FilterDescriptionDeleteView,
                                       TextOneListView,
                                       TextOneCreateView,
                                       TextOneUpdateView,
                                       TextOneDeleteView,
                                       TextTwoListView,
                                       TextTwoCreateView,
                                       TextTwoUpdateView,
                                       TextTwoDeleteView,
                                       TextThreeListView,
                                       TextThreeCreateView,
                                       TextThreeUpdateView,
                                       TextThreeDeleteView,
                                       TextFourListView,
                                       TextFourCreateView,
                                       TextFourUpdateView,
                                       TextFourDeleteView,
                                       LandingConfigView,
                                       FuelConfigurationListView,
                                       FuelConfigurationCreateView,
                                       FuelConfigurationUpdateView,
                                       FuelConfigurationDeleteView,
                                       BenefitItemListView,
                                       BenefitItemCreateView,
                                       BenefitItemUpdateView,
                                       BenefitItemDeleteView,
                                       OverviewItemListView,
                                       OverviewItemCreateView,
                                       OverviewItemUpdateView,
                                       OverviewItemDeleteView,
                                       ReviewItemListView,
                                       ReviewItemCreateView,
                                       ReviewItemUpdateView,
                                       ReviewItemDeleteView,
                                       DeliveryAndPayListView,
                                       DeliveryAndPayCreateView,
                                       DeliveryAndPayUpdateView,
                                       DeliveryAndPayDeleteview,
                                       HeaderMenuListView,
                                       HeaderMenuCreateView,
                                       HeaderMenuUpdateView,
                                       HeaderMenuDeleteView,
                                       FooterMenuListView,
                                       FooterMenuCreateView,
                                       FooterMenuUpdateView,
                                       FooterMenuDeleteView,
                                       MenuCategoryListView,
                                       MenuCategoryCreateView,
                                       MenuCategoryUpdateView,
                                       MenuCategoryDeleteView,
                                       SideMenuListView,
                                       SideMenuCreateView,
                                       SideMenuUpdateView,
                                       SideMenuDeleteView,
                                       InstallmentPaymentListView,
                                       InstallmentPaymentCreateView,
                                       InstallmentPaymentUpdateView,
                                       InstallmentPaymentDeleteView,
                                       UserListView,
                                       UserCreateView,
                                       UserUpdateView,
                                       UserDeleteView,
                                       UserPasswordChangeView,
                                       CloneProductView)


class SiteDashboardApplication(Application):
    name = None
    default_permissions = ['is_staff', ]

    site_create_view = SiteCreateView
    site_update_view = SiteUpdateView
    site_delete_view = SiteDeleteView
    site_list_view = SiteListView
    city_list_view = CityListView
    city_update_view = CityUpdateView
    city_create_view = CityCreateView
    city_delete_view = CityDeleteView
    socialnetref_list_view = SocialNetRefListView
    socialnetref_create_view = SocialNetRefCreateView
    socialnetref_update_view = SocialNetRefUpdateView
    socialnetref_delete_view = SocialNetRefDeleteView
    flatpage_list_view = FlatPageListView
    flatpage_create_view = FlatPageCreateView
    flatpage_update_view = FlatPageUpdateView
    flatpage_delete_view = FlatPageDeleteView
    contactmessage_list_view = ContactMessageListView
    contactmessage_update_view = ContactMessageUpdateView
    contactmessage_delete_view = ContactMessageDeleteView
    sitecontact_config_view = SiteContactConfigView
    timetable_list_view = TimetableListView
    timetable_create_view = TimetableCreateView
    timetable_update_view = TimetableUpdateView
    timetable_delete_view = TimetableDeleteView
    metatag_list_view = MetaTagListView
    metatag_create_view = MetaTagCreateView
    metatag_update_view = MetaTagUpdateView
    metatag_delete_view = MetaTagDeleteView
    filterdescription_list_view = FilterDescriptionListView
    filterdescription_create_view = FilterDescriptionCreateView
    filterdescription_update_view = FilterDescriptionUpdateView
    filterdescription_delete_view = FilterDescriptionDeleteView
    textone_list_view = TextOneListView
    textone_create_view = TextOneCreateView
    textone_update_view = TextOneUpdateView
    textone_delete_view = TextOneDeleteView
    texttwo_list_view = TextTwoListView
    texttwo_create_view = TextTwoCreateView
    texttwo_update_view = TextTwoUpdateView
    texttwo_delete_view = TextTwoDeleteView
    textthree_list_view = TextThreeListView
    textthree_create_view = TextThreeCreateView
    textthree_update_view = TextThreeUpdateView
    textthree_delete_view = TextThreeDeleteView
    textfour_list_view = TextFourListView
    textfour_create_view = TextFourCreateView
    textfour_update_view = TextFourUpdateView
    textfour_delete_view = TextFourDeleteView
    configuration_view = LandingConfigView
    fuel_list_view = FuelConfigurationListView
    fuel_create_view = FuelConfigurationCreateView
    fuel_update_view = FuelConfigurationUpdateView
    fuel_delete_view = FuelConfigurationDeleteView
    benefit_list_view = BenefitItemListView
    benefit_create_view = BenefitItemCreateView
    benefit_update_view = BenefitItemUpdateView
    benefit_delete_view = BenefitItemDeleteView
    overview_list_view = OverviewItemListView
    overview_create_view = OverviewItemCreateView
    overview_update_view = OverviewItemUpdateView
    overview_delete_view = OverviewItemDeleteView
    review_list_view = ReviewItemListView
    review_create_view = ReviewItemCreateView
    review_update_view = ReviewItemUpdateView
    review_delete_view = ReviewItemDeleteView
    deliverypay_list_view = DeliveryAndPayListView
    deliverypay_create_view = DeliveryAndPayCreateView
    deliverypay_update_view = DeliveryAndPayUpdateView
    deliverypay_delete_view = DeliveryAndPayDeleteview
    headermenu_list_view = HeaderMenuListView
    headermenu_create_view = HeaderMenuCreateView
    headermenu_update_view = HeaderMenuUpdateView
    headermenu_delete_view = HeaderMenuDeleteView
    footermenu_list_view = FooterMenuListView
    footermenu_create_view = FooterMenuCreateView
    footermenu_update_view = FooterMenuUpdateView
    footermenu_delete_view = FooterMenuDeleteView
    menucategory_list_view = MenuCategoryListView
    menucategory_create_view = MenuCategoryCreateView
    menucategory_update_view = MenuCategoryUpdateView
    menucategory_delete_view = MenuCategoryDeleteView
    sidemenu_list_view = SideMenuListView
    sidemenu_create_view = SideMenuCreateView
    sidemenu_update_view = SideMenuUpdateView
    sidemenu_delete_view = SideMenuDeleteView
    installment_list_view = InstallmentPaymentListView
    installment_create_view = InstallmentPaymentCreateView
    installment_update_view = InstallmentPaymentUpdateView
    installment_delete_view = InstallmentPaymentDeleteView
    user_list_view = UserListView
    user_create_view = UserCreateView
    user_update_view = UserUpdateView
    user_delete_view = UserDeleteView
    user_change_password_view = UserPasswordChangeView
    clone_product_view = CloneProductView

    def get_urls(self):
        urls = [
            url(r'^add/$', self.site_create_view.as_view(),
                name='site-add'),
            url(r'^sites/$', self.site_list_view.as_view(),
                name='site-list'),
            url(r'^site/edit/(?P<pk>[\d]+)/$', self.site_update_view.as_view(),
                name='site-detail'),
            url(r'^site/edit/$', self.site_update_view.as_view(),
                {'is_current': True}, name='site-detail-current'
                ),
            url(r'site/delete/(?P<pk>[\d]+)/$', self.site_delete_view.as_view(),
                name='site-delete'),
            url(r'^city/$', self.city_list_view.as_view(),
                name='city-list'),
            url(r'^city/add/$', self.city_create_view.as_view(),
                name='city-create'),
            url(r'^city/edit/(?P<pk>[\d]+)/$', self.city_update_view.as_view(),
                name='city-detail'),
            url(r'^city/delete/(?P<pk>[\d]+)/$', self.city_delete_view.as_view(),
                name='city-delete'),
            url(r'^social_ref/$', self.socialnetref_list_view.as_view(),
                name='socialref-list'),
            url(r'^social_ref/add/$', self.socialnetref_create_view.as_view(),
                name='socialref-create'),
            url(r'^social_ref/edit/(?P<pk>[\d]+)/$', self.socialnetref_update_view.as_view(),
                name='socialref-detail'),
            url(r'^social_ref/delete/(?P<pk>[\d]+)/$', self.socialnetref_delete_view.as_view(),
                name='socialref-delete'),
            url(r'^flatpage/$', self.flatpage_list_view.as_view(),
                name='flatpage-list'),
            url(r'^flatpage/add/$', self.flatpage_create_view.as_view(),
                name='flatpage-create'),
            url(r'^flatpage/edit/(?P<pk>[\d]+)/$', self.flatpage_update_view.as_view(),
                name='flatpage-detail'),
            url(r'^flatpage/delete/(?P<pk>[\d]+)/$', self.flatpage_delete_view.as_view(),
                name='flatpage-delete'),
            url(r'^contactmessage/$', self.contactmessage_list_view.as_view(),
                name='contactmessage-list'),
            url(r'^contactmessage/edit/(?P<pk>[\d]+)/$', self.contactmessage_update_view.as_view(),
                name='contactmessage-detail'),
            url(r'^contactmessage/delete/(?P<pk>[\d]+)/$', self.contactmessage_delete_view.as_view(),
                name='contactmessage-delete'),
            url(r'contactsconfig/$', self.sitecontact_config_view.as_view(),
                name='sitecontact-edit'),
            url(r'^timetable/$', self.timetable_list_view.as_view(),
                name='timetable-list'),
            url(r'^timetable/add/$', self.timetable_create_view.as_view(),
                name='timetable-create'),
            url(r'^timetable/edit/(?P<pk>[\d]+)/$', self.timetable_update_view.as_view(),
                name='timetable-detail'),
            url(r'^timetable/delete/(?P<pk>[\d]+)/$', self.timetable_delete_view.as_view(),
                name='timetable-delete'),
            url(r'^metatag/$', self.metatag_list_view.as_view(),
                name='metatag-list'),
            url(r'^metatag/add/$', self.metatag_create_view.as_view(),
                name='metatag-create'),
            url(r'^metatag/edit/(?P<pk>[\d]+)/$', self.metatag_update_view.as_view(),
                name='metatag-detail'),
            url(r'^metatag/delete/(?P<pk>[\d]+)/$', self.metatag_delete_view.as_view(),
                name='metatag-delete'),
            # filter description URLs
            url(r'^filterdescription/$', self.filterdescription_list_view.as_view(),
                name='filterdescription-list'),
            url(r'^filterdescription/add/$', self.filterdescription_create_view.as_view(),
                name='filterdescription-create'),
            url(r'^filterdescription/edit/(?P<pk>[\d]+)/$', self.filterdescription_update_view.as_view(),
                name='filterdescription-detail'),
            url(r'^filterdescription/delete/(?P<pk>[\d]+)/$', self.filterdescription_delete_view.as_view(),
                name='filterdescription-delete'),
            # text one
            url(r'^textone/$', self.textone_list_view.as_view(),
                name='textone-list'),
            url(r'^textone/add/$', self.textone_create_view.as_view(),
                name='textone-create'),
            url(r'^textone/edit/(?P<pk>[\d]+)/$', self.textone_update_view.as_view(),
                name='textone-detail'),
            url(r'^textone/delete/(?P<pk>[\d]+)/$', self.textone_delete_view.as_view(),
                name='textone-delete'),
            # text two
            url(r'^texttwo/$', self.texttwo_list_view.as_view(),
                name='texttwo-list'),
            url(r'^texttwo/add/$', self.texttwo_create_view.as_view(),
                name='texttwo-create'),
            url(r'^texttwo/edit/(?P<pk>[\d]+)/$', self.texttwo_update_view.as_view(),
                name='texttwo-detail'),
            url(r'^texttwo/delete/(?P<pk>[\d]+)/$', self.texttwo_delete_view.as_view(),
                name='texttwo-delete'),
            # text three
            url(r'^textthree/$', self.textthree_list_view.as_view(),
                name='textthree-list'),
            url(r'^textthree/add/$', self.textthree_create_view.as_view(),
                name='textthree-create'),
            url(r'^textthree/edit/(?P<pk>[\d]+)/$', self.textthree_update_view.as_view(),
                name='textthree-detail'),
            url(r'^textthree/delete/(?P<pk>[\d]+)/$', self.textthree_delete_view.as_view(),
                name='textthree-delete'),
            # text four
            url(r'^textfour/$', self.textfour_list_view.as_view(),
                name='textfour-list'),
            url(r'^textfour/add/$', self.textfour_create_view.as_view(),
                name='textfour-create'),
            url(r'^textfour/edit/(?P<pk>[\d]+)/$', self.textfour_update_view.as_view(),
                name='textfour-detail'),
            url(r'^textfour/delete/(?P<pk>[\d]+)/$', self.textfour_delete_view.as_view(),
                name='textfour-delete'),
            # landing configuration
            url(r'landing_config/$', self.configuration_view.as_view(),
                name='landingconfig-edit'),
            # fuel configuration
            url(r'^fuelconfiguration/$', self.fuel_list_view.as_view(),
                name='fuelconfiguration-list'),
            url(r'^fuelconfiguration/add/$', self.fuel_create_view.as_view(),
                name='fuelconfiguration-create'),
            url(r'^fuelconfiguration/edit/(?P<pk>[\d]+)/$', self.fuel_update_view.as_view(),
                name='fuelconfiguration-detail'),
            url(r'^fuelconfiguration/delete/(?P<pk>[\d]+)/$', self.fuel_delete_view.as_view(),
                name='fuelconfiguration-delete'),
            # benefits
            url(r'^benefit/$', self.benefit_list_view.as_view(),
                name='benefit-list'),
            url(r'^benefit/add/$', self.benefit_create_view.as_view(),
                name='benefit-create'),
            url(r'^benefit/edit/(?P<pk>[\d]+)/$', self.benefit_update_view.as_view(),
                name='benefit-detail'),
            url(r'^benefit/delete/(?P<pk>[\d]+)/$', self.benefit_delete_view.as_view(),
                name='benefit-delete'),
            # overviews
            url(r'^overview/$', self.overview_list_view.as_view(),
                name='overview-list'),
            url(r'^overview/add/$', self.overview_create_view.as_view(),
                name='overview-create'),
            url(r'^overview/edit/(?P<pk>[\d]+)/$', self.overview_update_view.as_view(),
                name='overview-detail'),
            url(r'^overview/delete/(?P<pk>[\d]+)/$', self.overview_delete_view.as_view(),
                name='overview-delete'),
            # reviews
            url(r'^review/$', self.review_list_view.as_view(),
                name='review-list'),
            url(r'^review/add/$', self.review_create_view.as_view(),
                name='review-create'),
            url(r'^review/edit/(?P<pk>[\d]+)/$', self.review_update_view.as_view(),
                name='review-detail'),
            url(r'^review/delete/(?P<pk>[\d]+)/$', self.review_delete_view.as_view(),
                name='review-delete'),
            # deliveries and pays
            url(r'^deliverypay/$', self.deliverypay_list_view.as_view(),
                name='deliverypay-list'),
            url(r'^deliverypay/add/$', self.deliverypay_create_view.as_view(),
                name='deliverypay-create'),
            url(r'^deliverypay/edit/(?P<pk>[\d]+)/$', self.deliverypay_update_view.as_view(),
                name='deliverypay-detail'),
            url(r'^deliverypay/delete/(?P<pk>[\d]+)/$', self.deliverypay_delete_view.as_view(),
                name='deliverypay-delete'),
            # HEADER menu
            url(r'^headermenu/$', self.headermenu_list_view.as_view(),
                name='headermenu-list'),
            url(r'^headermenu/add/$', self.headermenu_create_view.as_view(),
                name='headermenu-create'),
            url(r'^headermenu/edit/(?P<pk>[\d]+)/$', self.headermenu_update_view.as_view(),
                name='headermenu-detail'),
            url(r'^headermenu/delete/(?P<pk>[\d]+)/$', self.headermenu_delete_view.as_view(),
                name='headermenu-delete'),
            # FOOTER menu
            url(r'^footermenu/$', self.footermenu_list_view.as_view(),
                name='footermenu-list'),
            url(r'^footermenu/add/$', self.footermenu_create_view.as_view(),
                name='footermenu-create'),
            url(r'^footermenu/edit/(?P<pk>[\d]+)/$', self.footermenu_update_view.as_view(),
                name='footermenu-detail'),
            url(r'^footermenu/delete/(?P<pk>[\d]+)/$', self.footermenu_delete_view.as_view(),
                name='footermenu-delete'),
            # Menu category
            url(r'^menucategory/$', self.menucategory_list_view.as_view(),
                name='menucategory-list'),
            url(r'^menucategory/add/$', self.menucategory_create_view.as_view(),
                name='menucategory-create'),
            url(r'^menucategory/edit/(?P<pk>[\d]+)/$', self.menucategory_update_view.as_view(),
                name='menucategory-detail'),
            url(r'^menucategory/delete/(?P<pk>[\d]+)/$', self.menucategory_delete_view.as_view(),
                name='menucategory-delete'),
            # SIDE menu
            url(r'^sidemenu/$', self.sidemenu_list_view.as_view(),
                name='sidemenu-list'),
            url(r'^sidemenu/add/$', self.sidemenu_create_view.as_view(),
                name='sidemenu-create'),
            url(r'^sidemenu/edit/(?P<pk>[\d]+)/$', self.sidemenu_update_view.as_view(),
                name='sidemenu-detail'),
            url(r'^sidemenu/delete/(?P<pk>[\d]+)/$', self.sidemenu_delete_view.as_view(),
                name='sidemenu-delete'),
            # Installment payment
            url(r'^installment/$', self.installment_list_view.as_view(),
                name='installment-list'),
            url(r'^installment/add/$', self.installment_create_view.as_view(),
                name='installment-create'),
            url(r'^installment/edit/(?P<pk>[\d]+)/$', self.installment_update_view.as_view(),
                name='installment-detail'),
            url(r'^installment/delete/(?P<pk>[\d]+)/$', self.installment_delete_view.as_view(),
                name='installment-delete'),
            # users
            url(r'^user/$', self.user_list_view.as_view(),
                name='user-list'),
            url(r'^user/add/$', self.user_create_view.as_view(),
                name='user-create'),
            url(r'^user/edit/(?P<pk>[\d]+)/$', self.user_update_view.as_view(),
                name='user-detail'),
            url(r'^user/delete/(?P<pk>[\d]+)/$', self.user_delete_view.as_view(),
                name='user-delete'),
            url(r'user/change_password/$', self.user_change_password_view.as_view(),
                name='user-change-password'),
            # clone product
            url(r'cloneproduct/(?P<pk>[\d]+)/$', self.clone_product_view.as_view(),
                name='clone-product'),
        ]
        return self.post_process_urls(urls)


application = SiteDashboardApplication()
