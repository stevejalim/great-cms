import time

from unittest import mock

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase
from wagtail.core.blocks.stream_block import StreamBlockValidationError
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
    case_study_body_validation,
)

from domestic.models import DomesticDashboard, DomesticHomePage
from exportplan.models import ExportPlanDashboardPage
from tests.unit.core import factories
from tests.helpers import make_test_video
from .factories import CaseStudyFactory, DetailPageFactory


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
def test_curated_list_page_has_link_in_context_back_to_parent(client, domestic_homepage, domestic_site):

    list_page = factories.ListPageFactory(
        parent=domestic_homepage,
        record_read_progress=False,
        slug='example-learning-homepage'
    )
    curated_list_page = factories.CuratedListPageFactory(
        parent=list_page,
        slug='example-module'
    )

    expected_url = list_page.url
    assert expected_url == '/example-learning-homepage/'

    resp = client.get(curated_list_page.url)

    # Make a more precise string to search for: one that's marked up as a
    # hyperlink target, at least
    expected_link_string = f'href="{expected_url}"'
    assert expected_link_string.encode('utf-8') in resp.content


@pytest.mark.django_db
@pytest.mark.parametrize(
    'querystring_to_add,expected_backlink_value',
    (
        ('', None),
        (
            '?return-link=%2Fexport-plan%2Fsection%2Fabout-your-business%2F',
            '/export-plan/section/about-your-business/'
        ),
        (
            '?return-link=%2Fexport-plan%2Fsection%2Fabout-your-business%2F%3Ffoo%3Dbar',
            '/export-plan/section/about-your-business/?foo=bar'
        ),
        (
            '?bam=baz&return-link=%2Fexport-plan%2Fsection%2Fabout-your-business%2F%3Ffoo%3Dbar',
            '/export-plan/section/about-your-business/?foo=bar'  # NB: bam=baz should not be here
        ),
        (
            '?bam=baz&return-link=example%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar',
            None
        ),
        (
            (
                '?bam=baz&return-link=https%3A%2F%2Fphishing.example.com'
                '%2Fexport-plan%2Fsection%2Fabout-your-business%2F%3Ffoo%3Dbar'
            ),
            None
        ),
        (
            (
                '?bam=baz&return-link=%3A%2F%2Fphishing.example.com'
                '%2Fexport-plan%2Fsection%2Fabout-your-business%2F%3Ffoo%3Dbar'
            ),
            None
        ),
        (
            '?bam=baz',
            None
        ),
        (
            '?bam=baz&return-link=%2Fexport-plan%2Fsection%2Fabout-your-business%2F%3Ffoo%3Dbar',
            '/export-plan/section/about-your-business/?foo=bar'
        ),

    ),
    ids=(
        'no backlink querystring present',
        'backlink querystring present without encoded querystring of its own',
        'backlink querystring present WITH encoded querystring of its own',
        'backlink querystring present WITH encoded querystring and other args',
        'backlink querystring present WITH bad payload - path does not start with / ',
        'backlink querystring present WITH bad payload - path is a full URL',
        'backlink querystring present WITH bad payload - path is a URL with flexible proto',
        'backlink querystring NOT present BUT another querystring is',
        'backlink querystring present WITH OTHER QUERYSTRING TOO',
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


@pytest.mark.django_db
@pytest.mark.parametrize(
    'backlink_path,expected',
    (
        (None, None),
        ('', None),
        ('/export-plan/section/about-your-business/', 'About your business'),
        ('/export-plan/section/objectives/', 'Objectives'),
        ('/export-plan/section/target-markets-research/', 'Target markets research'),
        ('/export-plan/section/adaptation-for-your-target-market/', 'Adaptation for your target market'),
        ('/export-plan/section/marketing-approach/', 'Marketing approach'),
        ('/export-plan/section/costs-and-pricing/', 'Costs and pricing'),
        ('/export-plan/section/finance/', 'Finance'),
        ('/export-plan/section/payment-methods/', 'Payment methods'),
        ('/export-plan/section/travel-and-business-policies/', 'Travel and business policies'),
        ('/export-plan/section/business-risk/', 'Business risk'),
        (
            '/export-plan/section/adaptation-for-your-target-market/?foo=bar',
            'Adaptation for your target market'
        ),
        (
            '/export-plan/',
            None
        ),
        (
            '/path/that/will/not/match/anything/',
            None
        ),
    ),
    ids=(
        'no backlink',
        'empty string backlink',
        'Seeking: About your business',
        'Seeking: Objectives',
        'Seeking: Target markets research',
        'Seeking: Adaptation for your target market',
        'Seeking: Marketing approach',
        'Seeking: Costs and pricing',
        'Seeking: Payment methods',
        'Seeking: Finance',
        'Seeking: Travel and business policies',
        'Seeking: Business risk',
        'Valid backlink with querystring does not break name lookup',
        'backlink for real page that is not an export plan step',
        'backlink for a non-existent page',
    )
)
def test_detail_page_get_context_gets_backlink_title_based_on_backlink(backlink_path, expected):
    detail_page = factories.DetailPageFactory(
        template='learn/detail_page.html'
    )
    assert detail_page._get_backlink_title(backlink_path) == expected


@pytest.mark.django_db
def test_case_study__str():
    case_study = CaseStudyFactory(
        company_name='Test Co'
    )
    assert f'{case_study}' == 'Case Study: Test Co'


@pytest.mark.django_db
def test_case_study__timestamps():
    case_study = CaseStudyFactory(
        company_name='Test Co'
    )
    created = case_study.created
    modified = case_study.created
    assert created == modified

    time.sleep(1)  # Forgive this - we need to have a real, later save
    case_study.save()
    case_study.refresh_from_db()

    assert case_study.created == created
    assert case_study.modified > modified


@pytest.mark.django_db
@pytest.mark.parametrize(
    'block_type_values,expect_raise',
    (
        (['media', 'text'], False),
        (['media'], True),
        (['text'], True),
        ([], False),
        (['media', 'media'], True),
        (['text', 'text'], True),
    ),
    ids=(
        'media node and text node: fine',
        'text node only: not fine',
        'media node only: not fine',
        'no nodes: fine - the overall requirement is done at a higher level',
        'two text nodes: not fine',
        'two media nodes: not fine',
    )
)
def test_case_study_body_validation(block_type_values, expect_raise):

    value = []
    for block_type in block_type_values:
        mock_block = mock.Mock()
        mock_block.block_type = block_type
        value.append(mock_block)

    if expect_raise:
        with pytest.raises(StreamBlockValidationError):
            case_study_body_validation(value)
    else:
        # should not blow up
        case_study_body_validation(value)


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
