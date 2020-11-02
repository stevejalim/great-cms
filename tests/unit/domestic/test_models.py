import pytest
from wagtail.tests.utils import WagtailPageTests
from unittest import mock

from core import mixins
from domestic.models import DomesticHomePage, DomesticDashboard
from directory_sso_api_client import sso_api_client
from .factories import DomesticHomePageFactory, DomesticDashboardFactory
from tests.unit.core.factories import DetailPageFactory, ListPageFactory, CuratedListPageFactory
from tests.helpers import add_lessons_and_placeholders_to_curated_list_page, create_response

from directory_api_client import api_client


class DomesticHomePageTests(WagtailPageTests):

    def test_page_is_exclusive(self):
        assert issubclass(DomesticHomePage, mixins.WagtailAdminExclusivePageMixin)

    def test_can_create_homepage(self):
        homepage = DomesticHomePageFactory()
        self.assertEqual(homepage.title, 'homepage')

    def test_slug_is_autogenerated(self):
        DomesticHomePageFactory(slug='home')
        homepage = DomesticHomePage.objects.get(url_path='/')

        # slug should be auto-assigned to a slugified version of the title
        hello_page = DomesticHomePage(title='Hello world')
        homepage.add_child(instance=hello_page)

        retrieved_page = DomesticHomePage.objects.get(id=hello_page.id)
        self.assertEqual(retrieved_page.slug, 'hello-world')

        # auto-generated slug should receive a suffix to make it unique
        events_page = DomesticHomePage(title='Events')
        homepage.add_child(instance=events_page)
        retrieved_page = DomesticHomePage.objects.get(id=events_page.id)
        self.assertEqual(retrieved_page.slug, 'events')


class DomesticDashboardTests(WagtailPageTests):

    def test_page_is_exclusive(self):
        assert issubclass(DomesticDashboard, mixins.WagtailAdminExclusivePageMixin)

    def test_can_create_dashboard(self):
        dashboard = DomesticDashboardFactory()
        self.assertEqual(dashboard.title, 'Title of Dashboard')


@pytest.mark.django_db
@mock.patch.object(sso_api_client.user, 'get_user_page_views')
@mock.patch.object(api_client.exportplan, 'exportplan_list')
@mock.patch.object(api_client.personalisation, 'events_by_location_list')
@mock.patch.object(api_client.personalisation, 'export_opportunities_by_relevance_list')
@mock.patch.object(sso_api_client.user, 'get_user_lesson_completed')
def test_dashboard_page_routing(
    mock_get_user_lesson_completed,
    mock_events_by_location_list,
    mock_export_opportunities_by_relevance_list,
    mock_exportplan_list,
    mock_get_user_page_views,
    patch_set_user_page_view,
    mock_get_company_profile,
    client,
    user,
    get_request,
    domestic_homepage,
    domestic_site,
):
    mock_exportplan_list.return_value = [{}]
    mock_events_by_location_list.return_value = create_response(json_body={'results': []})
    mock_export_opportunities_by_relevance_list.return_value = create_response(json_body={'results': []})
    mock_get_user_page_views.return_value = create_response(json_body={'result': 'ok', 'page_views': {}})
    list_one = ListPageFactory(parent=domestic_homepage, slug='topic-one', record_read_progress=True)
    lesson_one = DetailPageFactory(parent=list_one, slug='lesson-one')
    dashboard = DomesticDashboardFactory(
        parent=domestic_homepage,
        slug='dashboard',
        components__0__route__route_type='learn',
        components__0__route__title='Learning title',
        components__0__route__body='Learning Body Text',
        components__0__route__button={'label': 'Start learning'},
        components__1__route__route_type='target',
        components__1__route__title='Target title',
        components__1__route__body='Target Body Text',
        components__1__route__button={'label': 'Start targetting'},
        components__2__route__route_type='plan',
        components__2__route__title='Planning title',
        components__2__route__body='Planning Body Text',
        components__2__route__button={'label': 'Start planning'}
    )
    # All three routes should be visible
    mock_get_user_lesson_completed.return_value = create_response(json_body={'result': 'ok'})
    context_data = dashboard.get_context(get_request)
    assert len(context_data['routes']) == 3
    assert context_data['routes']['learn'].value.get('route_type') == 'learn'
    assert context_data['routes']['plan'].value.get('route_type') == 'plan'
    assert context_data['routes']['plan'].value.get('body') == 'Planning Body Text'
    assert context_data['lessons_in_progress'] is False
    # Check that the lesson route block is enabled
    assert context_data['routes']['learn'].value.get('enabled') is True

    # Build learning pages and mock one as 'read'
    topic_one = ListPageFactory(parent=domestic_homepage, slug='topic-one', record_read_progress=True)
    section_one = CuratedListPageFactory(parent=topic_one, slug='topic-one-section-one')

    _topic_id = '99999999-1f68-4c9f-8728-aa8c62cf3a2a'
    lesson_one = DetailPageFactory(
        parent=section_one,
        slug='lesson-one',
        topic_block_id=_topic_id
    )

    section_one = add_lessons_and_placeholders_to_curated_list_page(
        curated_list_page=section_one,
        data_for_topics={
            0: {
                'id': _topic_id,
                'title': 'Module one, first topic block',
                'lessons_and_placeholders': [
                    {'type': 'lesson', 'value': lesson_one.id},
                    {
                        'type': 'placeholder',
                        'value': {
                            'title': 'Placeholder To Show They Do Not Interfere With Counts'
                        }
                    },
                ]
            },
        }
    )
    mock_get_user_lesson_completed.return_value = create_response(json_body={'result': 'ok', 'lesson_completed': [
        {'lesson': lesson_one.id},
    ]})

    # the learning route should be disabled
    context_data = dashboard.get_context(get_request)
    assert context_data['lessons_in_progress'] is True
    assert context_data['routes']['learn'].value.get('enabled') is False

    # set a country in exportplan and watch plan section disappear
    assert context_data['routes']['target'].value.get('enabled') is True
    mock_exportplan_list.return_value = create_response(json_body=[{'export_countries': ['France']}])
    context_data = dashboard.get_context(get_request)
    assert context_data['routes']['target'].value.get('enabled') is False

    # page visit on exportplan dashboard should make plan section disappear
    assert context_data['routes']['plan'].value.get('enabled') is True
    mock_get_user_page_views.return_value = create_response(
        json_body={'result': 'ok', 'page_views': {'/export-plan/dashboard/': {'service': 'great-cms'}}})
    context_data = dashboard.get_context(get_request)
    assert context_data['routes']['plan'].value.get('enabled') is False
