from django.conf import settings

from news.forms import CommentForm
from .conftest import NEWS_DETAIL_URL, NEWS_HOME_URL


FORM_NAME = 'form'


def test_authorized_client_has_form(author_client, news):
    response = author_client.get(NEWS_DETAIL_URL)
    assert isinstance(response.context.get('form'), CommentForm)


def test_anonymous_client_has_no_form(client, news):
    response = client.get(NEWS_DETAIL_URL)
    assert FORM_NAME not in response.context


def test_comments_order(client, comments, news):
    response = client.get(NEWS_DETAIL_URL)
    all_comments = response.context['news'].comment_set.all()
    all_created = [comment.created for comment in all_comments]
    sorted_created = sorted(all_created)
    assert all_created == sorted_created


def test_news_count(client, news_list):
    response = client.get(NEWS_HOME_URL)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news):
    response = client.get(NEWS_HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates
