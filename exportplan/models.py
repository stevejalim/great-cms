from wagtail.core.models import Page

from core import mixins
from exportplan import data


class ExportPlanDashboardPage(
    mixins.WagtailAdminExclusivePageMixin,
    mixins.EnableTourMixin,
    mixins.ExportPlanMixin,
    Page,
):

    template = 'exportplan/dashboard_page.html'

    def get_context(self, request):
        context = super().get_context(request)
        context['sections'] = list(data.SECTIONS.values())
        return context
