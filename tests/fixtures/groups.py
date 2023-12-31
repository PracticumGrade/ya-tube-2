import pytest
from mixer.backend.django import Mixer

from conftest import N_PER_FIXTURE


@pytest.fixture
def group(mixer: Mixer, author_user):
    return mixer.blend('posts.Group', author=author_user)


@pytest.fixture
def groups(mixer: Mixer):
    return mixer.cycle(N_PER_FIXTURE).blend('posts.Group')


@pytest.fixture
def group_pk_for_args(group):
    return group.pk,
