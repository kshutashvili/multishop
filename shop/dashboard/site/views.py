# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from oscar.core.loading import get_class, get_model

from django.shortcuts import reverse, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.views.generic import (CreateView, ListView,
                                  UpdateView, DeleteView,
                                  TemplateView)
from django.utils.translation import ugettext_lazy as _

from shop.dashboard.site.forms import (SiteForm, SiteConfigForm,
                                       CityForm, PhoneNumbersFormSet,
                                       TimetablesFormSet, SocialRefForm,
                                       FlatPageForm, ContactMessageForm,
                                       SiteContactConfigForm, TimetableForm,
                                       WorkScheduleFormSet, MetaTagForm,
                                       FilterDescriptionForm, TextOneForm,
                                       TextTwoForm, TextThreeForm,
                                       TextFourForm, LandingConfigForm,
                                       FuelConfigurationForm, BenefitItemForm,
                                       OverviewItemForm, ReviewItemForm,
                                       DeliveryAndPayForm, MenuItemForm,
                                       FooterMenuItemForm, MenuCategoryForm,
                                       InstallmentPaymentForm)
from shop.catalogue.models import FilterDescription
from shop.order.models import InstallmentPayment
from config.models import (MetaTag, TextOne, TextTwo, TextThree, TextFour,
                           Configuration, FuelConfiguration, BenefitItem,
                           OverviewItem, ReviewItem, DeliveryAndPay,
                           MenuItem, MenuCategory, SiteConfig)
from contacts.models import (City, SocialNetRef, FlatPage, ContactMessage,
                             Timetable)
from website.views import SiteMultipleObjectMixin

MetaTag = get_model('config', 'MetaTag')
City = get_model('contacts', 'City')
SocialNetRef = get_model('contacts', 'SocialNetRef')
FlatPage = get_model('contacts', 'FlatPage')
ContactMessage = get_model('contacts', 'ContactMessage')
Timetable = get_model('contacts', 'Timetable')
FilterDescription = get_model('catalogue', 'FilterDescription')
SiteForm = get_class('dashboard.site.forms', 'SiteForm')
CityForm = get_class('dashboard.site.forms', 'CityForm')
SiteConfigForm = get_class('dashboard.site.forms', 'SiteConfigForm')
PhoneNumbersFormSet = get_class('dashboard.site.forms', 'PhoneNumbersFormSet')
TimetablesFormSet = get_class('dashboard.site.forms', 'TimetablesFormSet')
SocialRefForm = get_class('dashboard.site.forms', 'SocialRefForm')
FlatPageForm = get_class('dashboard.site.forms', 'FlatPageForm')
ContactMessageForm = get_class('dashboard.site.forms', 'ContactMessageForm')
SiteContactConfigForm = get_class('dashboard.site.forms', 'SiteContactConfigForm')
TimetableForm = get_class('dashboard.site.forms', 'TimetableForm')
WorkScheduleFormSet = get_class('dashboard.site.forms', 'WorkScheduleFormSet')
MetaTagForm = get_class('dashboard.site.forms', 'MetaTagForm')


