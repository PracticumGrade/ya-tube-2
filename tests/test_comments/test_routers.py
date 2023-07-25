import pytest
from rest_framework import status

from utils import reverse

pytestmark = [
    pytest.mark.django_db
]


@pytest.mark.parametrize(
    "method, name, args, data", [
        ("GET", "comment-list", pytest.lazy_fixture("post_and_comment_pk_for_args"), None,),
        ("POST", "comment-list", pytest.lazy_fixture("post_and_comment_pk_for_args"), pytest.lazy_fixture("comment_create_data"),),
        ("GET", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), None,),
        ("PUT", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), pytest.lazy_fixture("comment_update_data"),),
        ("PATCH", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), None,),
        ("DELETE", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), None,),
    ]
)
def test_not_availability_for_for_anonymous_user(anonymous_client, comment_for_post, method, name, args, data):
    url = reverse(name, args=args)
    request_method = getattr(anonymous_client, method.lower())
    response = request_method(url, data=data)

    status_code = status.HTTP_401_UNAUTHORIZED
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"возвращается статус-код {status_code} для неавторизованного пользователя."
    )


@pytest.mark.parametrize(
    "method, name, args, status_code, data", [
        ("GET", "comment-list", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_200_OK, None,),
        ("POST", "comment-list", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_201_CREATED, pytest.lazy_fixture("comment_create_data"),),
        ("GET", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_200_OK, None,),
        ("PUT", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_200_OK, pytest.lazy_fixture("comment_update_data"),),
        ("PATCH", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_200_OK, None,),
        ("DELETE", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_204_NO_CONTENT, None,),
    ]
)
def test_availability_comment_for_author(author_client, comment_for_post, method, name, args, status_code, data):
    url = reverse(name, args=args)
    request_method = getattr(author_client, method.lower())
    response = request_method(url, data=data)

    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` "
        f"для автора поста возвращается статус-код {status_code}. "
        f"Проверьте что верно настроены права доступа автора к своему комментарию."
    )


@pytest.mark.parametrize(
    "method, name, args, status_code, data", [
        ("GET", "comment-list", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_200_OK, None,),
        ("GET", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_200_OK, None,),
        ("PUT", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_403_FORBIDDEN, pytest.lazy_fixture("comment_update_data"),),
        ("PATCH", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_403_FORBIDDEN, None,),
        ("DELETE", "comment-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"), status.HTTP_403_FORBIDDEN, None,),
    ]
)
def test_availability_post_for_reader(reader_client, post, method, name, args, status_code, data):
    url = reverse(name, args=args)
    request_method = getattr(reader_client, method.lower())
    response = request_method(url, data=data)

    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` "
        f"к чужому посту возвращается статус-код {status_code}. "
        f"Проверьте что верно настроены права доступа пользователя к чужому комментарию."
    )


@pytest.mark.parametrize(
    "method, name, data", [
        ("GET", "comment-detail", None,),
        ("PUT", "comment-detail", pytest.lazy_fixture("comment_update_data"),),
        ("PATCH", "comment-detail", None,),
        ("DELETE", "comment-detail", None,),
    ]
)
def test_not_found_post(author_client, post_pk_for_args, method, name, data):
    does_not_exists_pk = 123456789,
    args = (post_pk_for_args, does_not_exists_pk)
    url = reverse(name, args=args)
    request_method = getattr(author_client, method.lower())
    response = request_method(url, data=data)

    status_code = status.HTTP_404_NOT_FOUND
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` "
        f"для получения несуществующего объекта возвращается статус-код {status_code}"
    )
