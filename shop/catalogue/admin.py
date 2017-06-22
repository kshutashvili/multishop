from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from oscar.apps.catalogue.admin import ProductAdmin as OscarProductAdmin, \
    CategoryAdmin as OscarCategoryAdmin, \
    ProductAttributeValueAdmin as OscarProductAttributeValueAdmin, \
    CategoryInline, ProductRecommendationInline

from .models import ExtraImage, Product, Video, Category, ProductAttributeValue, \
    FilterDescription
from treebeard.forms import movenodeform_factory


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


CategoryAdminForm = movenodeform_factory(
    Category,
    exclude=('name', 'description', 'description_title'),
    widgets={
        'description_ru': CKEditorWidget(),
        'description_uk': CKEditorWidget(),
    }
)


@admin.register(Category)
class CategoryAdmin(OscarCategoryAdmin):

    form = CategoryAdminForm
    fields = ('name_ru', 'name_uk',
              'description_title_ru', 'description_title_uk',
              'description_ru', 'description_uk',
              'image', 'slug', 'site',
              '_position', '_ref_node_id')


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(OscarProductAttributeValueAdmin):
    form = ProductAttributeValueAdminForm


class FilterDescriptionAdminForm(forms.ModelForm):
    class Meta:
        model = FilterDescription
        widgets = {
            'description_ru': CKEditorWidget(),
            'description_uk': CKEditorWidget(),
        }
        exclude = ('title', 'description')


@admin.register(FilterDescription)
class FilterDescriptionAdmin(admin.ModelAdmin):
    form = FilterDescriptionAdminForm
    list_display = ('filter_url', 'title')


from oscar.apps.catalogue.admin import *  # noqa
