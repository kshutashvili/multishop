from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PortationDashboardConfig(AppConfig):
    label = 'portation_dashboard'
    name = 'shop.dashboard.portation'
    verbose_name = _('Poration (import/export) dashboard')
