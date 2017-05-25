from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from oscar.apps.catalogue.admin import ProductAdmin as OscarProductAdmin, \
    CategoryAdmin as OscarCategoryAdmin, \
    ProductAttributeValueAdmin as OscarProductAttributeValueAdmin, \
    CategoryInline, ProductRecommendationInline

from .models import ExtraImage, Product, Video, Category, ProductAttributeValue


class ExtraImageInline(admin.TabularInline):
    model = ExtraImage
    extra = 0


class VideoInline(admin.TabularInline):
    model = Video
    extra = 0


admin.site.unregister(Product)
admin.site.unregister(Category)
admin.site.unregister(ProductAttributeValue)


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        widgets = {
            'description_ru': CKEditorWidget(),
            'description_uk': CKEditorWidget(),
        }
        exclude = ('name', 'description')


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        widgets = {
            'description_ru': CKEditorWidget(),
            'description_uk': CKEditorWidget(),
        }
        exclude = ('name', 'description')


class ProductAttributeValueAdminForm(forms.ModelForm):
    class Meta:
        model = ProductAttributeValue
        widgets = {
            'value_richtext_ru': CKEditorWidget(),
            'value_richtext_uk': CKEditorWidget(),
        }
        exclude = ('value_text', 'value_richtext')


class AttributeInline(admin.TabularInline):
    model = ProductAttributeValue
    form = ProductAttributeValueAdminForm


@admin.register(Product)
class ProductAdmin(OscarProductAdmin):
    form = ProductAdminForm
    inlines = [AttributeInline, CategoryInline, ProductRecommendationInline,
               ExtraImageInline, VideoInline]


@admin.register(Category)
class CategoryAdmin(OscarCategoryAdmin):
    form = CategoryAdminForm


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(OscarProductAttributeValueAdmin):
    form = ProductAttributeValueAdminForm


from oscar.apps.catalogue.admin import *  # noqa
