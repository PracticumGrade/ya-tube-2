import pytest
from rest_framework import status

from posts.models import Comment
from utils import reverse


@pytest.mark.parametrize(
    "method,name,args", [
        ("POST", "comment-list", pytest.lazy_fixture("post_and_comment_pk_for_args"),),
        ("PUT", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"),),
    ]
)
def test_bad_request_and_errors(author_client, post, method, name, args):
    url = reverse(name, args=args)
    request_method = getattr(author_client, method.lower())
    bad_data = {}
    response = request_method(url, data=bad_data)

    status_code = status.HTTP_400_BAD_REQUEST
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"c некорректными данными, возвращается статус-код {status_code}"
    )

    data = response.json()
    expected_value = {"text": ["This field is required."]}
    assert data == expected_value, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"c некорректными данными, в теле ответа возвращаются ошибки."
    )


def test_comments_list(author_client, comments_for_post, post_and_comment_pk_for_args):
    url = reverse("comment-list", args=post_and_comment_pk_for_args)
    response = author_client.get(url)

    data = response.json()

    assert isinstance(data, list), (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"возвращается список."
    )

    # +1 комментарий, так как фикстура post_and_comment_pk_for_args создает ещё один пост
    count_comments = len(comments_for_post) + 1
    assert len(data) == count_comments, (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"для получение списка комментариев к конкретному посту возвращаются все комментарии."
    )


@pytest.mark.parametrize(
    "method, name, args, data", [
        ("POST", "comment-list", pytest.lazy_fixture("post_and_comment_pk_for_args"), pytest.lazy_fixture("post_create_data"),),
        ("GET", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), None,),
        ("PUT", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), pytest.lazy_fixture("post_update_data"),),
        ("PATCH", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), None,),
    ]
)
def test_serialize_comment(author_client, post, method, name, args, data):
    url = reverse(name, args=args)
    request_method = getattr(author_client, method.lower())
    response = request_method(url, data=data)

    data = response.json()
    assert isinstance(data, dict), (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` возвращается словарь"
    )


def test_create_comment(author_client, comment_create_data, post_pk_for_args):
    url = reverse("comment-list", args=post_pk_for_args)
    response = author_client.post(url, data=comment_create_data)

    assert Comment.objects.count() == 1, (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового комментария, объект был добавлен в БД."
    )

    data = response.json()
    assert data["text"] == comment_create_data["text"], (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового комментария, возвращаемый словарь содержит верное значение поля `text`"
    )


def test_incorrect_create_comment(author_client, post_pk_for_args):
    url = reverse("comment-list", args=post_pk_for_args)
    empty_data = {}
    author_client.post(url, data=empty_data)

    assert Comment.objects.count() == 0, (
        f"Убедитесь, что при отправке POST-запроса с некорректными данными на url `{url}`  "
        f"для создания нового комментария, объект не был добавлен в БД."
    )


@pytest.mark.parametrize(
    "method", [
        "PUT",
        "PATCH",
    ]
)
def test_update_comment(author_client, comment_for_post, post_and_comment_pk_for_args, comment_update_data, method):
    url = reverse("comment-detail", args=post_and_comment_pk_for_args)
    request_method = getattr(author_client, method.lower())
    response = request_method(url, data=comment_update_data)

    assert Comment.objects.count() == 1, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"для обновления комментария, новый объект не был добавлен в БД."
    )

    comment_for_post.refresh_from_db()
    assert comment_for_post.text == comment_update_data["text"], (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"для обновления комментария, пост был обновлен в БД."
    )

    data = response.json()
    assert data["text"] == comment_update_data["text"], (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"для обновления комментария, возвращается словарь с обновленным полем `text`"
    )


def test_delete_comment(author_client, comments_for_post, comment_for_post, post_and_comment_pk_for_args):
    url = reverse("comment-detail", args=post_and_comment_pk_for_args)
    response = author_client.delete(url)

    assert Comment.objects.count() == len(comments_for_post), (
        f"Убедитесь, что при отправке DELETE-запроса на url `{url}`  "
        f"для удаления комментария, из БД удаляется указанный комментарий."
    )

    assert response.data is None, (
        f"Убедитесь, что при отправке DELETE-запроса на url `{url}`  "
        f"для удаления комментария, возвращается пустое тело ответа."
    )
