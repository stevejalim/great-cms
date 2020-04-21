from unittest.mock import patch

import pytest

from core import helpers as core_helpers
from exportplan import helpers as exportplan_helpers
from tests.helpers import create_response

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
def mock_get_recommended_countries():
    return_value = [{'country': 'China'}, {'country': 'india'}]
    with patch.object(exportplan_helpers, 'get_recommended_countries', return_value=return_value) as patched:
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
        mock_get_recommended_countries,
        mock_get_exportplan,
        mock_export_plan_dashboard_page_tours,
):
    yield