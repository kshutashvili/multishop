from django.forms import widgets
from django.utils.encoding import force_text


class CustomFilterCheckboxChoiceInput(widgets.CheckboxChoiceInput):

    def __init__(self, name, value, attrs, choice, index):
        super(CustomFilterCheckboxChoiceInput, self).__init__(
            name, value, attrs, choice, index)
        self.product_count = force_text(choice[2])


class CustomFilterCheckboxFieldRenderer(widgets.CheckboxFieldRenderer):
    choice_input_class = CustomFilterCheckboxChoiceInput


class CustomFilterCheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    renderer = CustomFilterCheckboxFieldRenderer
