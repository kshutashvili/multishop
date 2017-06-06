from __future__ import unicode_literals

from django.utils.encoding import force_text
from django.forms.fields import MultipleChoiceField


class CustomFilterMultipleChoiceField(MultipleChoiceField):
    def valid_value(self, value):
        "Check to see if the provided value is a valid choice"
        text_value = force_text(value)
        for k, v, params in self.choices:
            if isinstance(v, (list, tuple)):
                # This is an optgroup, so look inside the group for options
                for k2, v2 in v:
                    if value == k2 or text_value == force_text(k2):
                        return True
            else:
                if value == k or text_value == force_text(k):
                    return True
        return False


class NonValidationMultipleChoiceField(CustomFilterMultipleChoiceField):

    def validate(self, value):
        pass
