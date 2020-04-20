import logging
from unittest import mock
from unittest.mock import patch
from urllib.parse import urljoin

import allure
import pytest
from django.urls import reverse

from core import helpers as core_helpers
from exportplan import helpers as exportplan_helpers
from tests.browser.common_selectors import (
    ExportPlanTargetMarketsData,
    ExportPlanTargetMarketsRecommendedCountriesFolded,
    TargetMarketsCountryChooser,
    TargetMarketsSectorSelectorUnfolded,
)
from tests.browser.util import (
    attach_jpg_screenshot,
    selenium_action,
    should_not_see_errors,
    should_see_all_elements,
)
from tests.helpers import create_response

logger = logging.getLogger(__name__)
pytestmark = [
    pytest.mark.browser,
    pytest.mark.export,
    pytest.mark.export_plan_dashboard,
]

CHINA = {
    'country': 'China',
    'timezone': 'Asia/Shanghai',
    'utz_offset': '+0800',
    'export_duty': 0.1,
    'commodity_name': 'Gin and Geneva',
    'last_year_data': {
        'year': '2018',
        'trade_value': '4005400',
        'country_name': 'China',
        'year_on_year_change': '0.805'
    },
    'easeofdoingbusiness': {
        'total': 264,
        'year_2019': 31,
        'country_code': 'CHN',
        'country_name': 'China'
    },
    'historical_import_data': {
        'historical_trade_value_all': {
            '2016': '798577217',
            '2017': '845887963',
            '2018': '947564831'
        },
        'historical_trade_value_partner': {
            '2016': '3554772',
            '2017': '3224189',
            '2018': '4005400'
        }
    },
    'corruption_perceptions_index': {
        'rank': 80,
        'country_code': 'CHN',
        'country_name': 'China',
        'cpi_score_2019': 41
    }
}
INDIA = {
    'country': 'india',
    'export_duty': 1.5,
    'commodity_name': 'gin and geneva in containers holding 2l or less gin',
    'easeofdoingbusiness': {
        'total': 264,
        'country_name': 'india',
        'country_code': 'ind',
        'year_2019': 63
    },
    'corruption_perceptions_index': {
        'country_name': 'india',
        'country_code': 'ind',
        'cpi_score_2019': 41,
        'rank': 80
    },
    'last_year_data': {
        'year': '2018',
        'trade_value': '4581875',
        'country_name': 'india',
        'year_on_year_change': '1.532'
    },
    'historical_import_data': {
        'historical_trade_value_partner': {
            '2018': '4581875',
            '2017': '7018753',
            '2016': '6134421'
        },
        'historical_trade_value_all': {
            '2018': '947564831',
            '2017': '845887963',
            '2016': '798577217'
        }
    },
    'timezone': 'asia/kolkata',
    'utz_offset': '+0530'
}
JAPAN = {
    'country': 'Japan',
    'timezone': 'Asia/Tokyo',
    'utz_offset': '+0900',
    'export_duty': 0,
    'commodity_name': 'Gin and Geneva',
    'last_year_data': {
        'year': '2018',
        'trade_value': '16249072',
        'country_name': 'Japan',
        'year_on_year_change': '0.942'
    },
    'easeofdoingbusiness': {
        'total': 264,
        'year_2019': 29,
        'country_code': 'JPN',
        'country_name': 'Japan'
    },
    'historical_import_data': {
        'historical_trade_value_all': {
            '2016': '798577217',
            '2017': '845887963',
            '2018': '947564831'
        },
        'historical_trade_value_partner': {
            '2017': '15310462',
            '2018': '16249072',
            '2019': '15406650'
        }
    },
    'corruption_perceptions_index': {
        'rank': 20,
        'country_code': 'JPN',
        'country_name': 'Japan',
        'cpi_score_2019': 73
    }
}


@pytest.fixture
def mock_user_location_create():
    with patch('core.helpers.store_user_location'):
        yield


@pytest.fixture
def mock_update_company_profile():
    with patch.object(core_helpers, 'update_company_profile', return_value=create_response()) as patched:
        yield patched


