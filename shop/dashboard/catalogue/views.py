from django.contrib.sites.shortcuts import get_current_site
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as OscarProductCreateUpdateView, \
    ProductClassCreateView as OscarProductClassCreateView, ProductClassUpdateView as OscarProductClassUpdateView, \
    CategoryCreateView as OscarCategoryCreateView, CategoryUpdateView as OscarCategoryUpdateView

from shop.dashboard.catalogue.forms import ProductForm, ProductAttributesFormSet, ProductClassForm, CategoryForm
from django.http.response import HttpResponseRedirect


class ProductCreateUpdateView(OscarProductCreateUpdateView):
    form_class = ProductForm

    def clean(self, form, formsets):
        self.object.site = get_current_site(self.request)
        self.object.save()
        return super(ProductCreateUpdateView, self).clean(form, formsets)


class ProductClassCreateView(OscarProductClassCreateView):
    template_name = 'shop/dashboard/catalogue/product_class_form.html'
    product_attributes_formset = ProductAttributesFormSet
    form_class = ProductClassForm

    def forms_valid(self, form, attributes_formset):
        form.cleaned_data['site'] = self.object.site = get_current_site(self.request)
        form.save()
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

    def form_valid(self, *args, **kwargs):
        self.object.site = get_current_site(self.request)
        self.object.save()
        return super(CategoryCreateView, self).form_valid(*args, **kwargs)


class CategoryUpdateView(OscarCategoryUpdateView):
    form_class = CategoryForm

    def form_valid(self, *args, **kwargs):
        self.object.site = get_current_site(self.request)
        self.object.save()
        return super(CategoryUpdateView, self).form_valid(*args, **kwargs)
