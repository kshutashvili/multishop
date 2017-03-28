# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory
from oscar.apps.dashboard.catalogue.forms import ProductForm as OscarProductForm, \
    ProductAttributesForm as OscarProductAttributes, ProductClassForm as OscarProductClassForm
from treebeard.forms import movenodeform_factory

from shop.catalogue.models import Product, ProductClass, ProductAttribute, Category


def _attr_textarea_field_uk(attribute):
    return forms.CharField(label=attribute.name_uk,
                           widget=forms.Textarea(),
                           required=attribute.required)


def _attr_text_field_uk(attribute):
    return forms.CharField(label=attribute.name_uk,
                           required=attribute.required)


class ProductForm(OscarProductForm):
    _localizable = ["text", "richtext"]
    OscarProductForm.FIELD_FACTORIES['text_uk'] = _attr_text_field_uk
    OscarProductForm.FIELD_FACTORIES['richtext_uk'] = _attr_textarea_field_uk
    title_uk = forms.CharField(label='Назва (українською)')
    description_uk = forms.CharField(label='Опис (українською)', widget=forms.Textarea(), required=False)

    class Meta:
        model = Product
        fields = [
            'title', 'title_uk', 'upc', 'description', 'description_uk', 'is_discountable', 'structure', 'site']
        widgets = {
            'structure': forms.HiddenInput()
        }

    def add_attribute_fields(self, product_class, is_parent=False):
        """
        For each attribute specified by the product class, this method
        dynamically adds form fields to the product form.
        """
        for attribute in product_class.attributes.all():
            field = self.get_attribute_field(attribute)
            if field:
                self.fields['attr_%s' % attribute.code] = field
                # Attributes are not required for a parent product
                if is_parent:
                    self.fields['attr_%s' % attribute.code].required = False
            if attribute.type in ProductForm._localizable:
                attribute.type = ''.join((attribute.type, '_uk'))
                field_uk = self.get_attribute_field(attribute)
                if field_uk:
                    self.fields['attr_%s_uk' % attribute.code] = field_uk
                    # Attributes are not required for a parent product
                    if is_parent:
                        self.fields['attr_%s_uk' % attribute.code].required = False

    def get_attribute_field(self, attribute):
        """
        Gets the correct form field for a given attribute type.
        """
        return self.FIELD_FACTORIES[attribute.type](attribute)


class ProductAttributesForm(OscarProductAttributes):
    class Meta:
        model = ProductAttribute
        fields = ["name", "name_uk", "code", "type", "option_group", "required"]


class ProductClassForm(OscarProductClassForm):
    name_uk = forms.CharField(label='Назва (українською)')

    class Meta:
        model = ProductClass
        fields = ['name', 'name_uk', 'requires_shipping', 'track_stock', 'options']


CategoryForm = movenodeform_factory(
    Category,
    fields=['name', 'name_uk', 'description', 'description_uk', 'image'])

ProductAttributesFormSet = inlineformset_factory(ProductClass,
                                                 ProductAttribute,
                                                 form=ProductAttributesForm,
                                                 extra=3)
