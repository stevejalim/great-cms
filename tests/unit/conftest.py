import pytest

from tests.unit.core.factories import ListPageFactory, CuratedListPageFactory
from tests.unit.learn import factories as learn_factories


@pytest.mark.django_db(transaction=True)
@pytest.fixture
def topics_with_lessons(domestic_homepage):
    list_page = ListPageFactory(parent=domestic_homepage, record_read_progress=True)
    topic_a = CuratedListPageFactory(parent=list_page, title='Lesson topic A', slug='topic-a',)

    topic_id_a = '495856f0-37ae-496b-a7c4-cd010a6e7011'
    lesson_a1 = learn_factories.LessonPageFactory(
        parent=topic_a, title='Lesson A1', slug='lesson-a1', topic_block_id=topic_id_a
    )
    lesson_a2 = learn_factories.LessonPageFactory(
        parent=topic_a, title='Lesson A2', slug='lesson-a2', topic_block_id=topic_id_a
    )

    topic_a.topics.is_lazy = True
    topic_a.topics.stream_data = [
        {
            'type': 'topic',
            'value': {'title': 'Some title', 'pages': [lesson_a1.pk, lesson_a2.pk]},
            'id': topic_id_a,
        }
    ]
    topic_a.save()

    topic_b = CuratedListPageFactory(parent=list_page, title='Lesson topic b', slug='topic-b',)
    topic_id_b = '748179h0-jd87-789f-h7e7-cd02816e9333'
    lesson_b1 = learn_factories.LessonPageFactory(
        parent=topic_b, title='Lesson b1', slug='lesson-b1', topic_block_id=topic_id_b
    )
    topic_b.topics.is_lazy = True
    topic_b.topics.stream_data = [
        {
            'type': 'topic',
            'value': {'title': 'Some title b', 'pages': [lesson_b1.pk]},
            'id': topic_id_b,
        }
    ]
    topic_b.save()

    return [(topic_a, [lesson_a1, lesson_a2]), (topic_b, [lesson_b1])]