@pytest.fixture
def mock_get_dashboard_events():
    with patch.object(core_helpers, 'get_dashboard_events', return_value=[]) as patched:
        yield patched


@pytest.fixture
def mock_get_dashboard_export_opportunities():
    with patch.object(core_helpers, 'get_dashboard_export_opportunities', return_value=[]) as patched:
        yield patched


@pytest.fixture
def mock_get_export_plan_market_data():
    return_value = {
        'timezone': 'Asia/Tokyo',
        'CPI': 73,
    }
    with patch.object(exportplan_helpers, 'get_exportplan_marketdata', return_value=return_value) as patched:
        yield patched


@pytest.fixture
def mock_get_export_plan_rules_regulations():
    return_value = {
        'country': 'Japan',
        'commodity_code': '2208.50',
    }
    with patch.object(exportplan_helpers, 'get_exportplan_rules_regulations', return_value=return_value) as patched:
        yield patched


@pytest.fixture
def mock_get_comtrade_last_year_import_data():
    return_value = {
        'last_year_data_partner': {
            'Year': 2019,
            'value': 16249072,
        }
    }
    with patch.object(exportplan_helpers, 'get_comtrade_lastyearimportdata', return_value=return_value) as patched:
        yield patched


@pytest.fixture
def mock_get_exportplan():
    return_value = {
        'pk': 1,
        'target_markets': [JAPAN],
    }
    with patch.object(exportplan_helpers, 'get_exportplan', return_value=return_value) as patched:
        yield patched


@pytest.fixture
def mock_all_dashboard_and_export_plan_requests_and_responses(
        mock_user_location_create,
        mock_update_company_profile,
        mock_get_dashboard_events,
        mock_get_dashboard_export_opportunities,
        mock_get_export_plan_market_data,
        mock_get_export_plan_rules_regulations,
        mock_get_comtrade_last_year_import_data,
        mock_get_exportplan,
        mock_export_plan_dashboard_page_tours,
):
    yield


@allure.step('Visit Target Markets page')
def visit_target_markets_page(live_server, browser):
    target_markets_url = urljoin(live_server.url, reverse('exportplan:target-markets'))
    browser.get(target_markets_url)
    should_not_see_errors(browser)

    attach_jpg_screenshot(browser, 'market data with folded countries chooser')
    should_see_all_elements(browser, ExportPlanTargetMarketsData)
    should_see_all_elements(browser, ExportPlanTargetMarketsRecommendedCountriesFolded)


@allure.step('Should see target market data for following countries: {country_names}')
def should_see_target_market_data_for(browser, country_names: list):
    visible_markets = browser.find_elements_by_css_selector(
        ExportPlanTargetMarketsData.MARKET_DATA.selector
    )
    visible_country_names = [
        market_data.find_element_by_tag_name('h2').text
        for market_data in visible_markets
    ]
    for market_data in visible_markets:
        country = market_data.find_element_by_tag_name('h2').text
        attach_jpg_screenshot(browser, f'Market data for {country}', element=market_data)
    assert visible_country_names == country_names


@allure.step('Add {country} to the export plan')
def add_country_to_export_plan(browser, country):
    add_country_button = browser.find_element_by_id(
        ExportPlanTargetMarketsData.ADD_COUNTRY.selector
    )
    attach_jpg_screenshot(browser, 'after clicking on add country button')
    with selenium_action(browser, f'Failed to click on add country'):
        add_country_button.click()

    country_input = browser.find_element_by_css_selector(
        TargetMarketsCountryChooser.COUNTRY_AUTOCOMPLETE_MENU.selector
    )
    with selenium_action(browser, f'Failed to click on add country'):
        country_input.click()

    country_elements = browser.find_elements_by_css_selector(
        TargetMarketsCountryChooser.AUTOCOMPLETE_COUNTRIES.selector
    )
    country_options = [
        element
        for element in country_elements
        if element.text == country
    ]
    country_option = country_options[0]

    logger.info(f'Will select: {country_option}')
    with selenium_action(browser, f'Failed to select country'):
        country_option.click()

    save_country = browser.find_element_by_id(
        TargetMarketsCountryChooser.SAVE_COUNTRY.selector
    )
    with selenium_action(browser, f'Failed to click on save country'):
        save_country.click()
    attach_jpg_screenshot(browser, f'After saving country selection')
    should_not_see_errors(browser)


