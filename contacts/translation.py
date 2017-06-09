from modeltranslation.translator import translator, TranslationOptions

from .models import FlatPage


class FlatPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


translator.register(FlatPage, FlatPageTranslationOptions)
