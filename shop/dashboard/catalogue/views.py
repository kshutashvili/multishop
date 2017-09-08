# -*- coding: utf-8 -*-
from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic import UpdateView, ListView, DeleteView
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.shortcuts import reverse, get_object_or_404
from django.utils.translation import ugettext_lazy as _

from oscar.apps.dashboard.catalogue.views import \
    ProductCreateUpdateView as OscarProductCreateUpdateView, \
    ProductClassCreateView as OscarProductClassCreateView, \
    ProductClassUpdateView as OscarProductClassUpdateView, \
    CategoryCreateView as OscarCategoryCreateView, \
    CategoryUpdateView as OscarCategoryUpdateView, \
    ProductListView as OscarProductListView, \
    CategoryListView as OscarCategoryListView, \
    ProductClassListView as OscarProductClassListView
from oscar.core.loading import get_class

from shop.dashboard.catalogue.forms import ProductForm, ModelMetaTagForm, \
    ProductAttributesFormSet, ProductClassForm, CategoryForm, \
    ExtraProductImageFormSet, ProductVideoFormSet, ProductClassSelectForm, \
    AttributeOptionGroupForm, AttributeOptionFormSet
from website.views import SiteMultipleObjectMixin
from .forms import StockRecordFormSet

ModelMetaTag = get_class('config.models', 'ModelMetaTag')
AttributeOptionGroup = get_class('shop.catalogue.models', 'AttributeOptionGroup')


class ProductCreateUpdateView(OscarProductCreateUpdateView):
    template_name = 'shop/dashboard/catalogue/product_update.html'
    form_class = ProductForm
    extra_product_image_formset = ExtraProductImageFormSet
    video_formset = ProductVideoFormSet
    stockrecord_formset = StockRecordFormSet

    def __init__(self, *args, **kwargs):
        super(ProductCreateUpdateView, self).__init__(*args, **kwargs)
        self.formsets['extra_image_formset'] = self.extra_product_image_formset
        self.formsets['video_formset'] = self.video_formset
        self.formsets['stockrecord_formset'] = self.stockrecord_formset

    def clean(self, form, formsets):
        self.object.site = get_current_site(self.request)
        self.object.save()
        return super(ProductCreateUpdateView, self).clean(form, formsets)

    def get_form_kwargs(self):
        kwargs = super( ProductCreateUpdateView, self ).get_form_kwargs()
        kwargs['site'] = get_current_site(self.request)
        return kwargs

    def get_context_data(self, **kwargs):
        cxt = super(ProductCreateUpdateView, self).get_context_data(**kwargs)
        if self.object:
            content_type = ContentType.objects.get_for_model(self.object)

            model_meta_tag = ModelMetaTag.objects.filter(
                content_type=content_type,
                object_id=self.object.id,
            )
            if model_meta_tag.exists():
                cxt['model_meta_tag'] = model_meta_tag[0]
            else:
                cxt.update({
                    'meta_tag_object': self.object,
                    'meta_tag_content_type': content_type,
                })

        cxt['category_formset'] = self.formsets['category_formset'](
            self.product_class,
            self.request.user,
            instance=self.object,
            site=get_current_site(self.request)
        )

        return cxt


class ProductClassCreateView(OscarProductClassCreateView):
    template_name = 'shop/dashboard/catalogue/product_class_form.html'
    product_attributes_formset = ProductAttributesFormSet
    form_class = ProductClassForm

    def forms_valid(self, form, attributes_formset):
        obj = form.save(commit=False)
        obj.site = get_current_site(self.request)
        obj.save()
        attributes_formset.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductClassUpdateView(OscarProductClassUpdateView):
    template_name = 'shop/dashboard/catalogue/product_class_form.html'
    product_attributes_formset = ProductAttributesFormSet
    form_class = ProductClassForm

    def form_valid(self, *args, **kwargs):
        self.object.site = get_current_site(self.request)
        self.object.save()
        return super(ProductClassUpdateView, self).form_valid(*args, **kwargs)


class CategoryCreateView(OscarCategoryCreateView):
    form_class = CategoryForm

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(CategoryCreateView, self).get_form_kwargs()
        kwargs['site'] = get_current_site(self.request)
        return kwargs

    def form_valid(self, form, *args, **kwargs):
        form.cleaned_data['site'] = get_current_site(self.request)
        return super(CategoryCreateView, self).form_valid(form, *args, **kwargs)


