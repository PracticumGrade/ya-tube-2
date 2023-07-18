import pytest
from rest_framework import status

pytestmark = [
    pytest.mark.django_db
]


@pytest.mark.parametrize(
    "method, url, data", [
        ("GET", pytest.lazy_fixture("comment_list_for_post_url"), None,),
        ("POST", pytest.lazy_fixture("comment_list_for_post_url"), pytest.lazy_fixture("comment_create_data"),),
        ("GET", pytest.lazy_fixture("comment_detail_for_post_url"), None,),
        ("PUT", pytest.lazy_fixture("comment_detail_for_post_url"), pytest.lazy_fixture("comment_update_data"),),
        ("PATCH", pytest.lazy_fixture("comment_detail_for_post_url"), None,),
        ("DELETE", pytest.lazy_fixture("comment_detail_for_post_url"), None,),
    ]
)
def test_not_availability_for_for_anonymous_user(anonymous_client, comment_for_post, method, url, data):
    request_method = getattr(anonymous_client, method.lower())
    response = request_method(url, data=data)

    status_code = status.HTTP_401_UNAUTHORIZED
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"возвращается статус-код {status_code} для неавторизованного пользователя."
    )


@pytest.mark.parametrize(
    "method,url,status_code,data", [
        ("GET", pytest.lazy_fixture("comment_list_for_post_url"), status.HTTP_200_OK, None,),
        ("POST", pytest.lazy_fixture("comment_list_for_post_url"), status.HTTP_201_CREATED, pytest.lazy_fixture("comment_create_data"),),
        ("GET", pytest.lazy_fixture("comment_detail_for_post_url"), status.HTTP_200_OK, None,),
        ("PUT", pytest.lazy_fixture("comment_detail_for_post_url"), status.HTTP_200_OK, pytest.lazy_fixture("comment_update_data"),),
        ("PATCH", pytest.lazy_fixture("comment_detail_for_post_url"), status.HTTP_200_OK, None,),
        ("DELETE", pytest.lazy_fixture("comment_detail_for_post_url"), status.HTTP_204_NO_CONTENT, None,),
    ]
)
def test_availability_comment_for_author(author_client, comment_for_post, method, url, status_code, data):
    request_method = getattr(author_client, method.lower())
    response = request_method(url, data=data)

    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` "
        f"для автора поста возвращается статус-код {status_code}. "
        f"Проверьте что верно настроены права доступа автора к своему комментарию."
    )


@pytest.mark.parametrize(
    "method,url,status_code,data", [
        ("GET", pytest.lazy_fixture("comment_list_for_post_url"), status.HTTP_200_OK, None,),
        ("GET", pytest.lazy_fixture("comment_detail_for_post_url"), status.HTTP_200_OK, None,),
        ("PUT", pytest.lazy_fixture("comment_detail_for_post_url"), status.HTTP_403_FORBIDDEN, pytest.lazy_fixture("comment_update_data"),),
        ("PATCH", pytest.lazy_fixture("comment_detail_for_post_url"), status.HTTP_403_FORBIDDEN, None,),
        ("DELETE", pytest.lazy_fixture("comment_detail_for_post_url"), status.HTTP_403_FORBIDDEN, None,),
    ]
)
def test_availability_post_for_reader(reader_client, post, method, url, status_code, data):
    request_method = getattr(reader_client, method.lower())
    response = request_method(url, data=data)

    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` "
        f"к чужому посту возвращается статус-код {status_code}. "
        f"Проверьте что верно настроены права доступа пользователя к чужому комментарию."
    )


@pytest.mark.parametrize(
    "method,data", [
        ("GET", None,),
        ("PUT", pytest.lazy_fixture("comment_update_data"),),
        ("PATCH", None,),
        ("DELETE", None,),
    ]
)
def test_not_found_post(author_client, method, data, comment_list_for_post_url):
    does_not_exists_pk = 123456789,
    url = f"{comment_list_for_post_url}{does_not_exists_pk}/"
    request_method = getattr(author_client, method.lower())
    response = request_method(url, data=data)

    status_code = status.HTTP_404_NOT_FOUND
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` "
        f"для получения несуществующего объекта возвращается статус-код {status_code}"
    )
