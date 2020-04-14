from core import models
from tests.unit.core.factories import ListPageFactory, DetailPageFactory


class TopicPageFactory(ListPageFactory):

    template = 'learn/topic_page.html'

    class Meta:
        model = models.ListPage
        django_get_or_create = ['slug', 'parent']


class LessonPageFactoru(DetailPageFactory):
    template = 'learn/lesson_page.html'

    class Meta:
        model = models.DetailPage
        django_get_or_create = ['slug', 'parent']
