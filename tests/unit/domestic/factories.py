import factory
import factory.fuzzy
import wagtail_factories

from core import blocks as core_blocks
from domestic.models import DomesticDashboard, DomesticHomePage


class RouteSectionFactory(wagtail_factories.StructBlockFactory):
    title = 'Title'
    route_type = 'learn'
    body = factory.fuzzy.FuzzyText(length=60)
    image = None
    button = None

    class Meta:
        model = core_blocks.RouteSectionBlock


class DomesticHomePageFactory(wagtail_factories.PageFactory):

    title = 'homepage'
    body = factory.fuzzy.FuzzyText(length=255)
    live = True
    slug = 'homepage'

    class Meta:
        model = DomesticHomePage


class DomesticDashboardFactory(wagtail_factories.PageFactory):
    title = 'Title of Dashboard'
    live = True
    slug = 'dashboard'

    components = wagtail_factories.StreamFieldFactory({'route': RouteSectionFactory})

    class Meta:
        model = DomesticDashboard
