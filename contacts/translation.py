from modeltranslation.translator import translator, TranslationOptions

from .models import FlatPage, City, Timetable


class FlatPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


class CityTranslationOptions(TranslationOptions):
    fields = ('city_name', 'address',)


class TimetableTranslationOptions(TranslationOptions):
    fields = ('weekdays', 'daytime')


translator.register(FlatPage, FlatPageTranslationOptions)
translator.register(City, CityTranslationOptions)
translator.register(Timetable, TimetableTranslationOptions)
