import abc
import datetime
import logging
import math

from directory_constants import choices
from formtools.wizard.views import NamedUrlSessionWizardView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.template.response import TemplateResponse
from django.views.generic import TemplateView, FormView
from core.fern import Fern
from django.conf import settings
from great_components.mixins import GA360Mixin

from django.urls import reverse_lazy
from directory_forms_api_client.helpers import Sender
from core import forms, helpers, serializers, cms_slugs

logger = logging.getLogger(__name__)

STEP_START = 'start'
STEP_WHAT_SELLING = 'what-are-you-selling'
STEP_PRODUCT_SEARCH = 'product-search'
STEP_SIGN_UP = 'sign-up'


class UpdateCompanyAPIView(generics.GenericAPIView):
    serializer_class = serializers.CompanySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = {key: value for key, value in serializer.validated_data.items() if value}
        if not self.request.user.company:
            data['name'] = f'unnamed sso-{self.request.user.id} company'
        helpers.update_company_profile(sso_session_id=self.request.user.session_id, data=data)
        return Response(status=200)


class ArticleView(GA360Mixin, FormView):
    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='MagnaPage',
            business_unit='MagnaUnit',
            site_section='capability',
        )
    template_name = 'core/article.html'
    success_url = cms_slugs.DASHBOARD_URL
    form_class = forms.NoOperationForm

    def get_context_data(self):
        return super().get_context_data(
            topic_name=self.kwargs['topic'],
            chapter_name=self.kwargs['chapter'],
            article_name=self.kwargs['article'],
            country_choices=[{'value': key, 'label': label} for key, label in choices.COUNTRY_CHOICES],
        )


class LoginView(GA360Mixin, TemplateView):
    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='MagnaPage',
            business_unit='MagnaUnit',
            site_section='login',
        )
    template_name = 'core/login.html'


class SignupView(GA360Mixin, TemplateView):
    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='MagnaPage',
            business_unit='MagnaUnit',
            site_section='signup',
        )
    template_name = 'core/signup.html'


class MarketsView(GA360Mixin, TemplateView):
    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='Markets',
            business_unit='MarketsUnit',
            site_section='markets',
        )

    template_name = 'core/markets.html'

    def get_page_title(self):
        if self.request.user.is_authenticated:
            return helpers.get_markets_page_title(self.request.user.company)

    def get_most_popular_countries(self):
        if self.request.user.is_authenticated and self.request.user.company.expertise_industries_labels:
            return helpers.get_popular_export_destinations(self.request.user.company.expertise_industries_labels[0])

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            page_title=self.get_page_title(),
            most_popular_countries=self.get_most_popular_countries(),
            **kwargs
        )


class TargetMarketView(GA360Mixin, TemplateView):
    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='TargetMarkets',
            business_unit='MagnaUnit',
            site_section='target markets',
        )
    template_name = 'core/target_markets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user and hasattr(self.request.user, 'export_plan'):
            context['export_plan'] = self.request.user.export_plan
        return context


class ProductLookupView(generics.GenericAPIView):
    serializer_class = serializers.ProductLookupSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'tx_id' in serializer.validated_data:
            data = helpers.search_commodity_refine(**serializer.validated_data)
        else:
            data = helpers.search_commodity_by_term(term=serializer.validated_data['q'])
        return Response(data)


class CountriesView(generics.GenericAPIView):

    def get(self, request):
        return Response([c for c in choices.COUNTRIES_AND_TERRITORIES_REGION if c.get('type') == 'Country'])


class SuggestedCountriesView(generics.GenericAPIView):

    def get(self, request):
        hs_code = request.GET.get('hs_code')
        return Response(helpers.get_suggested_countries_by_hs_code(
            sso_session_id=self.request.user.session_id,
            hs_code=hs_code
        ))


def handler404(request, *args, **kwargs):
    return TemplateResponse(
        request=request,
        template='core/404.html',
        context={},
        status=404
    )


def handler500(request, *args, **kwargs):
    return TemplateResponse(
        request=request,
        template='core/500.html',
        context={},
        status=500
    )


