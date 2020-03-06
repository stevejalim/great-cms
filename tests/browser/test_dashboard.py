import random
from unittest import mock

import allure
import pytest
from selenium.webdriver.common.keys import Keys

from core import helpers
from tests.helpers import create_response
from tests.browser.common_selectors import (
    DashboardModalLetsGetToKnowYou
)
from tests.browser.util import (
    attach_jpg_screenshot,
    find_element,
    is_element_visible
)

pytestmark = pytest.mark.browser

industry_options = [
    'Advanced Engineering',
    'Aerospace',
    'Agriculture, Horticulture and Fisheries',
    'Airports',
    'Automotive',
    'Biotechnology & Pharmaceuticals',
    'Chemicals',
    'Construction',
    'Consumer, Retail and Luxury',
    'Creative and Media',
    'Cyber Security',
    'Defence',
    'Education & Training',
    'Energy',
    'Environment',
    'Financial & Professional Services',
    'Food & Drink',
    'Healthcare & Medical',
    'Leisure & Tourism',
    'Life Sciences',
    'Maritme',
    'Mining',
    'Railways',
    'Security',
    'Space',
    'Sports Economy',
    'Technology & Smart Cities',
    'Water',
]


@allure.step('Should see all elements from: {selectors_enum}')
def should_see_all_elements(browser, selectors_enum):
    for selector in selectors_enum:
        if not selector.is_visible:
            continue
        error = f'Expected element "{selector}" is not visible'
        assert is_element_visible(browser, selector), error


@allure.step('Enter sectors user is interested in: {industries}')
def submit_industries(browser, industries):
    industries_input = find_element(
        browser, DashboardModalLetsGetToKnowYou.INDUSTRIES_INPUT
    )
    for industry in industries:
        industries_input.send_keys(industry)
        industries_input.send_keys(Keys.ENTER)

    attach_jpg_screenshot(
        browser,
        'After entering industries',
        selector=DashboardModalLetsGetToKnowYou.MODAL
    )

    continue_button = find_element(browser, DashboardModalLetsGetToKnowYou.SUBMIT)
    continue_button.click()


@allure.step('Should not see elements from: {selectors_enum}')
def should_not_see(browser, selectors_enum):
    for selector in selectors_enum:
        if not selector.is_visible:
            continue
        error = f'Unexpected element is visible: "{selector}"'
        try:
            assert not is_element_visible(browser, selector), error
        except AssertionError:
            attach_jpg_screenshot(browser, error, selector=selector)
            raise


@pytest.mark.django_db
@mock.patch.object(helpers, 'create_company_profile')
def test_dashboard_forced_user(mock_create_company_profile, mock_get_company_profile, server_user_browser_dashboard):

    def side_effect():
        mock_get_company_profile.return_value = {'foo': 'bar'}

    mock_create_company_profile.return_value = create_response()
    mock_create_company_profile.side_effect = side_effect
    live_server, user, browser = server_user_browser_dashboard

    should_see_all_elements(browser, DashboardModalLetsGetToKnowYou)

    industries = random.sample(industry_options, random.randint(1, 5))
    submit_industries(browser, industries)

    should_not_see(browser, DashboardModalLetsGetToKnowYou)
    attach_jpg_screenshot(browser, 'Dashboard')
