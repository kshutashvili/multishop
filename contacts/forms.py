from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.forms import FlatpageForm as DjangoFlatpageForm

from .models import FlatPage


class FlatpageForm(DjangoFlatpageForm):
    class Meta:
        model = FlatPage
        fields = '__all__'
        widgets = {
            'content': CKEditorWidget()
        }
