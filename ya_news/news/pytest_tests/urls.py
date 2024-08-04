import pytest
from django.urls import reverse


@pytest.fixture
def url_to_comments(news):
    news_url = reverse('news:detail', args=(news.id,))
    return news_url + '#comments'


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def news_home_url():
    return reverse('news:home')


@pytest.fixture
def login_url():
    return reverse('users:login')
