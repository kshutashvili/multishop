from modeltranslation.translator import translator, TranslationOptions

from .models import MenuItem


class MenuItemTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(MenuItem, MenuItemTranslationOptions)