@mock.patch.object(exportplan_helpers, 'get_exportplan')
@mock.patch.object(exportplan_helpers, 'get_comtrade_lastyearimportdata')
@mock.patch.object(exportplan_helpers, 'get_exportplan_rules_regulations')
@mock.patch.object(exportplan_helpers, 'get_exportplan_marketdata')
@mock.patch.object(core_helpers, 'get_dashboard_export_opportunities')
@mock.patch.object(core_helpers, 'get_dashboard_events')
@mock.patch.object(core_helpers, 'update_company_profile')
@mock.patch('core.helpers.store_user_location')
def test_can_see_target_markets_data(
    mock_user_location_create,
    mock_update_company_profile,
    mock_get_dashboard_events,
    mock_get_dashboard_export_opportunities,
    mock_get_export_plan_market_data,
    mock_get_export_plan_rules_regulations,
    mock_get_comtrade_last_year_import_data,
    mock_get_exportplan,
    server_user_browser_dashboard,
    mock_export_plan_dashboard_page_tours,
):
    mock_update_company_profile.return_value = create_response()
    mock_get_dashboard_events.return_value = []
    mock_get_dashboard_export_opportunities.return_value = []

    mock_get_export_plan_rules_regulations.return_value = {
        'country': 'Australia',
        'commodity_code': '220.850',
    }
    mock_get_export_plan_market_data.return_value = {
        'timezone': 'Australia/Sydney',
        'CPI': 10,
        'sectors': ['Automotive']
    }
    mock_get_comtrade_last_year_import_data.return_value = {
        'last_year_data_partner': {
            'Year': 2019,
            'value': 10000,
        }
    }

    data = {
        'target_markets': [
            {
                'country': 'Australia',
                'export_duty': 0.05,
                'easeofdoingbusiness': {
                    'total': 264,
                    'country_name': 'Australia',
                    'country_code': 'AUS',
                    'year_2019': 14
                },
                'corruption_perceptions_index': {
                    'country_name': 'Australia',
                    'country_code': 'AUS',
                    'cpi_score_2019': 77,
                    'rank': 12
                },
                'last_year_data': {
                    'year': 2019,
                    'trade_value': '33097917',
                    'country_name': 'Australia',
                    'year_on_year_change': '0.662'
                },
            }
        ],
        'sectors': ['Automotive']
    }
    mock_get_exportplan.return_value = data

    live_server, user, browser = server_user_browser_dashboard

    target_markets_url = urljoin(live_server.url, reverse('exportplan:target-markets'))
    browser.get(target_markets_url)
    should_not_see_errors(browser)

    attach_jpg_screenshot(browser, 'market data with folded countries chooser')
    should_see_all_elements(browser, ExportPlanTargetMarketsData)
    should_see_all_elements(browser, ExportPlanTargetMarketsRecommendedCountriesFolded)

    sector_chooser_button = browser.find_element_by_id(
        ExportPlanTargetMarketsRecommendedCountriesFolded.SECTOR_CHOOSER_BUTTON.selector
    )
    with selenium_action(browser, f'Failed to click on sector chooser button'):
        sector_chooser_button.click()
    attach_jpg_screenshot(browser, 'market data with unfolded countries chooser')


@mock.patch.object(exportplan_helpers, 'update_exportplan')
def test_can_add_multiple_countries_on_target_markets_page(
    mock_update_exportplan,
    mock_all_dashboard_and_export_plan_requests_and_responses,
    server_user_browser_dashboard,
):
    updated_export_plan_data = {
        'pk': 1,
        'target_markets': [JAPAN, CHINA],
    }
    mock_update_exportplan.return_value = updated_export_plan_data

    live_server, user, browser = server_user_browser_dashboard

    visit_target_markets_page(live_server, browser)
    should_see_target_market_data_for(browser, ['Japan'])

    add_country_to_export_plan(browser, 'China')

    should_see_target_market_data_for(browser, ['Japan', 'China'])
