from django import forms

from shop.catalogue.models import AttributeOptionGroup


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
                    choices=[(i.id, u'%s' % (i.option,)) for i in
                             group.options.all()],
                    required=False
                )
