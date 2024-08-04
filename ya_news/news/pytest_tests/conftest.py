from datetime import timedelta

import pytest
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from news.models import Comment, News


@pytest.mark.django_db
@pytest.fixture(autouse=True)
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    users_login = reverse('users:login')
    client.force_login(author)
    return users_login, client


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def reader_client(reader, client):
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    news_1 = reverse('news:home')
    news_2 = reverse('news:detail', args=(news.id,))
    return news_1, news_2, News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def comment(news, author):
    edit_url = reverse('news:edit', args=(comment.id,))
    delete_url = reverse('news:delete', args=(comment.id,))
    return delete_url, edit_url, Comment.objects.create(
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
    news_detail = reverse('news:detail', args=(news.id,))
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
    return news_detail
