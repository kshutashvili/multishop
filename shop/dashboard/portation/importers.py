from io import BytesIO
from openpyxl import load_workbook

from .base import Base
from shop.catalogue.models import Product
from shop.catalogue.models import Category
from shop.catalogue.models import ProductCategory


class CatalogueImporter(Base):

    def __init__(self, file):
        self.wb = load_workbook(BytesIO(file.read()))

    def handle(self):
        self.statistics = {
            'created': 0,
            'updated': 0,
        }
        self._import()
        return self.statistics

    def _import(self):
        ws = self.wb.active
        for row in ws:
            if row[0].row != 1:
                self.create_update_product(row)

    def create_update_product(self, data):

        field_values = data[0:len(self.FIELDS)]
        values = [item.value for item in field_values]
        values = dict(zip(self.FIELDS, values))

        try:
            product = Product.objects.get(id=values[Base.ID])
            self.statistics['updated'] += 1
        except Product.DoesNotExist:
            product = Product()
            self.statistics['created'] += 1

        categories = Category.objects.filter(
            id__in=self._get_categories(values[Base.CATEGORY]))
        ProductCategory.objects.filter(product=product).delete()
        for category in categories:
            ProductCategory.objects.create(product=product, category=category)

        product.title = values[self.TITLE]
        product.description = values[self.DESCRIPTION]
        product.upc = values[self.UPC]
        product.save()
        return product

    def _get_categories(self, category):
        if isinstance(category, str):
            categories = str(category).split(', ')
            categories = [int(item) for item in categories]
        else:
            categories = [int(category)]
        return categories