class AbstractSignupWizardView(abc.ABC):
    step_labels = (
        'Get tailored content',
        'What are you selling?',
        'Find your product',
        'Sign up',
    )

    @property
    @abc.abstractmethod
    def templates(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def form_list(self):
        raise NotImplementedError

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def done(self, form_list, **kwargs):
        # react component handles the signing up, this wizard is just for data collection that is fed into
        # the react component on the final step, so this step should not be submitted to
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        context = super().get_context_data(step_labels=self.step_labels, **kwargs)
        if self.steps.current == STEP_SIGN_UP:
            context['product_search_data'] = self.get_cleaned_data_for_step(STEP_PRODUCT_SEARCH)
        return context

    def get_step_url(self, step):
        # we want to maintain the querystring params. e.g, next tells the final
        # step where to send the user
        url = super().get_step_url(step)
        if self.request.GET.get('next'):
            querystring = self.request.META['QUERY_STRING']
            if querystring:
                url = f'{url}?{querystring}'
        return url


class SignupForTailoredContentWizardView(GA360Mixin, AbstractSignupWizardView, NamedUrlSessionWizardView):
    extra_context = {'allow_skip_signup': True}
    templates = {
        STEP_START: 'core/signup-wizard-step-start-tailored-content.html',
        STEP_WHAT_SELLING: 'core/signup-wizard-step-what-selling.html',
        STEP_PRODUCT_SEARCH: 'core/signup-wizard-step-product-search.html',
        STEP_SIGN_UP: 'core/signup-wizard-step-sign-up.html',
    }

    form_list = (
        (STEP_START, forms.NoOperationForm),
        (STEP_WHAT_SELLING, forms.WhatAreYouSellingForm),
        (STEP_PRODUCT_SEARCH, forms.ProductSearchForm),
        (STEP_SIGN_UP, forms.NoOperationForm),
    )


class SignupForExportPlanWizardView(GA360Mixin, AbstractSignupWizardView, NamedUrlSessionWizardView):
    extra_context = {'allow_skip_signup': False}
    templates = {
        STEP_START: 'core/signup-wizard-step-start-export-plan.html',
        STEP_WHAT_SELLING: 'core/signup-wizard-step-what-selling.html',
        STEP_PRODUCT_SEARCH: 'core/signup-wizard-step-product-search.html',
        STEP_SIGN_UP: 'core/signup-wizard-step-sign-up.html',
    }

    form_list = (
        (STEP_START, forms.NoOperationForm),
        (STEP_WHAT_SELLING, forms.WhatAreYouSellingForm),
        (STEP_PRODUCT_SEARCH, forms.ProductSearchForm),
        (STEP_SIGN_UP, forms.NoOperationForm),
    )


class CompanyNameFormView(GA360Mixin, FormView):
    def __init__(self):
        super().__init__()
        self.set_ga360_payload(
            page_id='MagnaPage',
            business_unit='MagnaUnit',
            site_section='signup-company-name',
        )
    template_name = 'core/company-name-form.html'
    form_class = forms.CompanyNameForm

    def get_success_url(self):
        return self.request.GET.get('next', cms_slugs.DASHBOARD_URL)

    def form_valid(self, form):
        helpers.update_company_profile(sso_session_id=self.request.user.session_id, data=form.cleaned_data)
        return super().form_valid(form)


class CreateTokenView(generics.GenericAPIView):
    permission_classes = []

    def get(self, request):
        # expire access @ now() in msec + 5 days
        plaintext = str(datetime.datetime.now() + datetime.timedelta(days=5))
        base_url = settings.BASE_URL
        # TODO: logging
        # print(f'token valid until {plaintext}')
        fern = Fern()
        ciphertext = fern.encrypt(plaintext)
        response = {'valid_until': plaintext, 'token': ciphertext, 'CLIENT URL': f'{base_url}/login?enc={ciphertext}'}
        return Response(response)


class CheckView(generics.GenericAPIView):
    def get(self, request):
        response = helpers.search_commodity_by_term(term='feta', json=False)
        try:
            response_code = response.json()['data']['hsCode']
            return Response({'status': status.HTTP_200_OK,
                             'CCCE_API': {'status': status.HTTP_200_OK, 'response_body': response_code,
                                          'elapsed_time': math.floor(response.elapsed.total_seconds() * 1000)}})
        except Exception as e:
            logger.exception(e)
            return Response({'status': status.HTTP_200_OK, 'CCCE_API': {'status': status.HTTP_503_SERVICE_UNAVAILABLE}})


class ContactUsHelpFormView(FormView):
    form_class = forms.ContactUsHelpForm
    template_name = 'core/contact-us-help-form.html'
    success_url = reverse_lazy('core:contact-us-success')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            form_kwargs['initial'] = {
                'email': self.request.user.email,
                'given_name': self.request.user.first_name,
                'family_name': self.request.user.last_name,
            }
        return form_kwargs

    def send_support_message(self, form):
        location = helpers.get_location(self.request)
        sender = Sender(
            email_address=form.cleaned_data['email'],
            country_code=location.get('country') if location else None,
            ip_address=helpers.get_sender_ip_address(self.request),
        )
        response = form.save(
            template_id=settings.CONTACTUS_ENQURIES_SUPPORT_TEMPLATE_ID,
            email_address=settings.GREAT_SUPPORT_EMAIL,
            form_url=self.request.get_full_path(),
            sender=sender,
        )
        response.raise_for_status()

    def send_user_message(self, form):
        # no need to set `sender` as this is just a confirmation email.
        response = form.save(
            template_id=settings.CONTACTUS_ENQURIES_CONFIRMATION_TEMPLATE_ID,
            email_address=form.cleaned_data['email'],
            form_url=self.request.get_full_path(),
        )
        response.raise_for_status()

    def form_valid(self, form):
        self.send_support_message(form)
        self.send_user_message(form)
        return super().form_valid(form)


class ContactUsHelpSuccessView(TemplateView):
    template_name = 'core/contact-us-help-form-success.html'
