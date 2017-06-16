from modeltranslation.translator import translator, TranslationOptions

from .models import MenuItem, MetaTag


class MenuItemTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(MenuItem, MenuItemTranslationOptions)


class MetaTagTranslationOptions(TranslationOptions):
    fields = ('title', 'title_meta', 'description_meta', 'h1', )


translator.register(MetaTag, MetaTagTranslationOptions)
