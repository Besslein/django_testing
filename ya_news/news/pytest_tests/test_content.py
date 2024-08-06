import pytest
from django.conf import settings

from news.forms import CommentForm
from .conftest import UrlConst


FORM_NAME = 'form'


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, news_detail_url):
    response = author_client.get(UrlConst.NEWS_DETAIL_URL)
    assert FORM_NAME in response.context
    assert isinstance(response.context[FORM_NAME], CommentForm)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news_detail_url):
    response = client.get(UrlConst.NEWS_DETAIL_URL)
    assert FORM_NAME not in response.context


@pytest.mark.django_db
def test_comments_order(client, news_detail_url, comments):
    response = client.get(UrlConst.NEWS_DETAIL_URL)
    all_comments = response.context['news'].comment_set.all()
    all_created = [comment.created for comment in all_comments]
    sorted_created = sorted(all_created)
    assert all_created == sorted_created


@pytest.mark.django_db
def test_news_count(client, news_home_url, news_list):
    response = client.get(UrlConst.NEWS_HOME_URL)
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news_home_url, news_list):
    response = client.get(UrlConst.NEWS_HOME_URL)
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates
