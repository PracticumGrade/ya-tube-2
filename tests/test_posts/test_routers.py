import pytest
from django.shortcuts import reverse
from rest_framework import status

pytestmark = [
    pytest.mark.django_db
]


@pytest.mark.parametrize(
    "method,name,args,data", [
        ("GET", "post-list", None, None,),
        ("POST", "post-list", None, pytest.lazy_fixture("post_create_data"),),
        ("GET", "post-detail", pytest.lazy_fixture("post_pk_for_args"), None,),
        ("PUT", "post-detail", pytest.lazy_fixture("post_pk_for_args"), pytest.lazy_fixture("post_update_data"),),
        ("PATCH", "post-detail", pytest.lazy_fixture("post_pk_for_args"), None,),
        ("DELETE", "post-detail", pytest.lazy_fixture("post_pk_for_args"), None,),
    ]
)
def test_not_availability_for_for_anonymous_user(anonymous_client, post, method, name, args, data):
    url = reverse(name, args=args)
    request_method = getattr(anonymous_client, method.lower())
    response = request_method(url, data=data)

    status_code = status.HTTP_401_UNAUTHORIZED
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"возвращается статус-код {status_code} для неавторизованного пользователя."
    )


@pytest.mark.parametrize(
    "method,name,args,status_code,data", [
        ("GET", "post-list", None, status.HTTP_200_OK, None,),
        ("POST", "post-list", None, status.HTTP_201_CREATED, pytest.lazy_fixture("post_create_data"),),
        ("GET", "post-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_200_OK, None,),
        ("PUT", "post-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_200_OK, pytest.lazy_fixture("post_update_data"),),
        ("PATCH", "post-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_200_OK, None,),
        ("DELETE", "post-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_204_NO_CONTENT, None,),
    ]
)
def test_availability_post_for_author(author_client, post, method, name, args, status_code, data):
    url = reverse(name, args=args)
    request_method = getattr(author_client, method.lower())
    response = request_method(url, data=data)

    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` "
        f"для автора поста возвращается статус-код {status_code}. "
        f"Проверьте что верно настроены права доступа автора к своему посту."
    )


@pytest.mark.parametrize(
    "method,name,args,status_code,data", [
        ("GET", "post-list", None, status.HTTP_200_OK, None,),
        ("GET", "post-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_200_OK, None,),
        ("PUT", "post-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_403_FORBIDDEN, pytest.lazy_fixture("post_update_data"),),
        ("PATCH", "post-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_403_FORBIDDEN, None,),
        ("DELETE", "post-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_403_FORBIDDEN, None,),
    ]
)
def test_availability_post_for_reader(reader_client, post, method, name, args, status_code, data):
    url = reverse(name, args=args)
    request_method = getattr(reader_client, method.lower())
    response = request_method(url, data=data)

    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` "
        f"к чужому посту возвращается статус-код {status_code}. "
        f"Проверьте что верно настроены права доступа пользователя к чужому посту."
    )
