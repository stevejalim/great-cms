import pytest
from unittest import mock
from freezegun import freeze_time

from django.urls import reverse
from requests.exceptions import ReadTimeout

from exportplan import helpers


@pytest.mark.django_db
@freeze_time('2016-11-23T11:21:10.977518Z')
@mock.patch.object(helpers, 'update_exportplan')
@mock.patch.object(helpers, 'get_exportplan')
def test_ajax_country_data(mock_get_export_plan, mock_update_exportplan, client, user):
    client.force_login(user)
    url = reverse('exportplan:ajax-country-data')

    update_return_data = {'target_markets': [{'country': 'UK'}, {'country': 'China', 'SomeData': 'xyz'}, ]}

    mock_get_export_plan.return_value = {'pk': 1, 'target_markets': [{'country': 'UK'}, ]}
    mock_update_exportplan.return_value = update_return_data

    response = client.get(url, {'country': 'China', })

    assert mock_get_export_plan.call_count == 1
    assert mock_get_export_plan.call_args == mock.call(sso_session_id='123')
    assert response.status_code == 200

    assert mock_update_exportplan.call_count == 1
    assert mock_update_exportplan.call_args == mock.call(
        data={'target_markets': [{'country': 'UK'}, {'country': 'China'}]},
        id=1,
        sso_session_id='123'
    )
    assert response.json() == {
        'datenow': '2016-11-23T11:21:10.977Z',
        'target_markets': update_return_data['target_markets']
    }


@pytest.mark.django_db
@mock.patch.object(helpers, 'get_exportplan')
def test_ajax_country_data_time_out(mock_get_exportplan, client, user):
    client.force_login(user)
    url = reverse('exportplan:ajax-country-data')

    mock_get_exportplan.side_effect = ReadTimeout
    response = client.get(url, {'country': 'China', })

    assert response.status_code == 504


@pytest.mark.django_db
def test_ajax_country_data_no_country(client, user):
    client.force_login(user)
    url = reverse('exportplan:ajax-country-data')
    response = client.get(url)

    assert response.status_code == 400