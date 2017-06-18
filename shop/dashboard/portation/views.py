from django.views.generic import FormView
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from openpyxl.writer.excel import save_virtual_workbook

from .forms import ImportForm
from .forms import ExportForm
from .exporters import CatelogueExporter


class ImportView(FormView):
    form_class = ImportForm


class ExportView(FormView):
    template_name = 'shop/dashboard/portation/base.html'
    form_class = ExportForm

    def get_form_kwargs(self):
        kwargs = super(ExportView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
        })
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data
        exporter = CatelogueExporter(data)
        wb = exporter.handle()
        response = HttpResponse(
            save_virtual_workbook(wb), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="export.xlsx"'
        return response

    def get_context_data(self, **kwargs):
        context = super(ExportView, self).get_context_data(**kwargs)
        context['title'] = _('Catalogue Export')
        return context
