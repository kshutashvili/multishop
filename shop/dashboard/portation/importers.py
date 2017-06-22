from io import BytesIO
from openpyxl import load_workbook

from .base import Base
from shop.catalogue.models import Product
from shop.catalogue.models import Category
from shop.catalogue.models import ProductCategory
from shop.catalogue.models import ProductAttributeValue
from shop.catalogue.models import AttributeOption


class CatalogueImporter(Base):

    def __init__(self, file):
        self.wb = load_workbook(BytesIO(file.read()))

    def handle(self):
        self.statistics = {
            'created': 0,
            'updated': 0,
            'errors': [],
        }
        self._import()
        return self.statistics

    def _import(self):
        ws = self.wb.active
        self.max_row = ws.max_row
        for row in ws:
            if row[0].row != 1:
                try:
                    self.create_update_product(row)
                except:
                    self.statistics['errors'].append(str(row[0].row))

    def create_update_product(self, data):
        field_values = data[0:len(self.FIELDS)]
        values = [item.value for item in field_values]
        values = dict(zip(self.FIELDS, values))

        try:
            product = Product.objects.get(id=values[self.ID])
            self.statistics['updated'] += 1
        except Product.DoesNotExist:
            product = Product()
            self.statistics['created'] += 1

        categories = Category.objects.filter(
            id__in=self._get_categories(values[self.CATEGORY]))
        ProductCategory.objects.filter(product=product).delete()
        for category in categories:
            product_category = ProductCategory()
            product_category.product = product
            product_category.category = category
            product_category._no_index = True

        product.title_ru = values[self.TITLE_RU]
        product.title_uk = values[self.TITLE_UK]
        product.description_ru = values[self.DESCRIPTION_RU]
        product.description_uk = values[self.DESCRIPTION_UK]
        product.upc = values[self.UPC]
        if not data[0].row == self.max_row:
            product._no_index = True
        self.save_product_attributes(product, data)
        product.save()
        return product

    def save_product_attributes(self, product, data):
        self.attributes_to_import = product.product_class.attributes.all()
        attrs_values = data[len(self.FIELDS):]
        i = 0
        for attr in self.attributes_to_import:
            try:
                value_obj = product.attribute_values.get(attribute=attr)
            except ProductAttributeValue.DoesNotExist:
                value_obj = ProductAttributeValue()
                value_obj.attribute = attr
                value_obj.product = product
            if attr.type in ProductAttributeValue._localizable:
                _attribute_ru = 'value_%s_ru' % attr.type
                _attribute_uk = 'value_%s_uk' % attr.type
                setattr(value_obj, _attribute_ru, attrs_values[i].value)
                setattr(value_obj, _attribute_uk, attrs_values[i + 1].value)
                i += 2
            else:
                try:
                    value_obj._set_value(attrs_values[i].value)
                except AttributeOption.DoesNotExist:
                    attr_option = AttributeOption.objects.create(
                        group=value_obj.attribute.option_group,
                        option=unicode(attrs_values[i].value)
                    )
                    value_obj._set_value(attr_option)
                i += 1
            value_obj.save()

    def _get_categories(self, category):
        if isinstance(category, str):
            categories = str(category).split(', ')
            categories = [int(item) for item in categories]
        elif isinstance(category, type(None)):
            categories = []
        else:
            categories = [int(category)]
        return categories
