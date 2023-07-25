import pytest
from rest_framework import status

from utils import reverse

pytestmark = [
    pytest.mark.django_db
]


@pytest.mark.parametrize(
    "name, args", [
        ("group-list", None,),
        ("group-detail", pytest.lazy_fixture("group_pk_for_args"),),
    ]
)
def test_not_availability_for_for_anonymous_user(anonymous_client, group, name, args):
    url = reverse(name, args=args)
    response = anonymous_client.get(url)

    status_code = status.HTTP_401_UNAUTHORIZED
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"возвращается статус-код {status_code} для неавторизованного пользователя."
    )


@pytest.mark.parametrize(
    "name, args", [
        ("group-list", None,),
        ("group-detail", pytest.lazy_fixture("group_pk_for_args"),),
    ]
)
def test_availability_for_authorization_user(author_client, group, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)

    status_code = status.HTTP_200_OK
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"для авторизованного пользователя возвращается статус-код {status_code}."
    )


@pytest.mark.parametrize(
    "method, name", [
        ("GET", "group-detail",)
    ]
)
def test_not_found_group(author_client, method, name):
    does_not_exists_pk = 123456789,
    url = reverse(name, args=does_not_exists_pk)
    request_method = getattr(author_client, method.lower())
    response = request_method(url)

    status_code = status.HTTP_404_NOT_FOUND
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` "
        f"для получения несуществующего объекта возвращается статус-код {status_code}"
    )
