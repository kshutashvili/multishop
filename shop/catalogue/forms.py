from django import forms

from shop.catalogue.models import AttributeOptionGroup, Product


class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)

        self.make_filter()

    def make_filter(self):
        for group in AttributeOptionGroup.objects.all():
            self.fields[u'filter_%s' % group.name] = \
                forms.MultipleChoiceField(
                    widget=forms.CheckboxSelectMultiple(),
                    label=group.name,
                    choices=[
                        (i.id, u'%s (%s)' % (i.option, Product.objects.filter(
                            attribute_values__value_option=i).count()))
                        for i in group.options.all()],
                    required=False
                )
