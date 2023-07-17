import pytest
from mixer.backend.django import Mixer

from conftest import N_PER_FIXTURE


@pytest.fixture
def comment_for_post(mixer: Mixer, author_user, post):
    return mixer.blend(
        'posts.Comment', author=author_user, post=post,
    )


@pytest.fixture
def comments_for_post(mixer: Mixer, post):
    return mixer.cycle(N_PER_FIXTURE).blend('posts.Comment', post=post)


@pytest.fixture
def comment_pk_for_args(comment_for_post):
    return comment_for_post.pk,


@pytest.fixture
def comment_list_for_post_url(post_pk_for_args, comment_pk_for_args):
    return f"/api/v1/posts/{post_pk_for_args[0]}/comments/"


@pytest.fixture
def comment_detail_for_post_url(post_pk_for_args, comment_pk_for_args):
    return f"/api/v1/posts/{post_pk_for_args[0]}/comments/{comment_pk_for_args[0]}/"


@pytest.fixture
def comment_create_data():
    return {
        "text": "Текст комментария",
    }


@pytest.fixture
def comment_update_data():
    return {
        "text": "Новый текст комментария",
    }
