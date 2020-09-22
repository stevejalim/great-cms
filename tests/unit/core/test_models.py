from unittest import mock

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.core.models import Collection
from wagtail.images import get_image_model
from wagtail.images.tests.utils import get_test_image_file
from wagtail.tests.utils import WagtailPageTests, WagtailTestUtils
from wagtail_factories import ImageFactory

from core.models import (
    AbstractObjectHash,
    CuratedListPage,
    DetailPage,
    InterstitialPage,
    LandingPage,
    ListPage,
)
from domestic.models import DomesticDashboard, DomesticHomePage
from exportplan.models import ExportPlanDashboardPage
from tests.unit.core import factories
from tests.helpers import make_test_video
from .factories import DetailPageFactory


def test_object_hash():
    mocked_file = mock.Mock()
    mocked_file.read.return_value = b'foo'
    hash = AbstractObjectHash.generate_content_hash(mocked_file)
    assert hash == 'acbd18db4cc2f85cedef654fccc4a4d8'


@pytest.mark.django_db
def test_detail_page_can_mark_as_read(client, domestic_homepage, user, domestic_site):
    # given the user has not read a lesson
    client.force_login(user)

    list_page = factories.ListPageFactory(parent=domestic_homepage, record_read_progress=True)
    curated_list_page = factories.CuratedListPageFactory(parent=list_page)
    detail_page = factories.DetailPageFactory(parent=curated_list_page)

    client.get(detail_page.url)

    # then the progress is saved
    read_hit = detail_page.page_views.get()
    assert read_hit.sso_id == str(user.pk)
    assert read_hit.list_page == list_page


@pytest.mark.django_db
def test_detail_page_cannot_mark_as_read(client, domestic_homepage, user, domestic_site):
    # given the user has not read a lesson
    client.force_login(user)
    list_page = factories.ListPageFactory(parent=domestic_homepage, record_read_progress=False)
    curated_list_page = factories.CuratedListPageFactory(parent=list_page)
    detail_page = factories.DetailPageFactory(parent=curated_list_page)

    client.get(detail_page.url)

    # then the progress is saved
    assert detail_page.page_views.count() == 0


@pytest.mark.django_db
def test_detail_page_anon_user_not_marked_as_read(client, domestic_homepage, domestic_site):
    # given the user has not read a lesson
    list_page = factories.CuratedListPageFactory(parent=domestic_homepage)
    detail_page = factories.DetailPageFactory(parent=list_page)

    client.get(detail_page.url)

    # then the progress is unaffected
    assert detail_page.page_views.count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    'querystring_to_add,expected_backlink_value',
    (
        ('', None),
        (
            '?return-link=%2Fexample%2Fexport-plan%2Fpath%2F',
            '/example/export-plan/path/'
        ),
        (
            '?return-link=%2Fexample%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar',
            '/example/export-plan/path/?foo=bar'
        ),
        (
            '?bam=baz&return-link=%2Fexample%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar',
            '/example/export-plan/path/?foo=bar'  # NB: bam=baz should not be here
        ),
        (
            '?bam=baz&return-link=example%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar',
            None
        ),
        (
            (
                '?bam=baz&return-link=https%3A%2F%2Fphishing.example.com'
                '%2Fexample%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar'
            ),
            None
        ),
        (
            (
                '?bam=baz&return-link=%3A%2F%2Fphishing.example.com'
                '%2Fexample%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar'
            ),
            None
        ),
        (
            '?bam=baz',
            None
        ),
        (
            '?bam=baz&return-link=%2Fexample%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar',
            '/example/export-plan/path/?foo=bar'
        ),

    ),
    ids=(
        "no backlink querystring present",
        "backlink querystring present without encoded querystring of its own",
        "backlink querystring present WITH encoded querystring of its own",
        "backlink querystring present WITH encoded querystring and other args",
        "backlink querystring present WITH bad payload - path doesn't start with / ",
        "backlink querystring present WITH bad payload - path is a full URL",
        "backlink querystring present WITH bad payload - path is a URL with flexible proto",
        "backlink querystring NOT present BUT another querystring is",
        "backlink querystring present WITH OTHER QUERYSTRING TOO",
    )
)
def test_detail_page_get_context_handles_backlink_querystring_appropriately(
    rf,
    domestic_homepage,
    domestic_site,
    user,
    querystring_to_add,
    expected_backlink_value
):

    list_page = factories.ListPageFactory(
        parent=domestic_homepage,
        record_read_progress=False
    )
    curated_list_page = factories.CuratedListPageFactory(parent=list_page)
    detail_page = factories.DetailPageFactory(
        parent=curated_list_page,
        template='learn/detail_page.html'
    )

    lesson_page_url = detail_page.url
    if querystring_to_add:
        lesson_page_url += querystring_to_add

    request = rf.get(lesson_page_url)
    request.user = user
    request.user.export_plan = mock.Mock('mocked-export-plan')

    context = detail_page.get_context(request)

    if expected_backlink_value is None:
        assert 'backlink' not in context
    else:
        assert context.get('backlink') == expected_backlink_value


