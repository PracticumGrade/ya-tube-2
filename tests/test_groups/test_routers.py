import pytest
from rest_framework import status

pytestmark = [
    pytest.mark.django_db
]


@pytest.mark.parametrize(
    "url", [
        pytest.lazy_fixture("group_list_url"),
        pytest.lazy_fixture("group_detail_url"),
    ]
)
def test_not_availability_for_for_anonymous_user(anonymous_client, group, url):
    response = anonymous_client.get(url)

    status_code = status.HTTP_401_UNAUTHORIZED
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"возвращается статус-код {status_code} для неавторизованного пользователя."
    )


@pytest.mark.parametrize(
    "url", [
        pytest.lazy_fixture("group_list_url"),
        pytest.lazy_fixture("group_detail_url"),
    ]
)
def test_availability_for_authorization_user(author_client, group, url):
    response = author_client.get(url)

    status_code = status.HTTP_200_OK
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"для авторизованного пользователя возвращается статус-код {status_code}."
    )
