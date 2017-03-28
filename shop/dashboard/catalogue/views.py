from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as OscarProductCreateUpdateView, \
    ProductClassCreateView as OscarProductClassCreateView, ProductClassUpdateView as OscarProductClassUpdateView, \
    CategoryCreateView as OscarCategoryCreateView, CategoryUpdateView as OscarCategoryUpdateView

from shop.dashboard.catalogue.forms import ProductForm, ProductAttributesFormSet, ProductClassForm, CategoryForm
from django.contrib.sites.shortcuts import get_current_site


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


class ProductClassUpdateView(OscarProductClassUpdateView):
    template_name = 'shop/dashboard/catalogue/product_class_form.html'
    product_attributes_formset = ProductAttributesFormSet
    form_class = ProductClassForm


class CategoryCreateView(OscarCategoryCreateView):
    form_class = CategoryForm


class CategoryUpdateView(OscarCategoryUpdateView):
    form_class = CategoryForm
