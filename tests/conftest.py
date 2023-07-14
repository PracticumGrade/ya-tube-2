import pytest
from rest_framework.test import APIClient
from mixer.backend.django import mixer as _mixer

N_PER_FIXTURE = 3
POST_FIELDS = ["id", "text", "pub_date"]

pytest_plugins = [
    'fixtures.posts',
]


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def anonymous_client():
    client = APIClient()
    return client


@pytest.fixture
def post_create_data():
    return {
        "text": "Текст заметки",
    }


@pytest.fixture
def post_update_data():
    return {
        "text": "Новый текст заметки",
    }


@pytest.fixture
def post_pk_for_args(post):
    return post.pk,


@pytest.fixture
def author_user(django_user_model):
    return django_user_model.objects.create(username="author")


@pytest.fixture
def author_client(author_user):
    client = APIClient()
    client.force_authenticate(user=author_user)

    return client


@pytest.fixture
def reader_user(django_user_model):
    return django_user_model.objects.create(username="reader")


@pytest.fixture
def reader_client(reader_user):
    client = APIClient()
    client.force_authenticate(user=reader_user)

    return client