class LandingPageTests(WagtailPageTests):

    def test_can_be_created_under_homepage(self):
        self.assertAllowedParentPageTypes(LandingPage, {DomesticHomePage})

    def test_can_be_created_under_landing_page(self):
        self.assertAllowedSubpageTypes(
            LandingPage, {ListPage, InterstitialPage, ExportPlanDashboardPage, DomesticDashboard}
        )


class ListPageTests(WagtailPageTests):

    def test_can_be_created_under_landing_page(self):
        self.assertAllowedParentPageTypes(ListPage, {LandingPage})

    def test_allowed_subtypes(self):
        self.assertAllowedSubpageTypes(ListPage, {CuratedListPage})


class CuratedListPageTests(WagtailPageTests):

    def test_can_be_created_under_list_page(self):
        self.assertAllowedParentPageTypes(CuratedListPage, {ListPage})

    def test_allowed_subtypes(self):
        self.assertAllowedSubpageTypes(CuratedListPage, {DetailPage})


class DetailPageTests(WagtailPageTests):

    def test_can_be_created_under_curated_list_page(self):
        self.assertAllowedParentPageTypes(DetailPage, {CuratedListPage})

    def test_detail_page_creation_for_single_hero_image(self):

        detail_page = DetailPageFactory(
            hero=[('Image', ImageFactory())]
        )
        self.assert_(detail_page, True)

    def test_validation_kick_for_multiple_hero_image(self):
        with pytest.raises(ValidationError):
            detail_page = DetailPageFactory(
                hero=[('Image', ImageFactory()), ('Image', ImageFactory())]
            )
            self.assert_(detail_page, None)


class TestImageAltRendition(TestCase, WagtailTestUtils):
    def setUp(self):
        self.login()
        root_collection = Collection.objects.create(name='Root', depth=0)
        great_image_collection = root_collection.add_child(name='Great Images')

        # Create an image with alt text
        AltTextImage = get_image_model() # Noqa
        self.image = AltTextImage.objects.create(
            title='Test image',
            file=get_test_image_file(),
            alt_text='smart alt text',
            collection=great_image_collection
        )

    def test_image_alt_rendition(self):
        rendition = self.image.get_rendition('width-100')
        assert rendition.alt == 'smart alt text'
        assert self.image.title != rendition.alt


class TestGreatMedia(TestCase):
    def test_sources_mp4_with_no_transcript(self):
        media = make_test_video()
        self.assertEqual(media.sources, [{
            'src': '/media/movie.mp4',
            'type': 'video/mp4',
            'transcript': None,
        }])

    def test_sources_mp4_with_transcript(self):
        media = make_test_video(transcript='A test transcript text')

        self.assertEqual(media.sources, [{
            'src': '/media/movie.mp4',
            'type': 'video/mp4',
            'transcript': 'A test transcript text',
        }])
