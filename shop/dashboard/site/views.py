from django.shortcuts import reverse, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
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
                                       FilterDescriptionForm)
from django.contrib.sites.models import Site
from oscar.core.loading import get_class, get_model
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


class FlatPageCreateUpdateView(UpdateView):
    model = FlatPage
    context_object_name = 'flat_page'
    form_class = FlatPageForm
    template_name = 'shop/dashboard/site/flatpage_detail.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        if self.creating:
            obj.site = get_current_site(self.request)

        obj.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        ctx = super(FlatPageCreateUpdateView, self).get_context_data(
            *args, **kwargs)

        ctx["title"] = self.get_title()

        return ctx


class FlatPageUpdateView(FlatPageCreateUpdateView):
    creating = False

    def get_title(self):
        return _("Update flat page '%s'") % self.object.title

    def get_success_url(self):
        messages.info(self.request, _("Flat page updated successfully"))
        return reverse("dashboard:flatpage-list")

    def get_object(self):
        obj = get_object_or_404(FlatPage, pk=self.kwargs['pk'])
        return obj


class FlatPageCreateView(FlatPageCreateUpdateView):
    creating = True

    def get_object(self):
        return None

    def get_title(self):
        return _("Add a new flat page")

    def get_success_url(self):
        messages.info(self.request, _("Flat page created successfully"))
        return reverse("dashboard:flatpage-list")


class FlatPageDeleteView(DeleteView):
    template_name = 'shop/dashboard/site/flatpage_delete.html'
    model = FlatPage
    form_class = FlatPageForm

    def get_context_data(self, *args, **kwargs):
        ctx = super(FlatPageDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = _("Delete flat page '%s'") % self.object.title

        return ctx

    def get_success_url(self):
        messages.info(self.request, _("Flat page deleted successfully"))
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
