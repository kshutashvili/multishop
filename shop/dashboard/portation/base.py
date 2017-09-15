from django.utils.translation import ugettext_lazy as _


class Base():

    ID = _('ID')
    PRODUCT_CLASS = _('Product class')

    FIELDS = (
        ('id', ID),
        ('product_class', PRODUCT_CLASS),
    )
