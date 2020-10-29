from unittest import mock

import pytest

from django.template import Context, Template
from datetime import timedelta

from core.templatetags.content_tags import (
    get_backlinked_url,
    get_topic_title_for_lesson,
)
from core.templatetags.object_tags import get_item
from core.templatetags.personalised_blocks import render_video_block
from core.templatetags.url_map import path_match
from core.templatetags.video_tags import render_video
from core.templatetags.progress_bar import progress_bar

from tests.helpers import add_lessons_and_placeholders_to_curated_list_page
from tests.unit.core import factories


def test_render_personalised_video_block_tag():
    video_mock = mock.Mock(
        sources=[{'src': '/media/foo.mp4', 'type': 'video/mp4'}]
    )
    block = dict(
        width=20,
        height=20,
        video=video_mock
    )
    html = render_video_block(block)

    assert '<video width="20" height="20" controls>' in html
    assert '<source src="/media/foo.mp4" type="video/mp4">' in html
    assert 'Your browser does not support the video tag.' in html


def test_general_render_video_tag():
    video_mock = mock.Mock(
        sources=[{'src': '/media/foo.mp4', 'type': 'video/mp4'}],
        duration=120,
    )
    block = dict(
        video=video_mock
    )
    html = render_video(block)

    assert '<video controls data-v-duration="120">' in html
    assert '<source src="/media/foo.mp4" type="video/mp4">' in html
    assert 'Your browser does not support the video tag.' in html


def test_empty_block_render_video_tag():

    block = dict()
    html = render_video(block)
    assert '' in html


@pytest.mark.django_db
def test_format_timedelta_filter(user, rf, domestic_site):
    cases = [
        {'value': timedelta(seconds=0), 'result': '0 min:0 min'},
        {'value': timedelta(seconds=25), 'result': '1 min:1 min'},
        {'value': timedelta(seconds=70), 'result': '2 min:2 mins'},
        {'value': timedelta(seconds=4500), 'result': '1 hour 15 min:1 hour 15 mins'},
        {'value': timedelta(seconds=7200), 'result': '2 hour:2 hours'},
        {'value': None, 'result': ':'}
    ]

    template = Template(
        '{% load format_timedelta from content_tags %}'
        '{{ delta|format_timedelta }}:{{ delta|format_timedelta:True }}'
    )

    for case in cases:
        context = Context({'delta': case.get('value')})
        html = template.render(context)
        assert html == case.get('result')


@pytest.mark.django_db
def test_pluralize(user, rf, domestic_site):
    cases = [
        {'value': 0, 'result': 's'},
        {'value': 1, 'result': ''},
        {'value': 2, 'result': 's'},
    ]

    template = Template(
        '{% load pluralize from content_tags %}'
        '{% pluralize value %}'
    )
    for case in cases:
        html = template.render(Context({'value': case.get('value')}))
        assert html == case.get('result')


@pytest.mark.django_db
def test_tojson(user, rf, domestic_site):

    template = Template(
        '{% load to_json %}'
        '{{ data|to_json }}'
    )

    html = template.render(Context({'data': {'thing1': 'one', 'thing2': 'two'}}))
    assert html == '{"thing1": "one", "thing2": "two"}'


@pytest.mark.django_db
def test_set(user, rf, domestic_site):

    template = Template(
        '{% load set %}'
        "{% set 'my_variable' 1234 %}"
        '{{ my_variable }}'
    )

    html = template.render(Context({}))
    assert html == '1234'


@pytest.mark.django_db
def test_get_item_filter(user, rf, domestic_site):
    cases = [
        {'lesson_details': {'my-lesson': {'topic_name': 'my topic'}}, 'result': 'my topic'},
        {'lesson_details': {'myLesson2': {'topic_name': 'my topic'}}, 'result': ''},
        {'lesson_details': '', 'result': ''},
    ]

    template = Template(
        '{% load object_tags %}'
        '{{ lesson_details|get_item:\"my-lesson\"|get_item:\"topic_name\" }}'
    )

    for case in cases:
        html = template.render(Context({'lesson_details': case.get('lesson_details')}))
        assert html == case.get('result')


@pytest.mark.django_db
@pytest.mark.parametrize(
    'request_path,outbound_url,expected_backlinked_url',
    (
        (
            '/example/export-plan/path/',
            '/test/outbound/path/',
            '/test/outbound/path/?return-link=%2Fexample%2Fexport-plan%2Fpath%2F'
        ),
        (
            '/example/export-plan/path/?foo=bar',
            '/test/outbound/path/',
            '/test/outbound/path/?return-link=%2Fexample%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar'
        ),
        (
            '/example/export-plan/path/',
            'https://example.com/test/outbound/path/',
            'https://example.com/test/outbound/path/?return-link=%2Fexample%2Fexport-plan%2Fpath%2F'
        ),
        (
            '/example/export-plan/path/?foo=bar',
            'https://example.com/test/outbound/path/',
            (
                'https://example.com/test/outbound/path/'
                '?return-link=%2Fexample%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar'
            )
        ),
        (
            '/example/export-plan/path/?foo=bar',
            '/test/outbound/path/?bam=baz',
            (
                '/test/outbound/path/'
                '?bam=baz&return-link=%2Fexample%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar'
            )
        ),
        (
            '/example/export-plan/path/?foo=bar',
            'https://example.com/test/outbound/path/?bam=baz',
            (
                'https://example.com/test/outbound/path/'
                '?bam=baz&return-link=%2Fexample%2Fexport-plan%2Fpath%2F%3Ffoo%3Dbar'
            )
        ),
    ),
    ids=[
        '1. Outbound path with NO existing querystring for the source/request path',
        '2. Outbound path with an existing querystring for the source/request path',
        '3. Full outbound URL with NO existing querystring for the source/request path',
        '4. Full outbound URL with existing querystring for the source/request path',
        '5. Both source/request and outbound URLs feature querystrings',
        '5. Both source/request and outbound URLs feature querystrings; outbound is a full URL',
    ]
)
def test_get_backlinked_url(rf, request_path, outbound_url, expected_backlinked_url):
    context = {'request': rf.get(request_path)}
    assert get_backlinked_url(context, outbound_url) == expected_backlinked_url


@pytest.mark.django_db
@pytest.mark.parametrize('path, expected', (
    ('/markets/', True),
    ('/markets/morepath/', True),
    ('/export-plan/markets/', False),
    ('', False),
),
    ids=[
        'match base path',
        'match extended path',
        'non-match',
        'empty path'
]
)
def test_path_match(rf, path, expected):
    context = {'request': rf.get(path)}
    match = path_match(context, '^\\/markets\\/')
    assert bool(match) == expected


@pytest.mark.django_db
def test_push(user, rf, domestic_site):

    template = Template(
        '{% load set %}'
        "{% push 'my_variable' 'item1' %}"
        "{% push 'my_variable' 'item2' %}"
        'one:{{ my_variable.0 }} '
        'two:{{ store.my_variable.1 }}'
    )

    html = template.render(Context({}))
    assert html == 'one:item1 two:item2'


@pytest.mark.parametrize(
    'data,key,expected',
    (
        ({'foo': 'bar'}, 'foo', 'bar'),
        ({'foo': 'bar'}, 'bam', None),
        ({1: 'bar'}, 1, 'bar'),
        ({'1': 'bar'}, 1, None),
        ({1: 'bar'}, '1', None),
        ('a string has no get attr', 'foo', ''),
        ({'foo': 'bar'}, 'FOO', 'bar'),
    )
)
def test_get_item(data, key, expected):
    assert get_item(data, key) == expected


@pytest.mark.parametrize(
    'total,complete,percentage',
    (
        (10, 0, '0%'),
        (10, 5, '50%'),
        (10, 10, '100%'),
        (0, 0, '0%'),
    )
)
def test_progress_bar(total, complete, percentage):
    html = progress_bar(total, complete)
    check = f'style="width:{percentage}"'
    assert html.find(check) > 0


