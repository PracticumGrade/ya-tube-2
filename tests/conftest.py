import pytest
from rest_framework.test import APIClient
from mixer.backend.django import mixer as _mixer

N_PER_FIXTURE = 3
POST_FIELDS = ["id", "text", "pub_date"]


MAPPING = {
    "post-list": "/api/v1/posts/",
    "post-detail": "/api/v1/posts/{0}/",
    "group-list": "/api/v1/groups/",
    "group-detail": "/api/v1/groups/{0}/",
    "comment-list": "/api/v1/posts/{0}/comments/",
    "comment-detail": "/api/v1/posts/{0}/comments/{1}/",
}


pytest_plugins = [
    'fixtures.posts',
    'fixtures.groups',
    'fixtures.comments',
]


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def anonymous_client():
    client = APIClient()
    return client


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
