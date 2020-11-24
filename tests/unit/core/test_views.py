import json
import pytest

from urllib.parse import urlencode
from unittest import mock
from unittest.mock import patch, Mock

from django.urls import reverse
from django.http.cookie import SimpleCookie
from django.conf import settings

from directory_api_client import api_client
from directory_sso_api_client import sso_api_client
from formtools.wizard.views import normalize_name
from rest_framework import status

from core import forms, helpers, serializers, views, cms_slugs

from tests.helpers import create_response
from tests.unit.core.factories import (
    CuratedListPageFactory,
    DetailPageFactory,
    LessonPlaceholderPageFactory,
    ListPageFactory,
    TopicPageFactory,
)
from tests.unit.learn.factories import LessonPageFactory
from tests.unit.domestic.factories import DomesticDashboardFactory

BETA_AUTH_TOKEN_PAST = 'gAAAAABfCpH53lJcM0TiiXTqD7X18yRoZHOjy-rbSogRxB0v011FMb6rCkMeizffou-z80D9DPL1PWRA7sn9NBrUS' \
                       '-M7FTQeapvntabhj-on62OFlNvzVMQ= '


def submit_step_factory(client, url_name, view_class):
    step_names = iter([name for name, form in view_class.form_list])
    view_name = normalize_name(view_class.__name__)

    def submit_step(data, step_name=None, params={}):
        step_name = step_name or next(step_names)
        path = reverse(url_name, kwargs={'step': step_name})
        # import pdb;pdb.set_trace()
        return client.post(
            path=f'{path}?{urlencode(params, doseq=True)}',
            data={
                view_name + '-current_step': step_name,
                **{step_name + '-' + key: value for key, value in data.items()}
            },
        )
    return submit_step


@pytest.fixture
def submit_signup_tailored_content_wizard_step(client):
    return submit_step_factory(
        client=client,
        url_name='core:signup-wizard-tailored-content',
        view_class=views.SignupForTailoredContentWizardView,
    )


@pytest.fixture
def submit_signup_export_plan_wizard_step(client):
    return submit_step_factory(
        client=client,
        url_name='core:signup-wizard-export-plan',
        view_class=views.SignupForExportPlanWizardView,
    )


@pytest.fixture
def company_data():
    return {
        'expertise_industries': json.dumps(['Science']),
        'expertise_countries': json.dumps(['USA']),
    }


@pytest.fixture
def contact_form_data(captcha_stub):
    return {
        'given_name': 'Test',
        'family_name': 'Example',
        'email': 'test@example.com',
        'comment': 'Help please',
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True,
    }


@pytest.mark.django_db
@mock.patch.object(helpers, 'update_company_profile')
def test_api_update_company_success(mock_update_company_profile, mock_get_company_profile, client, user, company_data):
    mock_update_company_profile.return_value = create_response()
    mock_get_company_profile.return_value = {'foo': 'bar'}
    client.force_login(user)

    response = client.post(reverse('core:api-update-company'), company_data)
    assert response.status_code == 200
    assert mock_update_company_profile.call_count == 1
    assert mock_update_company_profile.call_args == mock.call(
        data={
            'expertise_industries': ['Science'],
            'expertise_countries': ['USA'],
        },
        sso_session_id=user.session_id,
    )


@pytest.mark.django_db
def test_api_update_company_too_many_companies(client, user):
    company_data = {
        'expertise_countries': json.dumps(['USA', 'China', 'Australia', 'New Zealand']),
    }

    client.force_login(user)

    response = client.post(reverse('core:api-update-company'), company_data)

    assert response.status_code == 400
    assert response.json() == {
        'expertise_countries': [serializers.CompanySerializer.MESSAGE_TOO_MANY_COUNTRIES],
    }


@pytest.mark.django_db
@mock.patch.object(helpers, 'update_company_profile')
def test_api_update_company_no_name(mock_update_company_profile, mock_get_company_profile, client, user, company_data):
    mock_update_company_profile.return_value = create_response()
    mock_get_company_profile.return_value = {}
    client.force_login(user)

    response = client.post(reverse('core:api-update-company'), company_data)

    assert response.status_code == 200
    assert mock_update_company_profile.call_count == 1
    assert mock_update_company_profile.call_args == mock.call(
        data={
            'name': 'unnamed sso-1 company',
            'expertise_industries': ['Science'],
            'expertise_countries': ['USA'],
        },
        sso_session_id=user.session_id,
    )