@pytest.mark.django_db
def test_get_topic_title_for_lesson(domestic_homepage, domestic_site):

    # Lots of setup, alas

    list_page = factories.ListPageFactory(
        parent=domestic_homepage, record_read_progress=True
    )
    module_1 = factories.CuratedListPageFactory(
        title='Module 1',
        parent=list_page,
    )

    module_2 = factories.CuratedListPageFactory(
        title='Module 2', parent=list_page,
    )

    detail_page_1 = factories.DetailPageFactory(slug='detail-page-1-1', parent=module_1)
    detail_page_2 = factories.DetailPageFactory(slug='detail-page-1-2', parent=module_1)
    detail_page_3 = factories.DetailPageFactory(slug='detail-page-1-3', parent=module_1)
    detail_page_4 = factories.DetailPageFactory(slug='detail-page-4-2', parent=module_2)
    # page 5 is not going to be mapped to a topic below
    detail_page_5 = factories.DetailPageFactory(slug='detail-page-5-0', parent=module_2)
    # page 6 is going to be a child of a totally new module AND not be mapped to a topic
    detail_page_6 = factories.DetailPageFactory(slug='detail-page-6-0')

    topic_1 = factories.CuratedTopicBlockFactory(
        title='Topic 1',
        # We add detail_page_1 and detail_page_2 to
        # lessons_and_placeholder data FOR MODULE 1 via JSON below
    )
    topic_2 = factories.CuratedTopicBlockFactory(
        title='Topic 2',
        # We add detail_page_3 to lessons_and_placeholder data FOR MODULE 1 via JSON below
    )
    topic_3 = factories.CuratedTopicBlockFactory(
        title='Topic 3',
        # We add detail_page_4 to lessons_and_placeholder data FOR MODULE 2 via JSON below
    )

    module_1.topics = [('topic', topic_1), ('topic', topic_2)]
    module_2.topics = [('topic', topic_3)]
    module_1.save()
    module_2.save()

    lessons_for_topic_1 = [  # used in module 1
        {'type': 'lesson', 'value': detail_page_1.id},
        {'type': 'placeholder', 'value': {'title': 'Topic One: Placeholder One'}},
        {'type': 'lesson', 'value': detail_page_2.id},
        {'type': 'placeholder', 'value': {'title': 'Topic One: Placeholder Two'}},
    ]
    lessons_for_topic_2 = [  # used in module 1
        {'type': 'lesson', 'value': detail_page_3.id},
        {'type': 'placeholder', 'value': {'title': 'Topic Two: Placeholder One'}},
        {'type': 'placeholder', 'value': {'title': 'Topic Two: Placeholder Two'}},
        {'type': 'placeholder', 'value': {'title': 'Topic Two: Placeholder Three'}},
    ]
    lessons_for_topic_3 = [  # used in module 2
        {'type': 'placeholder', 'value': {'title': 'Topic Three: Placeholder One'}},
        {'type': 'lesson', 'value': detail_page_4.id},
        {'type': 'placeholder', 'value': {'title': 'Topic Three: Placeholder Two'}},
    ]

    module_1 = add_lessons_and_placeholders_to_curated_list_page(
        curated_list_page=module_1,
        data_for_topics={
            0: {
                'lessons_and_placeholders': lessons_for_topic_1,
            },
            1: {
                'lessons_and_placeholders': lessons_for_topic_2,
            },
        }

    )
    module_2 = add_lessons_and_placeholders_to_curated_list_page(
        curated_list_page=module_2,
        data_for_topics={
            0: {
                'lessons_and_placeholders': lessons_for_topic_3,
            },
        }
    )

    # Finally, to the test:
    assert get_topic_title_for_lesson(detail_page_1) == 'Topic 1'
    assert get_topic_title_for_lesson(detail_page_2) == 'Topic 1'
    assert get_topic_title_for_lesson(detail_page_3) == 'Topic 2'
    assert get_topic_title_for_lesson(detail_page_4) == 'Topic 3'
    assert get_topic_title_for_lesson(detail_page_5) == ''
    assert get_topic_title_for_lesson(detail_page_6) == ''
