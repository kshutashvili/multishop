# -*- coding: utf-8 -*-
from django import forms
from django.core import exceptions
from django.forms.models import inlineformset_factory

from oscar.apps.dashboard.catalogue.forms import \
    ProductForm as OscarProductForm, \
    ProductAttributesForm as OscarProductAttributes, \
    ProductClassForm as OscarProductClassForm, \
    ProductImageForm as OscarProductImageForm, \
    ProductClassSelectForm as OscarProductClassSelectForm, \
    StockRecordForm as OscarStockRecordForm, \
    StockRecordFormSet as OscarStockRecordFormSet
from oscar.forms.widgets import ImageInput
from treebeard.forms import movenodeform_factory

from shop.catalogue.models import Product, ProductClass, ProductAttribute, \
    Category, ProductAttributeValue, ExtraImage, Video
from shop.partner.models import StockRecord

from oscar.core.loading import get_class


ModelMetaTag = get_class('config.models', 'ModelMetaTag')


def _attr_textarea_field_uk(attribute):
    """
    django-oscar use factory to create attribute fields, attribute fields that will be
    displayed are hardcoded, so we need to define our owns
    """
    return forms.CharField(label=attribute.name_uk,
                           widget=forms.Textarea(),
                           required=attribute.required)


def _attr_text_field_uk(attribute):
    return forms.CharField(label=attribute.name_uk,
                           required=attribute.required)


def _attr_textarea_field_ru(attribute):
    """
    django-oscar use factory to create attribute fields, attribute fields that will be
    displayed are hardcoded, so we need to define our owns
    """
    return forms.CharField(label=attribute.name_ru,
                           widget=forms.Textarea(),
                           required=attribute.required)


def _attr_text_field_ru(attribute):
    return forms.CharField(label=attribute.name_ru,
                           required=attribute.required)


class ProductForm(OscarProductForm):
    _localizable = ["text",
                    "richtext"]  # types of fields, that need to be localized
    OscarProductForm.FIELD_FACTORIES['text_uk'] = _attr_text_field_uk
    OscarProductForm.FIELD_FACTORIES['richtext_uk'] = _attr_textarea_field_uk
    OscarProductForm.FIELD_FACTORIES['text_ru'] = _attr_text_field_ru
    OscarProductForm.FIELD_FACTORIES['richtext_ru'] = _attr_textarea_field_ru
    title_ru = forms.CharField(label='Название (на русском)')
    description_ru = forms.CharField(label='Описание (на русском)',
                                     widget=forms.Textarea(), required=False)
    title_uk = forms.CharField(label='Назва (українською)')
    description_uk = forms.CharField(label='Опис (українською)',
                                     widget=forms.Textarea(), required=False)

    class Meta:
        model = Product
        fields = [
            'title_ru', 'title_uk', 'upc', 'description_ru', 'description_uk',
            'is_discountable', 'structure', 'new', 'top_sale', 'recommended',
            'super_price', 'special_offer', 'gift', 'free_shipping']
        widgets = {
            'structure': forms.HiddenInput(),
        }

    def add_attribute_fields(self, product_class, is_parent=False):
        """
        For each attribute specified by the product class, this method
        dynamically adds form fields to the product form.
        """
        for attribute in product_class.attributes.all():
            if attribute.type in ProductForm._localizable:

                attr_type = attribute.type
                attribute.type = '_'.join((attr_type, 'ru',))
                field = self.get_attribute_field(attribute)
                if field:
                    self.fields['attr_%s' % attribute.code] = field
                    # Attributes are not required for a parent product
                    if is_parent:
                        self.fields['attr_%s' % attribute.code].required = False
                attribute.type = '_'.join((attr_type, 'uk'))
                field_uk = self.get_attribute_field(attribute)
                if field_uk:
                    self.fields['attr_%s_uk' % attribute.code] = field_uk
                    # Attributes are not required for a parent product
                    if is_parent:
                        self.fields[
                            'attr_%s_uk' % attribute.code].required = False
            else:
                field = self.get_attribute_field(attribute)
                if field:
                    self.fields['attr_%s' % attribute.code] = field
                    # Attributes are not required for a parent product
                    if is_parent:
                        self.fields['attr_%s' % attribute.code].required = False

    def get_attribute_field(self, attribute):
        """
        Gets the correct form field for a given attribute type.
        """
        return self.FIELD_FACTORIES[attribute.type](attribute)

    def _post_clean(self):
        self.instance.attr.initiate_attributes()
        for attribute in self.instance.attr.get_all_attributes():
            field_name = 'attr_%s' % attribute.code
            field_name_uk = 'attr_%s_uk' % attribute.code
            # An empty text field won't show up in cleaned_data.
            if field_name in self.cleaned_data:
                value = self.cleaned_data[field_name]
                setattr(self.instance.attr, attribute.code, value)
            if field_name_uk in self.cleaned_data:
                try:
                    attr = ProductAttributeValue.objects.get(
                        attribute=attribute, product=self.instance)
                    value = self.cleaned_data[field_name_uk]
                    setattr(attr, '_'.join(('value', attribute.type, 'uk',)),
                            value)
                    attr.save()
                except ProductAttributeValue.DoesNotExist:
                    pass
        super(ProductForm, self)._post_clean()

    def set_initial_attribute_values(self, product_class, kwargs):
        """
        Update the kwargs['initial'] value to have the initial values based on
        the product instance's attributes
        """
        instance = kwargs.get('instance')
        if instance is None:
            return
        for attribute in product_class.attributes.all():
            try:
                value = instance.attribute_values.get(
                    attribute=attribute).value
            except exceptions.ObjectDoesNotExist:
                pass
            else:
                if attribute.type in ProductForm._localizable:
                    kwargs['initial']['attr_%s' % attribute.code], \
                    kwargs['initial'][
                        'attr_%s_uk' % attribute.code] = value  # now returns tuple
                else:
                    kwargs['initial']['attr_%s' % attribute.code] = value


