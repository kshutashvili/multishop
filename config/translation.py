from modeltranslation.translator import translator, TranslationOptions

from .models import (MenuItem, MetaTag, BenefitItem, TextOne, TextTwo, TextThree,
                     TextFour, ReviewItem)


class MenuItemTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(MenuItem, MenuItemTranslationOptions)


class MetaTagTranslationOptions(TranslationOptions):
    fields = ('title', 'title_meta', 'description_meta', 'h1', )


translator.register(MetaTag, MetaTagTranslationOptions)


class BenefitItemTranslationOptions(TranslationOptions):
    fields = ('text',)

translator.register(BenefitItem, BenefitItemTranslationOptions)


class TextOneTranslationOptions(TranslationOptions):
    fields = ('text',)

translator.register(TextOne, TextOneTranslationOptions)


class TextTwoTranslationOptions(TranslationOptions):
    fields = ('text',)

translator.register(TextTwo, TextTwoTranslationOptions)


class TextThreeTranslationOptions(TranslationOptions):
    fields = ('text',)

translator.register(TextThree, TextThreeTranslationOptions)


class TextFourTranslationOptions(TranslationOptions):
    fields = ('text',)

translator.register(TextFour, TextFourTranslationOptions)


class ReviewItemTranslationOptions(TranslationOptions):
    fields = ('name', 'text',)

translator.register(ReviewItem, ReviewItemTranslationOptions)

