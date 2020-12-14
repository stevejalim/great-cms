from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from core import models as core_models
from domestic import models as domestic_models
from exportplan import models as exportplan_models
from sso import models as sso_models


@register(domestic_models.DomesticHomePage)
class DomesticHomePageTranslationOptions(TranslationOptions):
    fields = []


@register(domestic_models.DomesticDashboard)
class DomesticDashboardTranslationOptions(TranslationOptions):
    fields = []


@register(exportplan_models.ExportPlanDashboardPage)
class ExportPlanDashboardPageTranslationOptions(TranslationOptions):
    fields = []


@register(sso_models.BusinessSSOUser)
class BusinessSSOUserTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.GreatMedia)
class GreatMediaTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.DocumentHash)
class DocumentHashTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.ImageHash)
class ImageHashTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.AltTextImage)
class AltTextImageTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.Rendition)
class RenditionTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.Tour)
class TourTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.TourStep)
class TourStepTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.Product)
class ProductTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.Country)
class CountryTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.LandingPage)
class LandingPageTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.InterstitialPage)
class InterstitialPageTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.ListPage)
class ListPageTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.CuratedListPage)
class CuratedListPageTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.TopicPage)
class TopicPageTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.LessonPlaceholderPage)
class LessonPlaceholderPageTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.DetailPage)
class DetailPageTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.PageView)
class PageViewTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.ContentModuleTag)
class ContentModuleTagTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.ContentModule)
class ContentModuleTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.PersonalisationHSCodeTag)
class PersonalisationHSCodeTagTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.PersonalisationCountryTag)
class PersonalisationCountryTagTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.HSCodeTaggedCaseStudy)
class HSCodeTaggedCaseStudyTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.CountryTaggedCaseStudy)
class CountryTaggedCaseStudyTranslationOptions(TranslationOptions):
    fields = []


@register(core_models.CaseStudy)
class CaseStudyTranslationOptions(TranslationOptions):
    fields = []