class SiteCreateView(CreateView):
    model = Site
    form_class = SiteForm
    template_name = 'shop/dashboard/site/site.html'

    def get_context_data(self, **kwargs):
        context = super(SiteCreateView, self).get_context_data(**kwargs)
        context['title'] = _('Create Site')
        if self.request.POST:
            context['site_config_form'] = SiteConfigForm(self.request.POST,
                                                         self.request.FILES)
        else:
            context['site_config_form'] = SiteConfigForm()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        site_config = context['site_config_form']
        self.object = form.save()
        site_config.instance = self.object.config

        if site_config.is_valid():
            site_config.save()

        return super(SiteCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('dashboard:index')


class SiteUpdateView(UpdateView):
    template_name = 'shop/dashboard/site/site_detail.html'
    model = Site
    form_class = SiteForm

    def get_context_data(self, **kwargs):
        context = super(SiteUpdateView, self).get_context_data(**kwargs)
        context['title'] = _("Изменение сайта")
        if self.request.POST:
            context['site_config_form'] = SiteConfigForm(self.request.POST,
                                                         self.request.FILES)
        else:
            current_site = get_current_site(self.request)
            current_site_config = SiteConfig.objects.get(site=current_site)
            context['site_config_form'] = SiteConfigForm(instance=current_site_config)
        return context

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Сайт успешно изменен"))
        return reverse('dashboard:index')

    def form_valid(self, form):
        context = self.get_context_data()
        site_config = context['site_config_form']
        self.object = form.save()
        site_config.instance = self.object.config

        if site_config.is_valid():
            site_config.save()

        return super(SiteUpdateView, self).form_valid(form)


class CityListView(SiteMultipleObjectMixin, ListView):

    model = City
    context_object_name = 'cities'
    template_name = 'shop/dashboard/site/city_list.html'


class CityCreateUpdateView(UpdateView):
    model = City
    context_object_name = 'city'
    form_class = CityForm
    phone_numbers_formset = PhoneNumbersFormSet
    timetables_formset = TimetablesFormSet
    template_name = 'shop/dashboard/site/city_detail.html'

    def process_all_forms(self, form):
        if self.creating and form.is_valid():
            # the object will be needed by formsets
            self.object = form.save(commit=False)
            self.object.site = get_current_site(self.request)

        phone_numbers_formset = self.phone_numbers_formset(
            self.request.POST, self.request.FILES, instance=self.object)
        timetables_formset = self.timetables_formset(
            self.request.POST, self.request.FILES, instance=self.object
        )

        is_valid = (form.is_valid() and phone_numbers_formset.is_valid()
                    and timetables_formset.is_valid())

        if is_valid:
            return self.forms_valid(form,
                                    phone_numbers_formset,
                                    timetables_formset)
        else:
            return self.forms_invalid(form,
                                      phone_numbers_formset,
                                      timetables_formset)

    def forms_valid(self, form, phone_numbers_formset, timetables_formset):
        form.save()
        phone_numbers_formset.save()
        timetables_formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, phone_numbers_formset, timetables_formset):
        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"
                         ))
        ctx = self.get_context_data(form=form,
                                    phone_numbers_formset=phone_numbers_formset,
                                    work_schedules_formset=timetables_formset)
        return self.render_to_response(ctx)

    form_valid = form_invalid = process_all_forms

    def get_context_data(self, *args, **kwargs):
        ctx = super(CityCreateUpdateView, self).get_context_data(
            *args, **kwargs)

        if "phone_numbers_formset" not in ctx:
            ctx["phone_numbers_formset"] = self.phone_numbers_formset(
                instance=self.object)

        if "timetables_formset" not in ctx:
            ctx["timetables_formset"] = self.timetables_formset(
                instance=self.object)

        ctx["title"] = self.get_title()

        return ctx


class CityUpdateView(CityCreateUpdateView):
    creating = False

    def get_title(self):
        return _("Update city '%s'") % self.object.city_name

    def get_success_url(self):
        messages.info(self.request, _("City updated successfully"))
        return reverse("dashboard:city-list")

    def get_object(self):
        city = get_object_or_404(City, pk=self.kwargs['pk'])
        return city


class CityCreateView(CityCreateUpdateView):
    creating = True

    def get_object(self):
        return None

    def get_title(self):
        return _("Add a new city")

    def get_success_url(self):
        messages.info(self.request, _("City created successfully"))
        return reverse("dashboard:city-list")


class CityDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/city_delete.html'
    model = City
    form_class = CityForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(CityDeleteView, self).get_context_data(*args,
                                                           **kwargs)
        ctx['title'] = _("Delete city '%s'") % self.object.city_name
        return ctx

    def get_success_url(self):
        messages.info(self.request, _("City deleted successfully"))
        return reverse("dashboard:city-list")


class SocialNetRefListView(SiteMultipleObjectMixin, ListView):

    model = SocialNetRef
    context_object_name = 'social_refs'
    template_name = 'shop/dashboard/site/socialref_list.html'


class SocialNetRefCreateUpdateView(UpdateView):
    model = SocialNetRef
    context_object_name = 'social_ref'
    form_class = SocialRefForm
    template_name = 'shop/dashboard/site/socialref_detail.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.creating:
            obj.site = get_current_site(self.request)

        obj.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        ctx = super(SocialNetRefCreateUpdateView, self).get_context_data(
            *args, **kwargs)

        ctx["title"] = self.get_title()

        return ctx


class SocialNetRefUpdateView(SocialNetRefCreateUpdateView):
    creating = False

    def get_title(self):
        return _("Update social reference '%s'") % self.object.ref_type

    def get_success_url(self):
        messages.info(self.request, _("Social reference updated successfully"))
        return reverse("dashboard:socialref-list")

    def get_object(self):
        obj = get_object_or_404(SocialNetRef, pk=self.kwargs['pk'])
        return obj


class SocialNetRefCreateView(SocialNetRefCreateUpdateView):
    creating = True

    def get_object(self):
        return None

    def get_title(self):
        return _("Add a new social reference")

    def get_success_url(self):
        messages.info(self.request, _("Social reference created successfully"))
        return reverse("dashboard:socialref-list")


class SocialNetRefDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/socialref_delete.html'
    model = SocialNetRef
    form_class = SocialRefForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(SocialNetRefDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Delete social reference '%s'") % self.object.ref_type

        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Social reference deleted successfully"))
        return reverse("dashboard:socialref-list")


class FlatPageListView(SiteMultipleObjectMixin, ListView):

    model = FlatPage
    context_object_name = 'flat_pages'
    template_name = 'shop/dashboard/site/flatpage_list.html'


class FlatPageCreateView(CreateView):
    model = FlatPage
    context_object_name = 'flat_page'
    form_class = FlatPageForm
    template_name = 'shop/dashboard/site/flatpage_detail.html'

    def get_object(self):
        return None

    def get_success_url(self):
        messages.info(self.request, _("Flat page created successfully"))
        return reverse("dashboard:flatpage-list")


    def get_context_data(self, **kwargs):
        ctx = super(FlatPageCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать статическую страницу')
        return ctx


class FlatPageUpdateView(UpdateView):
    model = FlatPage
    context_object_name = 'flat_page'
    form_class = FlatPageForm
    template_name = 'shop/dashboard/site/flatpage_detail.html'

    def get_success_url(self):
        messages.info(self.request, _("Flat page updated successfully"))
        return reverse("dashboard:flatpage-list")

    def get_object(self):
        obj = get_object_or_404(FlatPage, pk=self.kwargs['pk'])
        return obj

    def get_context_data(self, **kwargs):
        ctx = super(FlatPageUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object
        return ctx


class FlatPageDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/flatpage_delete.html'
    model = FlatPage
    form_class = FlatPageForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(FlatPageDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление статической страницы '%s'") % self.object.title

        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Статическая страница успешно изменена"))
        return reverse("dashboard:flatpage-list")


class ContactMessageListView(SiteMultipleObjectMixin, ListView):

    model = ContactMessage
    context_object_name = 'contact_messages'
    template_name = 'shop/dashboard/site/contactmessage_list.html'


class ContactMessageUpdateView(UpdateView):
    model = ContactMessage
    context_object_name = 'contact_message'
    form_class = ContactMessageForm
    template_name = 'shop/dashboard/site/contactmessage_detail.html'

    def get_success_url(self):
        messages.info(self.request, _("Contact message updated successfully"))
        return reverse("dashboard:contactmessage-list")

    def get_object(self):
        obj = get_object_or_404(ContactMessage, pk=self.kwargs['pk'])
        return obj


class ContactMessageDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/contactmessage_delete.html'
    model = ContactMessage
    form_class = ContactMessageForm

    def get_success_url(self):
        messages.info(self.request, _("Contact message deleted successfully"))
        return reverse("dashboard:contactmessage-list")


class SiteContactConfigView(TemplateView):
    template_name = 'shop/dashboard/site/contacts_config.html'

    def get_context_data(self, **kwargs):
        ctx = super(SiteContactConfigView, self).get_context_data(**kwargs)

        ctx['form'] = SiteContactConfigForm(request=self.request)
        ctx['formset'] = WorkScheduleFormSet(instance=get_current_site(self.request))
        return ctx

    def post(self, request):

        form = SiteContactConfigForm(request.POST, request=request)
        formset = WorkScheduleFormSet(request.POST,
                                      instance=get_current_site(request))

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

        return HttpResponseRedirect(reverse('dashboard:sitecontact-edit'))


class TimetableListView(ListView):

    model = Timetable
    context_object_name = 'timetables'
    template_name = 'shop/dashboard/site/timetable_list.html'

    def get_queryset(self):
        return Timetable.objects.filter(city__isnull=True)


class TimetableCreateUpdateView(UpdateView):
    model = Timetable
    context_object_name = 'timetable'
    form_class = TimetableForm
    template_name = 'shop/dashboard/site/timetable_detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(TimetableCreateUpdateView, self).get_context_data(
            *args, **kwargs)

        ctx["title"] = self.get_title()

        return ctx


class TimetableUpdateView(TimetableCreateUpdateView):

    def get_title(self):
        return _("Update timetable '%s'") % self.object

    def get_success_url(self):
        messages.info(self.request, _("Timetable updated successfully"))
        return reverse("dashboard:timetable-list")

    def get_object(self):
        obj = get_object_or_404(Timetable, pk=self.kwargs['pk'])
        return obj


class TimetableCreateView(TimetableCreateUpdateView):

    def get_object(self):
        return None

    def get_title(self):
        return _("Add a new timetable")

    def get_success_url(self):
        messages.info(self.request, _("Timetable created successfully"))
        return reverse("dashboard:timetable-list")


class TimetableDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/timetable_delete.html'
    model = Timetable
    form_class = TimetableForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(TimetableDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Delete timetable '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Timetable deleted successfully"))
        return reverse("dashboard:timetable-list")


class MetaTagListView(ListView):

    model = MetaTag
    context_object_name = 'meta_tags'
    template_name = 'shop/dashboard/site/metatag_list.html'


class MetaTagCreateUpdateView(UpdateView):
    model = Timetable
    context_object_name = 'meta_tag'
    form_class = MetaTagForm
    template_name = 'shop/dashboard/site/metatag_detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(MetaTagCreateUpdateView, self).get_context_data(
            *args, **kwargs)

        ctx["title"] = self.get_title()

        return ctx


class MetaTagUpdateView(MetaTagCreateUpdateView):

    def get_title(self):
        return _("Update meta tag '%s'") % self.object

    def get_success_url(self):
        messages.info(self.request, _("Meta tag updated successfully"))
        return reverse("dashboard:metatag-list")

    def get_object(self):
        obj = get_object_or_404(MetaTag, pk=self.kwargs['pk'])
        return obj


class MetaTagCreateView(MetaTagCreateUpdateView):

    def get_object(self):
        return None

    def get_title(self):
        return _("Add a new meta tag")

    def get_success_url(self):
        messages.info(self.request, _("Meta tag created successfully"))
        return reverse("dashboard:metatag-list")


class MetaTagDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/metatag_delete.html'
    model = MetaTag
    form_class = MetaTagForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(MetaTagDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Delete meta tag '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Meta tag deleted successfully"))
        return reverse("dashboard:metatag-list")


class FilterDescriptionListView(ListView):
    model = FilterDescription
    context_object_name = 'filter_descriptions'
    template_name = 'shop/dashboard/site/filterdescription_list.html'


class FilterDescriptionCreateView(CreateView):
    template_name = 'shop/dashboard/site/filterdescription_detail.html'
    model = FilterDescription
    form_class = FilterDescriptionForm
    context_object_name = 'filter_description'

    def get_context_data(self, **kwargs):
        ctx = super(FilterDescriptionCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Create New Filter Description')
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Filter Description created successfully"))
        return reverse('dashboard:filterdescription-list')

    def get_object(self):
        return None


class FilterDescriptionUpdateView(UpdateView):
    template_name = 'shop/dashboard/site/filterdescription_detail.html'
    model = FilterDescription
    form_class = FilterDescriptionForm
    context_object_name = 'filter_description'

    def get_context_data(self, **kwargs):
        ctx = super(FilterDescriptionUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.title
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Filter Description updated successfully"))
        return reverse('dashboard:filterdescription-list')


class FilterDescriptionDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/filterdescription_delete.html'
    model = FilterDescription

    def get_context_data(self, *args, **kwargs):
        ctx = super(FilterDescriptionDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Delete filter description for '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Deleted filter description '%s'") % self.object.title)
        return reverse('dashboard:filterdescription-list')


class TextOneListView(SiteMultipleObjectMixin, ListView):
    model = TextOne
    context_object_name = 'text_obj'
    template_name = 'shop/dashboard/site/textobj_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(TextOneListView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый Текст 1')
        ctx['text_one'] = True
        ctx['text_two'] = False
        ctx['text_three'] = False
        ctx['text_four'] = False
        return ctx


class TextOneCreateView(CreateView):
    template_name = 'shop/dashboard/site/textobj_detail.html'
    model = TextOne
    form_class = TextOneForm
    context_object_name = 'text_obj'
    creating = True

    def get_context_data(self, **kwargs):
        ctx = super(TextOneCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый Текст 1')
        ctx['text_one'] = True
        ctx['text_two'] = False
        ctx['text_three'] = False
        ctx['text_four'] = False
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Текст 1 успешно создан"))
        return reverse('dashboard:textone-list')

    def get_object(self):
        return None

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.creating:
            obj.site = get_current_site(self.request)

        obj.save()

        return HttpResponseRedirect(self.get_success_url())


class TextOneUpdateView(UpdateView):
    template_name = 'shop/dashboard/site/textobj_detail.html'
    model = TextOne
    form_class = TextOneForm
    context_object_name = 'text_obj'

    def get_context_data(self, **kwargs):
        ctx = super(TextOneUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.text
        ctx['text_one'] = True
        ctx['text_two'] = False
        ctx['text_three'] = False
        ctx['text_four'] = False
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Текст 1 успешно изменен"))
        return reverse('dashboard:textone-list')


class TextOneDeleteView(DeleteView):
    model = TextOne
    template_name = 'shop/dashboard/site/textobj_delete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(TextOneDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление Текста 1 '%s'") % self.object
        ctx['text_one'] = True
        ctx['text_two'] = False
        ctx['text_three'] = False
        ctx['text_four'] = False
        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Текст 1 '%s' удален") % self.object.text)
        return reverse('dashboard:textone-list')


class TextTwoListView(TextOneListView):
    model = TextTwo

    def get_context_data(self, **kwargs):
        ctx = super(TextTwoListView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый Текст 2')
        ctx['text_one'] = False
        ctx['text_two'] = True
        ctx['text_three'] = False
        ctx['text_four'] = False
        return ctx


class TextTwoCreateView(TextOneCreateView):
    model = TextTwo
    form_class = TextTwoForm

    def get_context_data(self, **kwargs):
        ctx = super(TextTwoCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый Текст 2')
        ctx['text_one'] = False
        ctx['text_two'] = True
        ctx['text_three'] = False
        ctx['text_four'] = False
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Текст 2 успешно создан"))
        return reverse('dashboard:texttwo-list')


class TextTwoUpdateView(TextOneUpdateView):
    model = TextTwo
    form_class = TextTwoForm

    def get_context_data(self, **kwargs):
        ctx = super(TextTwoUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.text
        ctx['text_one'] = False
        ctx['text_two'] = True
        ctx['text_three'] = False
        ctx['text_four'] = False
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Текст 2 успешно изменен"))
        return reverse('dashboard:texttwo-list')


class TextTwoDeleteView(DeleteView):
    model = TextTwo
    template_name = 'shop/dashboard/site/textobj_delete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(TextTwoDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление Текста 2 '%s'") % self.object
        ctx['text_one'] = False
        ctx['text_two'] = True
        ctx['text_three'] = False
        ctx['text_four'] = False
        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Текст 2 '%s' успешно удален") % self.object)
        return reverse('dashboard:texttwo-list')


class TextThreeListView(TextOneListView):
    model = TextThree

    def get_context_data(self, **kwargs):
        ctx = super(TextThreeListView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый Текст 3')
        ctx['text_one'] = False
        ctx['text_two'] = False
        ctx['text_three'] = True
        ctx['text_four'] = False
        return ctx


class TextThreeCreateView(TextOneCreateView):
    model = TextThree
    form_class = TextThreeForm

    def get_context_data(self, **kwargs):
        ctx = super(TextThreeCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый Текст 3')
        ctx['text_one'] = False
        ctx['text_two'] = False
        ctx['text_three'] = True
        ctx['text_four'] = False
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Текст 3 успешно создан"))
        return reverse('dashboard:textthree-list')


class TextThreeUpdateView(TextOneUpdateView):
    model = TextThree
    form_class = TextThreeForm

    def get_context_data(self, **kwargs):
        ctx = super(TextThreeUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.text
        ctx['text_one'] = False
        ctx['text_two'] = False
        ctx['text_three'] = True
        ctx['text_four'] = False
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Текст 3 успешно изменен"))
        return reverse('dashboard:textthree-list')


class TextThreeDeleteView(DeleteView):
    model = TextThree
    template_name = 'shop/dashboard/site/textobj_delete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(TextThreeDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление Текста 3 '%s'") % self.object
        ctx['text_one'] = False
        ctx['text_two'] = False
        ctx['text_three'] = True
        ctx['text_four'] = False
        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Текст 3 '%s' удален") % self.object)
        return reverse('dashboard:textthree-list')


class TextFourListView(TextOneListView):
    model = TextFour

    def get_context_data(self, **kwargs):
        ctx = super(TextFourListView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый Текст 4')
        ctx['text_one'] = False
        ctx['text_two'] = False
        ctx['text_three'] = False
        ctx['text_four'] = True
        return ctx


class TextFourCreateView(TextOneCreateView):
    model = TextFour
    form_class = TextFourForm

    def get_context_data(self, **kwargs):
        ctx = super(TextFourCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('создать новый текст 4')
        ctx['text_one'] = False
        ctx['text_two'] = False
        ctx['text_three'] = False
        ctx['text_four'] = True
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Текст 4 успешно создан"))
        return reverse('dashboard:textfour-list')


class TextFourUpdateView(TextOneUpdateView):
    model = TextFour
    form_class = TextFourForm

    def get_context_data(self, **kwargs):
        ctx = super(TextFourUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.text
        ctx['text_one'] = False
        ctx['text_two'] = False
        ctx['text_three'] = False
        ctx['text_four'] = True
        return ctx

    def get_success_url(self):
        messages.success(self.request, _("Текст 4 успешно обновлен"))
        return reverse('dashboard:textfour-list')


class TextFourDeleteView(DeleteView):
    model = TextFour
    template_name = 'shop/dashboard/site/textobj_delete.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(TextFourDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление Текста 4 '%s'") % self.object
        ctx['text_one'] = False
        ctx['text_two'] = False
        ctx['text_three'] = False
        ctx['text_four'] = True
        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Текст 4 удален '%s'") % self.object)
        return reverse('dashboard:textfour-list')


class LandingConfigView(UpdateView):
    template_name = 'shop/dashboard/site/landingconfig_edit.html'
    model = Configuration
    form_class = LandingConfigForm

    def get_context_data(self, **kwargs):
        ctx = super(LandingConfigView, self).get_context_data(**kwargs)
        obj = Configuration.get_solo()
        form = LandingConfigForm(instance=obj)
        curr_site = get_current_site(self.request)
        form.fields['footer_map_for'].queryset = form.fields['footer_map_for'].queryset.filter(site=curr_site)
        ctx['form'] = form
        return ctx

    def get_object(self, *args, **kwargs):
        obj = self.model.get_solo()
        return obj

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.site = get_current_site(self.request)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Лэндинг обновлен"))
        return reverse('dashboard:index')


class FuelConfigurationListView(ListView):
    model = FuelConfiguration
    context_object_name = 'fuel_configuration'
    template_name = 'shop/dashboard/site/fuelconfiguration_list.html'


class FuelConfigurationCreateView(CreateView):
    template_name = 'shop/dashboard/site/fuelconfiguration_detail.html'
    model = FuelConfiguration
    form_class = FuelConfigurationForm
    context_object_name = 'fuel_configuration'

    def get_context_data(self, **kwargs):
        ctx = super(FuelConfigurationCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новую цену на топливо')
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.config = Configuration.get_solo()
        obj.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Цена на топливо успешно создана"))
        return reverse('dashboard:fuelconfiguration-list')

    def get_object(self):
        return None


class FuelConfigurationUpdateView(UpdateView):
    template_name = 'shop/dashboard/site/fuelconfiguration_detail.html'
    model = FuelConfiguration
    form_class = FuelConfigurationForm
    context_object_name = 'fuel_configuration'

    def get_context_data(self, **kwargs):
        ctx = super(FuelConfigurationUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.fuel_type
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Цена на топливо успешно изменена"))
        return reverse('dashboard:fuelconfiguration-list')


class FuelConfigurationDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/fuelconfiguration_delete.html'
    model = FuelConfiguration

    def get_context_data(self, *args, **kwargs):
        ctx = super(FuelConfigurationDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление цены '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Удалена цена для '%s'") % self.object)
        return reverse('dashboard:fuelconfiguration-list')


class BenefitItemListView(ListView):
    model = BenefitItem
    context_object_name = 'benefits'
    template_name = 'shop/dashboard/site/benefit_list.html'


class BenefitItemCreateView(CreateView):
    template_name = 'shop/dashboard/site/benefit_detail.html'
    model = BenefitItem
    form_class = BenefitItemForm
    context_object_name = 'benefit'

    def get_context_data(self, **kwargs):
        ctx = super(BenefitItemCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новое Преимущество')
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.config = Configuration.get_solo()
        obj.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Преимущество успешно создана"))
        return reverse('dashboard:benefit-list')

    def get_object(self):
        return None


class BenefitItemUpdateView(UpdateView):
    template_name = 'shop/dashboard/site/benefit_detail.html'
    model = BenefitItem
    form_class = BenefitItemForm
    context_object_name = 'benefit'

    def get_context_data(self, **kwargs):
        ctx = super(BenefitItemUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.text
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Преимущество успешно изменено"))
        return reverse('dashboard:benefit-list')


class BenefitItemDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/benefit_delete.html'
    model = BenefitItem

    def get_context_data(self, *args, **kwargs):
        ctx = super(BenefitItemDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление преимущества '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Удалено преимущество '%s'") % self.object)
        return reverse('dashboard:benefit-list')


class OverviewItemListView(ListView):
    model = OverviewItem
    context_object_name = 'overviews'
    template_name = 'shop/dashboard/site/overview_list.html'


class OverviewItemCreateView(CreateView):
    template_name = 'shop/dashboard/site/overview_detail.html'
    model = OverviewItem
    form_class = OverviewItemForm
    context_object_name = 'overview'

    def get_context_data(self, **kwargs):
        ctx = super(OverviewItemCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый Обзор')
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.config = Configuration.get_solo()
        obj.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Обзор успешно создана"))
        return reverse('dashboard:overview-list')

    def get_object(self):
        return None


class OverviewItemUpdateView(UpdateView):
    template_name = 'shop/dashboard/site/overview_detail.html'
    model = OverviewItem
    form_class = OverviewItemForm
    context_object_name = 'overview'

    def get_context_data(self, **kwargs):
        ctx = super(OverviewItemUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.link
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Обзор успешно изменен"))
        return reverse('dashboard:overview-list')


class OverviewItemDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/overview_delete.html'
    model = OverviewItem

    def get_context_data(self, *args, **kwargs):
        ctx = super(OverviewItemDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление обзора '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Обзор '%s' удален") % self.object)
        return reverse('dashboard:overview-list')


class ReviewItemListView(ListView):
    model = ReviewItem
    context_object_name = 'reviews'
    template_name = 'shop/dashboard/site/review_list.html'


class ReviewItemCreateView(CreateView):
    template_name = 'shop/dashboard/site/review_detail.html'
    model = ReviewItem
    form_class = ReviewItemForm
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        ctx = super(ReviewItemCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый Отзыв')
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.config = Configuration.get_solo()
        obj.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Отзыв успешно создана"))
        return reverse('dashboard:review-list')

    def get_object(self):
        return None


class ReviewItemUpdateView(UpdateView):
    template_name = 'shop/dashboard/site/review_detail.html'
    model = ReviewItem
    form_class = ReviewItemForm
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        ctx = super(ReviewItemUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.name
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Отзыв успешно изменен"))
        return reverse('dashboard:review-list')


class ReviewItemDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/review_delete.html'
    model = ReviewItem

    def get_context_data(self, *args, **kwargs):
        ctx = super(ReviewItemDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление отзыва '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Отзыв '%s' удален") % self.object)
        return reverse('dashboard:review-list')


class DeliveryAndPayListView(ListView):
    model = DeliveryAndPay
    template_name = "shop/dashboard/site/deliverypay_list.html"
    context_object_name = 'deliveries'


class DeliveryAndPayCreateView(CreateView):
    model = DeliveryAndPay
    form_class = DeliveryAndPayForm
    template_name = "shop/dashboard/site/deliverypay_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(DeliveryAndPayCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новую запись о Доставке/Оплате')
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.config = Configuration.get_solo()
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Запись о Доставке/Оплате успешно создана"))
        return reverse('dashboard:deliverypay-list')

    def get_object(self):
        return None


class DeliveryAndPayUpdateView(UpdateView):
    model = DeliveryAndPay
    form_class = DeliveryAndPayForm
    template_name = "shop/dashboard/site/deliverypay_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(DeliveryAndPayUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.title
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Запись о Доставке/Оплате успешно изменена"))
        return reverse('dashboard:deliverypay-list')


class DeliveryAndPayDeleteview(DeleteView):
    model = DeliveryAndPay
    template_name = "shop/dashboard/site/deliverypay_delete.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(DeliveryAndPayDeleteview, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление Записи '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Запись '%s' удалена") % self.object)
        return reverse('dashboard:deliverypay-list')


class HeaderMenuListView(SiteMultipleObjectMixin, ListView):
    model = MenuItem
    template_name = "shop/dashboard/site/headermenu_list.html"
    context_object_name = 'header_menu'
    queryset = MenuItem.objects.in_header()


class HeaderMenuCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "shop/dashboard/site/headermenu_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(HeaderMenuCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый пункт меню')
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.site = get_current_site(self.request)
        obj.position = MenuItem.POSITION.HEADER
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Новый пункт меню создан"))
        return reverse('dashboard:headermenu-list')

    def get_object(self):
        return None


class HeaderMenuUpdateView(UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "shop/dashboard/site/headermenu_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(HeaderMenuUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.name
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Пункт меню успешно изменен"))
        return reverse('dashboard:headermenu-list')


class HeaderMenuDeleteView(DeleteView):
    model = MenuItem
    template_name = "shop/dashboard/site/headermenu_delete.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(HeaderMenuDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление пункта меню '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Пункт меню '%s' удален") % self.object)
        return reverse('dashboard:headermenu-list')


class FooterMenuListView(SiteMultipleObjectMixin, ListView):
    model = MenuItem
    template_name = "shop/dashboard/site/footermenu_list.html"
    context_object_name = 'footer_menu'
    queryset = MenuItem.objects.in_footer()


class FooterMenuCreateView(CreateView):
    model = MenuItem
    form_class = FooterMenuItemForm
    template_name = "shop/dashboard/site/footermenu_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(FooterMenuCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый пункт меню')
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.site = get_current_site(self.request)
        obj.position = MenuItem.POSITION.FOOTER
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Новый пункт меню создан"))
        return reverse('dashboard:footermenu-list')

    def get_object(self):
        return None


class FooterMenuUpdateView(UpdateView):
    model = MenuItem
    form_class = FooterMenuItemForm
    template_name = "shop/dashboard/site/footermenu_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(FooterMenuUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.name
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Пункт меню успешно изменен"))
        return reverse('dashboard:footermenu-list')


class FooterMenuDeleteView(DeleteView):
    model = MenuItem
    template_name = "shop/dashboard/site/footermenu_delete.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(FooterMenuDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление пункта меню '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Пункт меню '%s' удален") % self.object)
        return reverse('dashboard:footermenu-list')


class MenuCategoryListView(ListView):
    model = MenuCategory
    template_name = "shop/dashboard/site/menucategory_list.html"
    context_object_name = 'menu_categories'


class MenuCategoryCreateView(CreateView):
    model = MenuCategory
    form_class = MenuCategoryForm
    template_name = "shop/dashboard/site/menucategory_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(MenuCategoryCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новую категорию меню')
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        #obj.site = get_current_site(self.request)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Новая категория меню создана"))
        return reverse('dashboard:menucategory-list')

    def get_object(self):
        return None


class MenuCategoryUpdateView(UpdateView):
    model = MenuCategory
    form_class = MenuCategoryForm
    template_name = "shop/dashboard/site/menucategory_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(MenuCategoryUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.name
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Категория меню успешно изменена"))
        return reverse('dashboard:menucategory-list')


class MenuCategoryDeleteView(DeleteView):
    model = MenuCategory
    template_name = "shop/dashboard/site/menucategory_delete.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(MenuCategoryDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление категории меню '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Категория меню '%s' удалена") % self.object)
        return reverse('dashboard:menucategory-list')


class SideMenuListView(SiteMultipleObjectMixin, ListView):
    model = MenuItem
    template_name = "shop/dashboard/site/sidemenu_list.html"
    context_object_name = 'side_menu'
    queryset = MenuItem.objects.in_side()


class SideMenuCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "shop/dashboard/site/sidemenu_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(SideMenuCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новый пункт меню')
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.site = get_current_site(self.request)
        obj.position = MenuItem.POSITION.SIDE
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Новый пункт меню создан"))
        return reverse('dashboard:sidemenu-list')

    def get_object(self):
        return None


class SideMenuUpdateView(UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "shop/dashboard/site/sidemenu_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(SideMenuUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.name
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Пункт меню успешно изменен"))
        return reverse('dashboard:sidemenu-list')


class SideMenuDeleteView(DeleteView):
    model = MenuItem
    template_name = "shop/dashboard/site/sidemenu_delete.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(SideMenuDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление пункта меню '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Пункт меню '%s' удален") % self.object)
        return reverse('dashboard:sidemenu-list')


class InstallmentPaymentListView(SiteMultipleObjectMixin, ListView):
    model = InstallmentPayment
    template_name = "shop/dashboard/site/installment_list.html"
    context_object_name = 'installments'


class InstallmentPaymentCreateView(CreateView):
    model = InstallmentPayment
    form_class = InstallmentPaymentForm
    template_name = "shop/dashboard/site/installment_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(InstallmentPaymentCreateView, self).get_context_data(**kwargs)
        ctx['title'] = _('Создать новую рассрочку')
        return ctx

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.site = get_current_site(self.request)
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, _("Новый рассрочка создана"))
        return reverse('dashboard:installment-list')

    def get_object(self):
        return None


class InstallmentPaymentUpdateView(UpdateView):
    model = InstallmentPayment
    form_class = InstallmentPaymentForm
    template_name = "shop/dashboard/site/installment_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(InstallmentPaymentUpdateView, self).get_context_data(**kwargs)
        ctx['title'] = self.object.phone
        return ctx

    def get_object(self):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return obj

    def get_success_url(self):
        messages.success(self.request, _("Рассрочка успешно изменена"))
        return reverse('dashboard:installment-list')


class InstallmentPaymentDeleteView(DeleteView):
    model = InstallmentPayment
    template_name = "shop/dashboard/site/installment_delete.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(InstallmentPaymentDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Удаление рассрочки '%s'") % self.object

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, _("Пункт меню '%s' удален") % self.object)
        return reverse('dashboard:installment-list')