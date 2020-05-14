from unittest import mock

import pytest

from django.contrib.auth.models import AnonymousUser

from core import helpers, middleware
from tests.unit.core import factories


@pytest.fixture(autouse=True)
def mock_company_profile(mock_get_company_profile):
    mock_get_company_profile.return_value = {
        'expertise_products_services': {'other': ['Vodka']},
        'expertise_countries': [],
        'expertise_industries': [],
    }
    return mock_get_company_profile


@mock.patch.object(helpers, 'store_user_location')
def test_stores_user_location(mock_store_user_location, rf, user):
    request = rf.get('/')
    request.user = user

    middleware.UserLocationStoreMiddleware().process_request(request)

    assert mock_store_user_location.call_count == 1
    assert mock_store_user_location.call_args == mock.call(request)


@mock.patch.object(helpers, 'store_user_location')
def test_stores_user_location_anon_user(mock_store_user_location, rf):
    request = rf.get('/')
    request.user = AnonymousUser()

    middleware.UserLocationStoreMiddleware().process_request(request)

    assert mock_store_user_location.call_count == 0


@pytest.mark.django_db
def test_user_specific_redirect_middleware(domestic_site, client):
    learn_page = factories.ListPageFactory(parent=domestic_site.root_page, slug='learn')
    introduction_page = factories.DetailPageFactory(parent=learn_page, slug='introduction')
    categories_page = factories.DetailPageFactory(parent=learn_page, slug='categories')

    # Given the user has gone to /learn/inroduction/
    response = client.get(introduction_page.url)
    assert response.status_code == 200

    # When the user next goes to /learn/ or /learn/inroduction/
    for page in [learn_page, introduction_page]:
        response = client.get(page.url)

        # Then they should be redirected to /learn/categories/
        assert response.status_code == 302
        assert response.url == categories_page.url


@pytest.mark.django_db
def test_user_product_expertise_middleware(domestic_site, client, mock_update_company_profile, user):
    client.force_login(user)

    topic_page = factories.ListPageFactory(parent=domestic_site.root_page)
    lesson_page = factories.DetailPageFactory(parent=topic_page)

    response = client.get(
        lesson_page.url,
        {'product': ['Vodka', 'Potassium'], 'remember-expertise-products-services': True}
    )
    assert response.status_code == 200
    assert mock_update_company_profile.call_count == 1
    assert mock_update_company_profile.call_args == mock.call(
        sso_session_id=user.session_id,
        data={'expertise_products_services': {'other': ['Vodka', 'Potassium']}}
    )


@pytest.mark.django_db
def test_user_product_expertise_middleware_no_company(
    domestic_site, client, mock_update_company_profile, user, mock_get_company_profile
):
    mock_get_company_profile.return_value = None
    client.force_login(user)

    topic_page = factories.ListPageFactory(parent=domestic_site.root_page)
    lesson_page = factories.DetailPageFactory(parent=topic_page)

    response = client.get(
        lesson_page.url,
        {'product': ['Vodka', 'Potassium'], 'remember-expertise-products-services': True}
    )
    assert response.status_code == 200
    assert mock_update_company_profile.call_count == 1
    assert mock_update_company_profile.call_args == mock.call(
        sso_session_id=user.session_id,
        data={'expertise_products_services': {'other': ['Vodka', 'Potassium']}}
    )


@pytest.mark.django_db
def test_user_product_expertise_middleware_not_logged_in(domestic_site, client, mock_update_company_profile):
    topic_page = factories.ListPageFactory(parent=domestic_site.root_page)
    lesson_page = factories.DetailPageFactory(parent=topic_page)

    response = client.get(
        lesson_page.url,
        {'product': ['Vodka', 'Potassium'], 'remember-expertise-products-services': True}
    )
    assert response.status_code == 200
    assert mock_update_company_profile.call_count == 0


@pytest.mark.django_db
def test_user_product_expertise_middleware_not_store(domestic_site, client, mock_update_company_profile, user):
    client.force_login(user)

    topic_page = factories.ListPageFactory(parent=domestic_site.root_page)
    lesson_page = factories.DetailPageFactory(parent=topic_page)

    response = client.get(
        lesson_page.url,
        {'product': ['Vodka', 'Potassium']}
    )
    assert response.status_code == 200
    assert mock_update_company_profile.call_count == 0


@pytest.mark.django_db
def test_user_product_expertise_middleware_not_store_idempotent(
    domestic_site, client, mock_update_company_profile, user
):
    client.force_login(user)

    topic_page = factories.ListPageFactory(parent=domestic_site.root_page)
    lesson_page = factories.DetailPageFactory(parent=topic_page)

    response = client.get(
        lesson_page.url,
        {'product': ['Vodka'], 'remember-expertise-products-services': True}
    )
    assert response.status_code == 200
    assert mock_update_company_profile.call_count == 0
