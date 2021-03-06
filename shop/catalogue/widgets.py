from django.forms import widgets


class CustomFilterCheckboxChoiceInput(widgets.CheckboxChoiceInput):

    def __init__(self, name, value, attrs, choice, index):
        super(CustomFilterCheckboxChoiceInput, self).__init__(
            name, value, attrs, choice, index)
        params = choice[2]
        self.product_count = params['product_count']
        if self.product_count == 0:
            params['attrs']['disabled'] = True
        self.attrs.update(params['attrs'])


class CustomFilterCheckboxFieldRenderer(widgets.CheckboxFieldRenderer):
    choice_input_class = CustomFilterCheckboxChoiceInput


class CustomFilterCheckboxSelectMultiple(widgets.CheckboxSelectMultiple):
    renderer = CustomFilterCheckboxFieldRenderer
