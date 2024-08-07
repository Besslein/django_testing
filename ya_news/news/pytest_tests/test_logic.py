from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from .conftest import NEWS_DETAIL_URL, EDIT_URL, URL_TO_COMMENTS, DELETE_URL


FORM_DATA = {
    'text': 'Новый текст',
}
BAD_WORDS_DATA = {
    'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
}


def test_user_can_create_note(author_client, author, news):
    initial_comment_count = Comment.objects.count()
    url = reverse(NEWS_DETAIL_URL, args=(news.id,))
    response = author_client.post(url, data=FORM_DATA)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == initial_comment_count + 1
    new_comment = Comment.objects.latest('id')
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.news == news
    assert new_comment.author == author


def test_anonymous_user_cannot_create_note(client, news):
    count = Comment.objects.count()
    url = reverse(NEWS_DETAIL_URL, args=(news.id,))
    response = client.post(url, data=FORM_DATA)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == count


def test_user_cannot_use_bad_words(author_client, news):
    count = Comment.objects.count()
    url = reverse(NEWS_DETAIL_URL, args=(news.id,))
    response = author_client.post(url, data=BAD_WORDS_DATA)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == count


def test_author_can_edit_comment(author, author_client, news, comment):
    url = reverse(EDIT_URL, args=(comment.id,))
    response = author_client.post(url, data=FORM_DATA)
    redirect_url = reverse(URL_TO_COMMENTS, args=(news.id,)) + '#comments'
    assertRedirects(response, redirect_url)
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment_from_db.text == FORM_DATA['text']
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news


def test_other_user_cannot_edit_comment(reader_client, comment):
    response = reader_client.post(EDIT_URL, args=(comment.id,), data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text
    assert comment.author == comment_from_db.author
    assert comment.news == comment_from_db.news


def test_author_can_delete_comment(author_client, comment):
    count = Comment.objects.count() - 1
    url = reverse(DELETE_URL, args=(comment.id,))
    response = author_client.delete(url)
    redirect_url = reverse(URL_TO_COMMENTS, args=(comment.id,)) + '#cpmments'
    assertRedirects(response, redirect_url)
    assert Comment.objects.count() == count


def test_other_user_cannot_delete_comment(reader_client, comment):
    count = Comment.objects.count()
    response = reader_client.delete(DELETE_URL, args=(comment.id,))
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == count
