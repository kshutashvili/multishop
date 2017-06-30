from django.contrib.sites.shortcuts import get_current_site
from django.http.response import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
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
    ExtraProductImageFormSet, ProductVideoFormSet, ProductClassSelectForm
from website.views import SiteMultipleObjectMixin

ModelMetaTag = get_class('config.models', 'ModelMetaTag')


class ProductCreateUpdateView(OscarProductCreateUpdateView):
    template_name = 'shop/dashboard/catalogue/product_update.html'
    form_class = ProductForm
    extra_product_image_formset = ExtraProductImageFormSet
    video_formset = ProductVideoFormSet

    def __init__(self, *args, **kwargs):
        super(ProductCreateUpdateView, self).__init__(*args, **kwargs)
        self.formsets['extra_image_formset'] = self.extra_product_image_formset
        self.formsets['video_formset'] = self.video_formset

    def clean(self, form, formsets):
        self.object.site = get_current_site(self.request)
        self.object.save()
        return super(ProductCreateUpdateView, self).clean(form, formsets)

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

    def form_valid(self, form, *args, **kwargs):
        form.cleaned_data['site'] = get_current_site(self.request)
        return super(CategoryCreateView, self).form_valid(form, *args, **kwargs)


class CategoryUpdateView(OscarCategoryUpdateView):
    template_name = 'shop/dashboard/catalogue/category_form.html'
    form_class = CategoryForm

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
    productclass_form_class = ProductClassSelectForm

    def get_context_data(self, **kwargs):
        ctx = super(ProductListView, self).get_context_data(**kwargs)
        site = get_current_site(self.request)
        ctx['productclass_form'] = self.productclass_form_class(site=site)
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
