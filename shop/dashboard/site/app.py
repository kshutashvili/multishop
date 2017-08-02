from django.conf.urls import url
from oscar.core.application import Application

from shop.dashboard.site.views import (SiteCreateView, CityListView,
                                       CityUpdateView, CityCreateView,
                                       CityDeleteView,
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
                                       TimetableDeleteView)


class SiteDashboardApplication(Application):
    name = None
    default_permissions = ['is_staff', ]

    site_create_view = SiteCreateView
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

    def get_urls(self):
        urls = [
            url(r'^add/$', self.site_create_view.as_view(),
                name='site-add'),
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
            url(r'^flatpage/add/$', self.flatpage_list_view.as_view(),
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

        ]
        return self.post_process_urls(urls)


application = SiteDashboardApplication()