@pytest.mark.django_db
def test_api_update_company_not_logged_in(client, company_data):
    response = client.post(reverse('core:api-update-company'), company_data)

    assert response.status_code == 403


@pytest.mark.django_db
@mock.patch.object(api_client.personalisation, 'events_by_location_list')
@mock.patch.object(api_client.personalisation, 'export_opportunities_by_relevance_list')
@mock.patch.object(sso_api_client.user, 'get_user_lesson_completed')
def test_dashboard_page_logged_in(
    mock_get_user_lesson_completed,
    mock_events_by_location_list,
    mock_export_opportunities_by_relevance_list,
    patch_set_user_page_view,
    patch_get_user_page_views,
    mock_get_company_profile,
    domestic_homepage,
    domestic_dashboard,
    client,
    user
):
    mock_get_user_lesson_completed.return_value = create_response(json_body={'results': []})
    mock_events_by_location_list.return_value = create_response(json_body={'results': []})
    mock_export_opportunities_by_relevance_list.return_value = create_response(json_body={'results': []})
    client.force_login(user)
    response = client.get(cms_slugs.DASHBOARD_URL)
    assert response.status_code == 200


@pytest.mark.django_db
def test_dashboard_page_not_logged_in(
    domestic_homepage,
    domestic_dashboard,
    client,
    user
):
    response = client.get(cms_slugs.DASHBOARD_URL)
    assert response.status_code == 302
    assert response.url == cms_slugs.LOGIN_URL


@pytest.mark.django_db
@mock.patch.object(api_client.personalisation, 'events_by_location_list')
@mock.patch.object(api_client.personalisation, 'export_opportunities_by_relevance_list')
@mock.patch.object(sso_api_client.user, 'get_user_lesson_completed')
def test_dashboard_page_lesson_progress(
    mock_get_user_lesson_completed,
    mock_export_opportunities_by_relevance_list,
    mock_events_by_location_list,
    patch_set_user_page_view,
    patch_get_user_page_views,
    patch_export_plan,
    mock_get_company_profile,
    client,
    user,
    get_request,
    domestic_homepage,
    domestic_site
):
    mock_events_by_location_list.return_value = create_response(json_body={'results': []})
    mock_export_opportunities_by_relevance_list.return_value = create_response(json_body={'results': []})
    client.force_login(user)

    # given the user has read some lessons
    section_one = ListPageFactory(parent=domestic_homepage, slug='section-one', record_read_progress=True)
    section_two = ListPageFactory(parent=domestic_homepage, slug='section-two', record_read_progress=True)

    module_one = CuratedListPageFactory(parent=section_one, slug='section-one-module-one')
    module_two = CuratedListPageFactory(parent=section_two, slug='section-two-module-one')
    CuratedListPageFactory(parent=section_two, slug='section-two-module-two')

    topic_1_1 = TopicPageFactory(parent=module_one, title='Module one, first topic block')
    topic_1_2 = TopicPageFactory(parent=module_one, title='Module one, second topic block')

    topic_2_1 = TopicPageFactory(parent=module_two, title='Module two, first topic block')
    topic_2_2 = TopicPageFactory(parent=module_two, title='Module two, second topic block')

    # Section 1 Module 1 Topic 1 gets two children
    lesson_one = DetailPageFactory(
        parent=topic_1_1,
        slug='lesson-one',
    )
    LessonPlaceholderPageFactory(
        title='Placeholder To Show They Do Not Interfere With Counts',
        parent=topic_1_1,
    )

    # Section 1 Module 1 Topic 2 gets one child
    lesson_two = DetailPageFactory(
        parent=topic_1_2,
        slug='lesson-two',
    )

    # Section 1 Module 2 Topic 1 gets two children
    DetailPageFactory(
        parent=topic_2_1,
        slug='lesson-three',
    )
    DetailPageFactory(
        parent=topic_2_1,  # ie, in same topic block as one above
        slug='lesson-four',
    )

    # Section 1 Module 2 Topic 2 children
    LessonPlaceholderPageFactory(
        title='Another Placeholder To Show They Do Not Interfere With Counts',
        parent=topic_2_2,
    )
    lesson_five = DetailPageFactory(
        parent=topic_2_2,  # correct
        slug='lesson-five',
    )

    # create dashboard
    dashboard = DomesticDashboardFactory(parent=domestic_homepage, slug='dashboard')

    mock_get_user_lesson_completed.return_value = create_response(json_body={'result': 'ok', 'lesson_completed': [
        {'lesson': lesson_one.id},
        {'lesson': lesson_two.id},
    ]})

    context_data = dashboard.get_context(get_request)
    # check the progress
    assert len(context_data['module_pages']) == 2
    assert context_data['module_pages'][0]['page'].id == module_one.id
    assert context_data['module_pages'][1]['page'].id == module_two.id
    assert context_data['module_pages'][0]['total_pages'] == 2
    assert context_data['module_pages'][1]['total_pages'] == 3
    assert context_data['module_pages'][0]['completion_count'] == 2
    assert context_data['module_pages'][0]['completed_lesson_pages'] == {
        topic_1_1.id: set([lesson_one.id]),
        topic_1_2.id: set([lesson_two.id]),
    }
    assert context_data['module_pages'][1]['completion_count'] == 0
    assert context_data['module_pages'][1]['completed_lesson_pages'] == {}

    mock_get_user_lesson_completed.return_value = create_response(json_body={'result': 'ok', 'lesson_completed': [
        {'lesson': lesson_one.id},
        {'lesson': lesson_two.id},
        {'lesson': lesson_five.id}
    ]})

    context_data = dashboard.get_context(get_request)
    # WARNING! The topics should swap round as two is in progress
    # and has more unread than one
    assert context_data['module_pages'][0]['page'].id == module_two.id
    assert context_data['module_pages'][1]['page'].id == module_one.id
    assert context_data['module_pages'][0]['completion_count'] == 1
    assert context_data['module_pages'][0]['completed_lesson_pages'] == {
        topic_2_2.id: set([lesson_five.id]),
    }
    assert context_data['module_pages'][1]['completion_count'] == 2
    assert context_data['module_pages'][1]['completed_lesson_pages'] == {
        topic_1_1.id: set([lesson_one.id]),
        topic_1_2.id: set([lesson_two.id]),
    }


