from datetime import timedelta

import pytest
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from news.models import Comment, News


URL_TO_COMMENTS = 'news:detail'
EDIT_URL = 'news:edit'
DELETE_URL = 'news:delete'
NEWS_DETAIL_URL = reverse('news:detail', args=news.id,)
NEWS_HOME_URL = reverse('news:home')
LOGIN_URL = 'users:login'


@pytest.mark.django_db
@pytest.fixture(autouse=True)
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def reader_client(reader, client):
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def comments(news, author):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Tекст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def news_list():
    today = timezone.now()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
