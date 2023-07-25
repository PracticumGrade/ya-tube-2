import pytest
from rest_framework import status

from posts.models import Post
from utils import reverse


@pytest.mark.parametrize(
    "method,name,args", [
        ("POST", "post-list", None,),
        ("PUT", "post-detail", pytest.lazy_fixture("post_pk_for_args"),),
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


def test_posts_list(author_client, posts):
    url = reverse("post-list")
    response = author_client.get(url)

    data = response.json()

    assert isinstance(data, list), (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"возвращается список."
    )
    assert len(data) == len(posts), (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"для получение списка постов возвращаются все посты."
    )


@pytest.mark.parametrize(
    "method, name, args, data", [
        ("POST", "post-list", None, pytest.lazy_fixture("post_create_data"),),
        ("GET", "post-detail", pytest.lazy_fixture("post_pk_for_args"), None,),
        ("PUT", "post-detail", pytest.lazy_fixture("post_pk_for_args"), pytest.lazy_fixture("post_update_data"),),
        ("PATCH", "post-detail", pytest.lazy_fixture("post_pk_for_args"), None,),
    ]
)
def test_serialize_post(author_client, post, method, name, args, data):
    url = reverse(name, args=args)
    request_method = getattr(author_client, method.lower())
    response = request_method(url, data=data)

    data = response.json()
    assert isinstance(data, dict), (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` возвращается словарь"
    )


def test_create_post(author_client, post_create_data):
    url = reverse("post-list")
    response = author_client.post(url, data=post_create_data)

    assert Post.objects.count() == 1, (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового поста, объект был добавлен в БД."
    )

    data = response.json()
    assert data["text"] == post_create_data["text"], (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового поста, возвращаемый словарь содержит верное значение поля `text`"
    )


def test_incorrect_create_post(author_client):
    url = reverse("post-list")
    empty_data = {}
    author_client.post(url, data=empty_data)

    assert Post.objects.count() == 0, (
        f"Убедитесь, что при отправке POST-запроса с некорректными данными на url `{url}`  "
        f"для создания нового поста, объект не был добавлен в БД."
    )


@pytest.mark.parametrize(
    "method", [
        "PUT",
        "PATCH",
    ]
)
def test_update_post(author_client, post, post_pk_for_args, post_update_data, method):
    url = reverse("post-detail", args=post_pk_for_args)
    request_method = getattr(author_client, method.lower())
    response = request_method(url, data=post_update_data)

    assert Post.objects.count() == 1, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"для обновления поста, новый объект не был добавлен в БД."
    )

    post.refresh_from_db()
    assert post.text == post_update_data["text"], (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"для обновления поста, пост был обновлен в БД."
    )

    data = response.json()
    assert data["text"] == post_update_data["text"], (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"для обновления поста, возвращается словарь с обновленным полем `text`"
    )


def test_delete_post(author_client, posts, post, post_pk_for_args):
    url = reverse("post-detail", args=post_pk_for_args)
    response = author_client.delete(url)

    assert Post.objects.count() == len(posts), (
        f"Убедитесь, что при отправке DELETE-запроса на url `{url}`  "
        f"для удаления поста, из БД удаляется указанный пост."
    )

    assert response.data is None, (
        f"Убедитесь, что при отправке DELETE-запроса на url `{url}`  "
        f"для обновления поста, возвращается пустое тело ответа."
    )