@pytest.mark.django_db
def test_dashboard_apis_ok(
    client,
    user,
    get_request,
    patch_get_dashboard_events,
    patch_get_dashboard_export_opportunities,
    patch_set_user_page_view,
    patch_get_user_page_views,
    patch_get_user_lesson_completed,
    domestic_homepage
):
    patch_get_dashboard_events.stop()
    patch_get_dashboard_export_opportunities.stop()

    with patch(
        'directory_api_client.api_client.personalisation.events_by_location_list'
    ) as events_api_results:
        events_api_results.return_value = Mock(status_code=200, **{'json.return_value': {
            'results': [{
                'name': 'Global Aid and Development Directory',
                'content': 'DIT is producing a directory of companies \
who supply, or would like to supply, relevant humanitarian aid \
and development products and services to the United Nations \
family of organisations and NGOs.  ',
                'location': {'city': 'London'},
                'url': 'www.example.com',
                'date': '2020-06-06'
            }, {
                'name': 'Less Info',
                'content': 'Content',
                'url': 'www.example.com',
            }]
        }})

        with patch(
            'directory_api_client.api_client.\
personalisation.export_opportunities_by_relevance_list'
        ) as exops_api_results:
            exops_api_results.return_value = Mock(status_code=200, **{'json.return_value': {
                'results': [{'title': 'French sardines required',
                             'url': 'http://exops.trade.great:3001/\
export-opportunities/opportunities/french-sardines-required',
                             'description': 'Nam dolor nostrum distinctio.Et quod itaque.',
                             'published_date': '2020-01-14T15:26:45.334Z',
                             'closing_date': '2020-06-06',
                             'source': 'post'}]
            }})

            client.force_login(user)

            dashboard = DomesticDashboardFactory(parent=domestic_homepage, slug='dashboard')
            context_data = dashboard.get_context(get_request)

            assert context_data['events'] == [{
                'title': 'Global Aid and Development Directory',
                'description': 'DIT is producing a directory of compani…',
                'url': 'www.example.com',
                'location': 'London',
                'date': '06 Jun 2020'
            }, {
                'title': 'Less Info',
                'description': 'Content',
                'url': 'www.example.com',
                'location': 'n/a',
                'date': 'n/a'
            }]
            assert context_data['export_opportunities'] == [{
                'title': 'French sardines required',
                'description': 'Nam dolor nostrum distinctio.…',
                'source': 'post',
                'url': 'http://exops.trade.great:3001/export-opportunities\
/opportunities/french-sardines-required',
                'published_date': '14 Jan 2020',
                'closing_date': '06 Jun 2020'
            }]


