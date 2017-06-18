class Base():

    ID = 'ID'
    PRODUCT_CLASS = 'Product class'
    UPC = 'UPC'
    CATEGORY = 'Category ID(s)'
    TITLE = 'Title'
    DESCRIPTION = 'Description'

    FIELDS = [
        ID,
        PRODUCT_CLASS,
        UPC,
        CATEGORY,
        TITLE,
        DESCRIPTION,
    ]

    def __init__(self, *args, **kwargs):
        print self.FIELDS_TO_EXPORT_IMPORT
        print 'alalalall'
