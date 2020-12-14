from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from django.conf import settings

from export_readiness import models


class BaseTranslationOptions(TranslationOptions):
    @property
    def required_languages(self):
        required_field_names = [
            field.name for field in self.model._meta.fields if not field.blank and field.name in self.fields
        ]
        return {settings.LANGUAGE_CODE: required_field_names}


@register(models.CountryGuidePage)
class CountryGuidePageTranslationOptions(TranslationOptions):
    fields = []


@register(models.ArticlePage)
class ArticlePageTranslationOptions(TranslationOptions):
    fields = []


@register(models.ArticleListingPage)
class ArticleListingPageTranslationOptions(TranslationOptions):
    fields = []


@register(models.CampaignPage)
class CampaignPageTranslationOptions(TranslationOptions):
    fields = []
