from django.urls import path, reverse_lazy
from django.contrib.auth.decorators import login_required
from great_components.decorators import skip_ga360

from exportplan import views, api

LOGIN_URL = reverse_lazy('core:login')

app_name = 'exportplan'

urlpatterns = [
    path('section/marketing-approach/', skip_ga360(views.ExportPlanMarketingApproachView.as_view()),
         name='marketing-approach'),
    path('logo', skip_ga360(views.LogoFormView.as_view()), name='add-logo'),
    path(
        'section/target-markets/',
        login_required(skip_ga360(views.ExportPlanTargetMarketsView.as_view()), login_url=LOGIN_URL),
        {'slug': 'target-markets'},
        name='target-markets'
    ),
    path(
        'section/adaptation-for-target-market/',
        login_required(views.ExportPlanAdaptationForTargetMarketView.as_view(), login_url=LOGIN_URL),
        {'slug': 'adaptation-for-target-market'},
        name='adaptation-for-target-market'
    ),
    path(
        'section/about-your-business/',
        login_required(skip_ga360(views.ExportPlanAboutYourBusinessView.as_view()), login_url=LOGIN_URL),
        {'slug': 'about-your-business'},
        name='about-your-business'
    ),
    path(
        'section/target-markets-research/',
        login_required(skip_ga360(views.ExportPlanTargetMarketsResearchView.as_view()), login_url=LOGIN_URL),
        {'slug': 'target-markets-research'},
        name='target-markets-research'
    ),
    path(
        'section/objectives/',
        login_required(skip_ga360(views.ExportPlanBusinessObjectivesView.as_view()), login_url=LOGIN_URL),
        {'slug': 'objectives'},
        name='objectives'
    ),
    path(
        'section/<slug:slug>/',
        login_required(skip_ga360(views.ExportPlanSectionView.as_view()), login_url=LOGIN_URL),
        name='section'
    ),
    path(
        'logo',
        login_required(skip_ga360(views.LogoFormView.as_view()), login_url=LOGIN_URL),
        name='add-logo'
    ),
    path(
        'api/recommended-countries/',
        login_required(skip_ga360(api.ExportPlanRecommendedCountriesDataView.as_view()), login_url=LOGIN_URL),
        name='ajax-recommended-countries-data'
    ),
    path('api/export-plan/', skip_ga360(api.UpdateExportPlanAPIView.as_view()), name='api-update-export-plan'),
    path('api/remove-country-data/', skip_ga360(api.ExportPlanRemoveCountryDataView.as_view()),
         name='api-remove-country-data'),
    path('api/remove-sector/', skip_ga360(api.ExportPlanRemoveSectorView.as_view()), name='api-remove-sector'),
    path('api/country-data/', skip_ga360(api.ExportPlanCountryDataView.as_view()), name='api-country-data'),
    path('api/marketing-country-data/', skip_ga360(api.RetrieveMarketingCountryData.as_view()),
         name='api-marketing-country-data'),
    path('api/objectives/create/', skip_ga360(api.ObjectivesCreateAPIView.as_view()), name='api-objectives-create'),
    path('api/objectives/update/', skip_ga360(api.ObjectivesUpdateAPIView.as_view()), name='api-objectives-update'),
    path('api/objectives/delete/', skip_ga360(api.ObjectivesDestroyAPIView.as_view()), name='api-objectives-delete'),
    path('api/route-to-markets/create/', skip_ga360(api.RouteToMarketsCreateAPIView.as_view()),
         name='api-route-to-markets-create'),
    path('api/route-to-markets/update/', skip_ga360(api.RouteToMarketsUpdateAPIView.as_view()),
         name='api-route-to-markets-update'),
    path(
        'api/route-to-markets/delete/', skip_ga360(api.RouteToMarketsDestroyAPIView.as_view()),
        name='api-route-to-markets-delete'
    ),
]
