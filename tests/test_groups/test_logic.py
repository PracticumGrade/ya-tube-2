import pytest
from utils import reverse


def test_groups_list(author_client, groups):
    url = reverse("group-list")
    response = author_client.get(url)

    data = response.json()

    assert isinstance(data, list), (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"возвращается список."
    )
    assert len(data) == len(groups), (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"для получение списка групп возвращаются все группы."
    )


@pytest.mark.parametrize(
    "method, name, args", [
        ("GET", "group-detail", pytest.lazy_fixture("post_and_comment_pk_for_args"),),
    ]
)
def test_serialize_group(author_client, post, method, name, args):
    url = reverse(name, args=args)
    request_method = getattr(author_client, method.lower())
    response = request_method(url)

    data = response.json()
    assert isinstance(data, dict), (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` возвращается словарь"
    )
