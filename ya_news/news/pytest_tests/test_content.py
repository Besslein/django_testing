from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm
from .conftest import NEWS_DETAIL_URL, NEWS_HOME_URL


FORM_NAME = 'form'


def test_authorized_client_has_form(author_client, news):
    response = author_client.get(reverse(NEWS_DETAIL_URL, args=(news.id,)))
    assert isinstance(response.context.get('form'), CommentForm)


def test_anonymous_client_has_no_form(client, news):
    response = client.get(reverse(NEWS_DETAIL_URL, args=(news.id,)))
    assert FORM_NAME not in response.context


def test_comments_order(client, comments, news):
    response = client.get(reverse(NEWS_DETAIL_URL, args=(news.id,)))
    all_comments = response.context['news'].comment_set.all()
    all_created = [comment.created for comment in all_comments]
    sorted_created = sorted(all_created)
    assert all_created == sorted_created


def test_news_count(client, news_list):
    url = reverse(NEWS_HOME_URL)
    response = client.get(url)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news):
    url = reverse(NEWS_HOME_URL)
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates
