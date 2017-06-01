from oscar.apps.partner.prices import FixedPrice as OscarFixedPrice


class FixedPrice(OscarFixedPrice):

    def __init__(self, currency, excl_tax, tax=None, previous=None):
        self.currency = currency
        self.excl_tax = excl_tax
        self.tax = tax
        self.previous = previous


class TaxInclusiveFixedPrice(FixedPrice):
    """
    Specialised version of FixedPrice that must have tax passed.  It also
    specifies that offers should use the tax-inclusive price (which is the norm
    in the UK).
    """
    exists = is_tax_known = True

    def __init__(self, currency, excl_tax, tax):
        self.currency = currency
        self.excl_tax = excl_tax
        self.tax = tax

    @property
    def incl_tax(self):
        return self.excl_tax + self.tax

    @property
    def effective_price(self):
        return self.incl_tax
