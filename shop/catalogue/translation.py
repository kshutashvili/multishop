from modeltranslation.translator import translator, TranslationOptions

from shop.catalogue.models import ProductAttribute, ProductClass, Category, \
    ProductAttributeValue, FilterDescription, AttributeOption
from shop.order.models import PaymentMethod
from .models import Product


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'slug')


class ProductAttributeTranslationOptions(TranslationOptions):
    fields = ('name',)


class ProductClassTranslationOptions(TranslationOptions):
    fields = ('name',)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'description_title',
              'slug', 'name_in_side_menu')


class ProductAttributeValueTranslationOptions(TranslationOptions):
    fields = ('value_text', 'value_richtext',)


class FilterDescriptionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class AttributeOptionTranslationOptions(TranslationOptions):
    fields = ('option',)


class PaymentMethodTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Product, ProductTranslationOptions)
translator.register(ProductAttribute, ProductAttributeTranslationOptions)
translator.register(ProductClass, ProductClassTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(ProductAttributeValue, ProductAttributeValueTranslationOptions)
translator.register(FilterDescription, FilterDescriptionTranslationOptions)
translator.register(AttributeOption, AttributeOptionTranslationOptions)
translator.register(PaymentMethod, PaymentMethodTranslationOptions)