class ProductAttributesForm(OscarProductAttributes):
    name_uk = forms.CharField(label='Назва (українською)')
    name_ru = forms.CharField(label='Название (на русском)')

    class Meta:
        model = ProductAttribute
        fields = ["name_ru", "name_uk", "code", "type", "option_group",
                  "required"]


class ProductClassForm(OscarProductClassForm):
    name_uk = forms.CharField(label='Назва (українською)')
    name_ru = forms.CharField(label='Название (на русском)')

    class Meta:
        model = ProductClass
        fields = ['name_ru', 'name_uk', 'requires_shipping', 'track_stock',
                  'options', 'image']
        widgets = {
            'image': ImageInput(),
        }


CategoryForm = movenodeform_factory(
    Category,
    fields=['name_ru', 'name_uk', 'description_ru', 'description_uk', 'image'])


class ExtraProductImageForm(OscarProductImageForm):
    class Meta:
        model = ExtraImage
        fields = ['product', 'image', ]
        # use ImageInput widget to create HTML displaying the
        # actual uploaded image and providing the upload dialog
        # when clicking on the actual image.
        widgets = {
            'image': ImageInput(),
        }


class ProductVideoForm(OscarProductImageForm):
    class Meta:
        model = Video
        fields = ['product', 'video', ]
        # use ImageInput widget to create HTML displaying the
        # actual uploaded image and providing the upload dialog
        # when clicking on the actual image.
        widgets = {
            'video': forms.URLInput(),
        }


ProductAttributesFormSet = inlineformset_factory(ProductClass,
                                                 ProductAttribute,
                                                 form=ProductAttributesForm,
                                                 extra=3)

BaseExtraProductImageFormSet = inlineformset_factory(
    Product, ExtraImage, form=ExtraProductImageForm, extra=2)

BaseProductVideoFormSet = inlineformset_factory(
    Product, Video, form=ProductVideoForm, extra=2)


class ExtraProductImageFormSet(BaseExtraProductImageFormSet):
    def __init__(self, product_class, user, *args, **kwargs):
        super(ExtraProductImageFormSet, self).__init__(*args, **kwargs)


class ProductVideoFormSet(BaseProductVideoFormSet):
    def __init__(self, product_class, user, *args, **kwargs):
        super(ProductVideoFormSet, self).__init__(*args, **kwargs)


class ProductClassSelectForm(OscarProductClassSelectForm):
    def __init__(self, *args, **kwargs):
        site = kwargs.pop('site') if 'site' in kwargs else None
        super(ProductClassSelectForm, self).__init__(*args, **kwargs)
        if site:
            self.fields['product_class'].queryset = ProductClass.objects.filter(
                site=site)


class StockRecordForm(OscarStockRecordForm):

    def __init__(self, product_class, user, *args, **kwargs):
        # The user kwarg is not used by stock StockRecordForm. We pass it
        # anyway in case one wishes to customise the partner queryset
        self.user = user
        super(StockRecordForm, self).__init__(*args, **kwargs)

        # Restrict accessible partners for non-staff users
        if not self.user.is_staff:
            self.fields['partner'].queryset = self.user.partners.all()

        # If not tracking stock, we hide the fields
        if not product_class.track_stock:
            for field_name in ['num_in_stock', 'low_stock_treshold']:
                if field_name in self.fields:
                    del self.fields[field_name]
        else:
            for field_name in ['price_excl_tax', 'num_in_stock']:
                if field_name in self.fields:
                    self.fields[field_name].required = True

    class Meta:
        model = StockRecord
        fields = [
            'partner', 'partner_sku',
            'price_currency', 'price_excl_tax', 'price_retail', 'cost_price',
            'num_in_stock', 'low_stock_threshold',
        ]


class ModelMetaTagForm(forms.ModelForm):
    class Meta:
        model = ModelMetaTag
        fields = '__all__'