class CategoryUpdateView(OscarCategoryUpdateView):
    template_name = 'shop/dashboard/catalogue/category_form.html'
    form_class = CategoryForm

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(CategoryUpdateView, self).get_form_kwargs()
        kwargs['site'] = get_current_site(self.request)
        return kwargs

    def form_valid(self, *args, **kwargs):
        self.object.site = get_current_site(self.request)
        self.object.save()
        return super(CategoryUpdateView, self).form_valid(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        content_type = ContentType.objects.get_for_model(self.object)

        model_meta_tag = ModelMetaTag.objects.filter(
            content_type=content_type,
            object_id=self.object.id,
        )
        if model_meta_tag.exists():
            context['model_meta_tag'] = model_meta_tag[0]
        else:
            context.update({
                'meta_tag_object': self.object,
                'meta_tag_content_type': content_type,
            })
        return context


class ProductListView(SiteMultipleObjectMixin, OscarProductListView):
    template_name = 'shop/dashboard/catalogue/product_list.html'
    productclass_form_class = ProductClassSelectForm

    def get_context_data(self, **kwargs):
        ctx = super(ProductListView, self).get_context_data(**kwargs)
        site = get_current_site(self.request)
        ctx['productclass_form'] = self.productclass_form_class(site=site)
        ctx['product_items'] = self.get_queryset()
        return ctx


class CategoryListView(SiteMultipleObjectMixin, OscarCategoryListView):
    pass


class ProductClassListView(SiteMultipleObjectMixin, OscarProductClassListView):
    pass


class MetaTagCreateView(CreateView):
    model = ModelMetaTag
    form_class = ModelMetaTagForm
    template_name = 'shop/dashboard/catalogue/model_meta_tag.html'

    def get_initial(self):
        return {
            'object_id': self.request.GET.get('object_id'),
            'content_type': self.request.GET.get('content_type'),
        }

    def get_context_data(self, **kwargs):
        context = super(MetaTagCreateView, self).get_context_data(**kwargs)
        context['title'] = _('Create Object Meta Tag')
        return context

    def get_success_url(self):
        message = _('Meta tag for "{}" was created successfully') \
            .format(self.object.content_object)
        messages.info(self.request, message)
        next = self.request.GET.get('next')
        if next:
            return next
        return self.request.META.get('HTTP_REFERER')


class MetaTagUpdateView(UpdateView):
    model = ModelMetaTag
    form_class = ModelMetaTagForm
    template_name = 'shop/dashboard/catalogue/model_meta_tag.html'

    def get_context_data(self, **kwargs):
        context = super(MetaTagUpdateView, self).get_context_data(**kwargs)
        context['title'] = _('Update Object Meta Tag')
        return context

    def get_success_url(self):
        message = _('Meta tag for "{}" was updated successfully') \
            .format(self.object.content_object)
        messages.info(self.request, message)
        next = self.request.GET.get('next')
        if next:
            return next
        return self.request.META.get('HTTP_REFERER')


class AttributeOptionGroupListView(SiteMultipleObjectMixin, ListView):
    model = AttributeOptionGroup
    template_name = "shop/dashboard/catalogue/attributeoptiongroup_list.html"
    context_object_name = 'option_groups'


class AttributeOptionGroupCreateUpdateView(UpdateView):
    model = AttributeOptionGroup
    form_class = AttributeOptionGroupForm
    option_formset = AttributeOptionFormSet
    template_name = 'shop/dashboard/catalogue/attributeoptiongroup_detail.html'

    def process_all_forms(self, form):
        if self.creating and form.is_valid():
            # the object will be needed by formsets
            self.object = form.save(commit=False)
            self.object.site = get_current_site(self.request)

        option_formset = self.option_formset(
            self.request.POST, self.request.FILES, instance=self.object)

        is_valid = form.is_valid() and option_formset.is_valid()

        if is_valid:
            return self.forms_valid(form,
                                    option_formset)
        else:
            return self.forms_invalid(form,
                                      option_formset)

    def forms_valid(self, form, option_formset):
        form.save()
        option_formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def forms_invalid(self, form, option_formset):
        messages.error(self.request,
                       _("Your submitted data was not valid - please "
                         "correct the errors below"
                         ))
        ctx = self.get_context_data(form=form,
                                    option_formset=option_formset)
        return self.render_to_response(ctx)

    form_valid = form_invalid = process_all_forms

    def get_context_data(self, *args, **kwargs):
        ctx = super(AttributeOptionGroupCreateUpdateView, self).get_context_data(
            *args, **kwargs)

        if "option_formset" not in ctx:
            ctx["option_formset"] = self.option_formset(
                instance=self.object)

        ctx["title"] = self.get_title()

        return ctx


class AttributeOptionGroupUpdateView(AttributeOptionGroupCreateUpdateView):
    creating = False

    def get_title(self):
        return u"Обновить групу опций атрибутов '%s'" % self.object.name

    def get_success_url(self):
        messages.info(self.request, u"Группа опций атрибутов успешно сохранена")
        return reverse("dashboard:optiongroup-list")

    def get_object(self):
        city = get_object_or_404(self.model, pk=self.kwargs['pk'])
        return city


class AttributeOptionGroupCreateView(AttributeOptionGroupCreateUpdateView):
    creating = True

    def get_object(self):
        return None

    def get_title(self):
        return u"Создать новую группу опций атрибутов"

    def get_success_url(self):
        messages.info(self.request, u"Новая группа опций атрибутов создана")
        return reverse("dashboard:optiongroup-list")


class AttributeOptionGroupDeleteView(DeleteView):
    model = AttributeOptionGroup
    template_name = "shop/dashboard/catalogue/attributeoptiongroup_delete.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super(AttributeOptionGroupDeleteView, self).get_context_data(
            *args,
            **kwargs)

        ctx['title'] = u"Удаление группы опций атрибутов '%s'" % self.object.name

        return ctx

    def get_success_url(self):
        messages.success(
            self.request, u"Группа опций атрибутов '%s' удалена" % self.object.name)
        return reverse('dashboard:optiongroup-list')