@pytest.mark.django_db
def test_dashboard_apis_fail(
        client,
        user,
        get_request,
        patch_get_dashboard_events,
        patch_get_dashboard_export_opportunities,
        patch_set_user_page_view,
        patch_get_user_page_views,
        patch_get_user_lesson_completed,
        domestic_homepage
):
    patch_get_dashboard_events.stop()
    patch_get_dashboard_export_opportunities.stop()
    patch_get_user_lesson_completed.stop()
    with patch(
        'directory_api_client.api_client.personalisation.events_by_location_list'
    ) as events_api_results:
        events_api_results.return_value = Mock(status_code=500, **{'json.return_value': {}})

        with patch(
            'directory_api_client.api_client.\
personalisation.export_opportunities_by_relevance_list'
        ) as exops_api_results:
            exops_api_results.return_value = Mock(status_code=500, **{'json.return_value': {}})

            client.force_login(user)
            dashboard = DomesticDashboardFactory(parent=domestic_homepage, slug='dashboard')
            context_data = dashboard.get_context(get_request)

            assert context_data['events'] == []
            assert context_data['export_opportunities'] == []


@pytest.mark.django_db
def test_capability_article_logged_in(client, user):
    client.force_login(user)
    url = reverse(
        'core:capability-article', kwargs={'topic': 'some topic', 'chapter': 'some chapter', 'article': 'some article'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['topic_name'] == 'some topic'
    assert response.context_data['chapter_name'] == 'some chapter'
    assert response.context_data['article_name'] == 'some article'


@pytest.mark.django_db
def test_capability_article_not_logged_in(client):

    url = reverse(
        'core:capability-article',
        kwargs={'topic': 'some-topic', 'chapter': 'some-chapter', 'article': 'some-article'}
    )

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == f'{cms_slugs.LOGIN_URL}?next={url}'


@pytest.mark.django_db
def test_login_page_not_logged_in(client):
    url = reverse('core:login')

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_page_logged_in(client, user):
    client.force_login(user)
    url = reverse('core:login')

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == cms_slugs.DASHBOARD_URL


@pytest.mark.django_db
@mock.patch.object(helpers, 'get_markets_page_title')
def test_markets_logged_in(mock_get_markets_page_title, mock_get_company_profile, user, client):
    mock_get_markets_page_title.return_value = 'Some page title'
    mock_get_company_profile.return_value = {
        'expertise_countries': ['AF'],
        'expertise_industries': ['SL10001'],
        'expertise_products_services': {},
    }
    client.force_login(user)
    url = reverse('core:markets')

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['page_title'] == 'Some page title'
    assert len(response.context_data['most_popular_countries']) == 5


@pytest.mark.django_db
def test_markets_not_logged_in(mock_get_company_profile, client):
    url = reverse('core:markets')

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['page_title'] is None
    assert response.context_data['most_popular_countries'] is None


@pytest.mark.django_db
@mock.patch.object(helpers, 'search_commodity_by_term')
def test_search_commodity_by_term(mock_search_commodity_by_term, client):
    mock_search_commodity_by_term.return_value = data = [
        {'value': '123323', 'label': 'some description'},
        {'value': '223323', 'label': 'some other description'},
    ]
    term = 'some term'

    response = client.post(reverse('core:api-lookup-product'), {'proddesc': term})

    assert response.status_code == 200
    assert response.json() == data
    assert mock_search_commodity_by_term.call_count == 1
    assert mock_search_commodity_by_term.call_args == mock.call(term=term)


@pytest.mark.django_db
@mock.patch.object(helpers, 'search_commodity_refine')
def test_refine_commodity(mock_search_commodity_refine, client):
    mock_search_commodity_refine.return_value = data = [
        {'value': '123323', 'label': 'some description'},
        {'value': '223323', 'label': 'some other description'},
    ]

    response = client.post(reverse('core:api-lookup-product'), {
        'interaction_id': 1234, 'tx_id': 1234, 'value_id': 1234, 'value_string': 'processed'
    })

    assert response.status_code == 200
    assert response.json() == data
    assert mock_search_commodity_refine.call_count == 1


@pytest.mark.django_db
def test_get_countries(client):
    response = client.get(reverse('core:api-countries'))
    countries = response.json()
    assert response.status_code == 200
    assert len(countries) > 190
    assert 'id' in countries[0]
    assert 'name' in countries[0]
    assert 'region' in countries[0]


@pytest.mark.django_db
@mock.patch.object(helpers, 'get_suggested_countries_by_hs_code')
def test_get_suggested_countries(mock_get_suggested_countries_by_hs_code, client, user):
    data = [
        {'hs_code': 4, 'country_name': 'Sweden', 'country_iso2': 'SE', 'region': 'Europe'},
        {'hs_code': 4, 'country_name': 'Spain', 'country_iso2': 'ES', 'region': 'Europe'}
    ]
    mock_get_suggested_countries_by_hs_code.return_value = data

    client.force_login(user)
    response = client.get(reverse('core:api-suggested-countries'), data={'hs_code': '20'})
    assert response.status_code == 200
    assert response.json() == data


@pytest.mark.django_db
def test_list_page_uses_right_template(domestic_homepage, rf, user):
    request = rf.get('/')
    request.user = user
    topic_page = CuratedListPageFactory(parent=domestic_homepage)
    lesson_page = LessonPageFactory(parent=topic_page)
    response = lesson_page.serve(request)
    assert response.template_name == 'learn/detail_page.html'


@pytest.mark.django_db
def test_handler404(client, settings):
    response = client.get('/hey-kid-do-a-kickflip/')

    assert response.template_name == 'core/404.html'
    assert response.status_code == 404


@pytest.fixture
def signup_wizard_steps_data():
    return {
        views.STEP_START: {},
        views.STEP_WHAT_SELLING: {'choice': forms.WhatAreYouSellingForm.PRODUCTS},
        views.STEP_PRODUCT_SEARCH: {'products': 'Sharks,Crayons'},
        views.STEP_SIGN_UP: {},
    }


@pytest.mark.django_db
def test_signup_wizard_for_tailored_content_success(
    submit_signup_tailored_content_wizard_step, signup_wizard_steps_data, client
):
    response = submit_signup_tailored_content_wizard_step(signup_wizard_steps_data[views.STEP_START])
    assert response.status_code == 302

    response = submit_signup_tailored_content_wizard_step(signup_wizard_steps_data[views.STEP_WHAT_SELLING])
    assert response.status_code == 302

    response = submit_signup_tailored_content_wizard_step(signup_wizard_steps_data[views.STEP_PRODUCT_SEARCH])
    assert response.status_code == 302

    response = submit_signup_tailored_content_wizard_step(signup_wizard_steps_data[views.STEP_SIGN_UP])
    assert response.status_code == 302

    # note that the react component handles the logging in, so no need to submit the last step here,
    with pytest.raises(NotImplementedError):
        client.get(response.url)


@pytest.mark.django_db
def test_signup_wizard_for_tailored_content_step_labels_exposed(client):

    response = client.get(reverse('core:signup-wizard-tailored-content', kwargs={'step': views.STEP_START}))
    assert response.context_data['step_labels'] == views.SignupForTailoredContentWizardView.step_labels

    response = client.get(reverse('core:signup-wizard-tailored-content', kwargs={'step': views.STEP_WHAT_SELLING}))
    assert response.context_data['step_labels'] == views.SignupForTailoredContentWizardView.step_labels

    response = client.get(reverse('core:signup-wizard-tailored-content', kwargs={'step': views.STEP_PRODUCT_SEARCH}))
    assert response.context_data['step_labels'] == views.SignupForTailoredContentWizardView.step_labels

    response = client.get(reverse('core:signup-wizard-tailored-content', kwargs={'step': views.STEP_SIGN_UP}))
    assert response.context_data['step_labels'] == views.SignupForTailoredContentWizardView.step_labels


@pytest.mark.django_db
def test_signup_wizard_for_tailored_content_exposes_product_on_final_step(
    submit_signup_tailored_content_wizard_step, signup_wizard_steps_data, client
):
    search_data = signup_wizard_steps_data[views.STEP_PRODUCT_SEARCH]

    response = submit_signup_tailored_content_wizard_step(signup_wizard_steps_data[views.STEP_START])
    assert response.status_code == 302

    response = submit_signup_tailored_content_wizard_step(signup_wizard_steps_data[views.STEP_WHAT_SELLING])
    assert response.status_code == 302

    response = submit_signup_tailored_content_wizard_step(search_data)
    assert response.status_code == 302

    response = client.get(response.url)
    assert response.context_data['product_search_data'] == search_data


@pytest.mark.django_db
def test_signup_wizard_for_tailored_content_next_url(
    submit_signup_tailored_content_wizard_step, signup_wizard_steps_data
):
    response = submit_signup_tailored_content_wizard_step(
        data=signup_wizard_steps_data[views.STEP_START],
        params={'next': '/foo/bar/'},
    )
    assert response.status_code == 302
    assert response.url == '/signup/tailored-content/what-are-you-selling/?next=%2Ffoo%2Fbar%2F'

    response = submit_signup_tailored_content_wizard_step(
        data=signup_wizard_steps_data[views.STEP_WHAT_SELLING],
        params={'next': '/foo/bar/'},
    )
    assert response.status_code == 302
    assert response.url == '/signup/tailored-content/product-search/?next=%2Ffoo%2Fbar%2F'

    response = submit_signup_tailored_content_wizard_step(
        data=signup_wizard_steps_data[views.STEP_PRODUCT_SEARCH],
        params={'next': '/foo/bar/'},
    )
    assert response.status_code == 302
    assert response.url == '/signup/tailored-content/sign-up/?next=%2Ffoo%2Fbar%2F'


@pytest.mark.django_db
@mock.patch.object(helpers, 'update_company_profile')
def test_set_company_name_success(mock_update_company_profile, mock_get_company_profile, client, user):
    mock_update_company_profile.return_value = create_response()
    mock_get_company_profile.return_value = {'foo': 'bar'}
    client.force_login(user)

    response = client.post(reverse('core:set-company-name'), {'name': 'Example corp'})
    assert response.status_code == 302
    assert response.url == cms_slugs.DASHBOARD_URL
    assert mock_update_company_profile.call_count == 1
    assert mock_update_company_profile.call_args == mock.call(
        data={'name': 'Example corp'},
        sso_session_id=user.session_id,
    )


@pytest.mark.django_db
@mock.patch.object(helpers, 'update_company_profile')
def test_set_company_name_success_with_next(mock_update_company_profile, mock_get_company_profile, client, user):
    mock_update_company_profile.return_value = create_response()
    mock_get_company_profile.return_value = {'foo': 'bar'}
    client.force_login(user)

    url = reverse('core:set-company-name')
    response = client.post(f'{url}?next=/foo/bar/', {'name': 'Example corp'})
    assert response.status_code == 302
    assert response.url == '/foo/bar/'


@pytest.mark.django_db
def test_create_api_token(client, rf):
    response = client.get('/api/create-token/')
    assert response.data is not None
    assert response.status_code == 200


@pytest.mark.django_db
def test_auth_with_url(client, rf):
    response = client.get('/api/create-token/')
    token = response.data['token']

    response_2 = client.get(f'/markets/?enc={token}')
    assert response_2.status_code == 200


@pytest.mark.django_db
def test_auth_with_cookie(client, rf):
    response = client.get('/api/create-token/')
    token = response.data['token']

    response_2 = client.get(f'/markets/?enc={token}')
    assert response_2.status_code == 200

    response_3 = client.get('/markets/')
    assert response_3.status_code == 200


@pytest.mark.django_db
def test_bad_auth_with_url(client):
    response = client.get('/markets/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_bad_auth_with_cookie(client):
    client.cookies = SimpleCookie({'beta-user': BETA_AUTH_TOKEN_PAST})
    response = client.get('/markets/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_bad_auth_with_enc_token(client):
    response = client.get(f'/markets/?enc={BETA_AUTH_TOKEN_PAST}')
    assert response.status_code == 403


@pytest.mark.django_db
@mock.patch.object(helpers, 'search_commodity_by_term')
def test_check_view(mock_search_commodity_by_term, client):
    # mock the API response with the wrong hs code. Make sure we dont hit the actual API endpoint in every test run.
    mock_search_commodity_by_term.return_value = create_response(json_body={'data': {'hsCode': '923311'}})

    res = client.get('/api/check/').json()

    assert res['CCCE_API']['response_body'] == '923311'
    assert res['CCCE_API']['status'] == status.HTTP_200_OK
    assert res['status'] == status.HTTP_200_OK
    assert mock_search_commodity_by_term.call_count == 1


@pytest.mark.django_db
@mock.patch.object(helpers, 'search_commodity_by_term')
def test_check_view_external_error(mock_search_commodity_by_term, client):
    test_http_error = status.HTTP_504_GATEWAY_TIMEOUT
    # the external API is down
    mock_search_commodity_by_term.return_value = create_response(status_code=test_http_error)

    res = client.get('/api/check/').json()

    assert res['CCCE_API']['status'] == test_http_error
    assert res['status'] == status.HTTP_200_OK
    assert mock_search_commodity_by_term.call_count == 1


@pytest.mark.django_db
def test_target_market_page(
    patch_export_plan,
    domestic_homepage,
    client,
    user
):
    client.force_login(user)
    url = reverse('core:target-market')

    response = client.get(url)

    # Check that the page renders even if there is no dashboard definition in wagtail
    assert response.status_code == 200
    assert response.context_data['dashboard_components'] is None

    # Populate dashboard with a couple of routes and check context
    DomesticDashboardFactory(
        parent=domestic_homepage,
        slug='dashboard',
        components__0__route__route_type='learn',
        components__0__route__title='Learning title',
        components__0__route__body='Learning Body Text',
        components__0__route__button={'label': 'Start learning'},
        components__1__route__route_type='plan',
        components__1__route__title='Planning title',
        components__1__route__body='Planning Body Text',
        components__1__route__button={'label': 'Start planning'}
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.context_data['dashboard_components'][0].value['route_type'] == 'learn'
    assert response.context_data['dashboard_components'][1].value['route_type'] == 'plan'


@pytest.mark.django_db
def test_contact_us_form_prepopualate(client, user):
    client.force_login(user)
    url = reverse('core:contact-us-help')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context_data['form'].initial == {
        'email': user.email,
        'family_name': user.last_name,
        'given_name': user.first_name,
    }


@pytest.mark.parametrize('get_location_value', [{'country': 'UK'}, None])
@pytest.mark.django_db
@mock.patch.object(helpers, 'get_location')
@mock.patch.object(views.ContactUsHelpFormView.form_class, 'save')
def test_contact_us_help_notify_save_success(
        mock_save, mock_get_location, client, get_location_value, contact_form_data
):
    mock_get_location.return_value = get_location_value
    url = reverse('core:contact-us-help')
    response = client.post(url, contact_form_data)

    assert response.status_code == 302
    assert response.url == reverse('core:contact-us-success')
    assert mock_save.call_count == 2
    assert mock_save.call_args_list == [
        mock.call(
            email_address=settings.GREAT_SUPPORT_EMAIL,
            form_url='/contact-us/help/',
            sender={
                'email_address': contact_form_data['email'],
                'country_code': get_location_value['country'] if get_location_value else None,
                'ip_address': '127.0.0.1'
            },
            template_id=settings.CONTACTUS_ENQURIES_SUPPORT_TEMPLATE_ID
        ),
        mock.call(
            email_address=contact_form_data['email'],
            form_url='/contact-us/help/',
            template_id=settings.CONTACTUS_ENQURIES_CONFIRMATION_TEMPLATE_ID
        )
    ]
