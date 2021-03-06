from django.views.generic import FormView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib import messages

from openpyxl.writer.excel import save_virtual_workbook

from .forms import ImportForm
from .forms import ExportForm
from .exporters import CatelogueExporter
from .importers import CatalogueImporter
from shop.catalogue.models import ProductClass


class ImportView(FormView):
    template_name = 'shop/dashboard/portation/base.html'
    form_class = ImportForm

    def get_context_data(self, **kwargs):
        context = super(ImportView, self).get_context_data(**kwargs)
        context['includes_files'] = True
        context['title'] = _('Import')
        return context

    def form_valid(self, form):
        file = form.cleaned_data['file']
        importer = CatalogueImporter(file)
        result = importer.handle()
        result_message = _('Updated: {}; Created: {}.'.format(
            result['updated'], result['created']))
        messages.success(self.request, result_message)
        errors = result.get('errors')
        if errors:
            errors_message = _('Errors on rows: {}').format(', '.join(errors))
            messages.error(self.request, errors_message)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


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
        context['includes_files'] = False
        return context


class AttrubitesListView(ListView):
    """ A view that returns attributes list based on selected product class """
    def get(self, request, *args, **kwargs):
        p_class_id = request.GET.get('p_class_id')
        self.product_class = get_object_or_404(ProductClass, id=p_class_id)
        data = {
            'attributes': [],
        }
        attributes = self.get_queryset()
        for attribute in attributes:
            data['attributes'].append({
                'id': attribute.id,
                'code': attribute.code,
                'name': attribute.name,
            })
        return JsonResponse(data, status=200, safe=False)

    def get_queryset(self):
        return self.product_class.attributes.all()
