# -*- coding: utf-8 -*-

from django import forms
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.sites.models import Site
from config.models import SiteConfig
from contacts.models import (City, PhoneNumber,
                             Timetable, SocialNetRef,
                             FlatPage, ContactMessage,
                             WorkSchedule)
from django.forms.models import inlineformset_factory
from ckeditor.widgets import CKEditorWidget


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'


class SiteConfigForm(forms.ModelForm):

    class Meta:
        model = SiteConfig
        exclude = ('site', )


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ('city_name_ru', 'city_name_uk',
                  'slug', 'address_ru', 'address_uk',
                  'google_maps_api_key')


class PhoneNumbersForm(forms.ModelForm):

    class Meta:
        model = PhoneNumber
        exclude = ('site', )


class TimetableForm(forms.ModelForm):

    class Meta:
        model = Timetable
        fields = ('weekdays_ru', 'weekdays_uk',
                  'daytime_ru', 'daytime_uk',
                  )

PhoneNumbersFormSet = inlineformset_factory(City,
                                            PhoneNumber,
                                            form=PhoneNumbersForm,
                                            extra=3)

TimetablesFormSet = inlineformset_factory(City,
                                          Timetable,
                                          form=TimetableForm,
                                          extra=3)


class SocialRefForm(forms.ModelForm):

    class Meta:
        model = SocialNetRef
        exclude = ('site', )


class FlatPageForm(forms.ModelForm):

    content_ru = forms.CharField(label='Содержание (на русском)', widget=CKEditorWidget())
    content_uk = forms.CharField(label='Зміст (українською)', widget=CKEditorWidget())

    class Meta:
        model = FlatPage
        fields = ('title_ru', 'title_uk',
                  'content_ru', 'content_uk',
                  'slug_ru', 'slug_uk')


class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = ContactMessage
        exclude = ('site', )


class SiteContactConfigForm(forms.Form):
    kievstar = forms.CharField(max_length=20,
                               validators=[PhoneNumber.phone_regex],
                               required=False)
    vodafone = forms.CharField(max_length=20,
                               validators=[PhoneNumber.phone_regex],
                               required=False)
    life = forms.CharField(max_length=20,
                           validators=[PhoneNumber.phone_regex],
                           required=False)

    email = forms.EmailField()

    def __init__(self, *args, **kwargs):

        # set initial values
        self.site = get_current_site(kwargs.pop('request'))
        phone_numbers = PhoneNumber.objects.filter(site=self.site)

        if 'initial' not in kwargs:
            kwargs['initial'] = {}

        initial = kwargs['initial']

        for number in phone_numbers:
            initial[number.operator] = number.phone

        initial['email'] = self.site.config.email

        super(SiteContactConfigForm, self).__init__(*args, **kwargs)

    def save(self):

        operator_choices = dict(PhoneNumber.OPERATOR._CHOICES)

        phone_numbers = [key
                         for key in self.changed_data
                         if key in operator_choices]

        for key in phone_numbers:
            PhoneNumber.objects.filter(site=self.site,
                                       operator=key,
                                       city__isnull=True).delete()

            phone = self.cleaned_data.get(key)

            if phone:
                number = PhoneNumber(operator=key,
                                     phone=phone,
                                     site=self.site)
                number.save()

        if 'email' in self.changed_data:
            config_obj = self.site.config
            config_obj.email = self.cleaned_data['email']
            config_obj.save()


class WorkScheduleForm(forms.ModelForm):

    timetable = forms.ModelMultipleChoiceField(queryset=Timetable.objects.filter(
        city__isnull=True
    ))

    class Meta:
        model = WorkSchedule
        fields = ('schedule_type', 'timetable')

WorkScheduleFormSet = inlineformset_factory(Site,
                                            WorkSchedule,
                                            form=WorkScheduleForm,
                                            extra=1)
