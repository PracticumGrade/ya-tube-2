import pytest
from rest_framework import status


@pytest.fixture
def user_credential():
    return {
        "username": "username",
        "password": "password"
    }


@pytest.fixture
def login_user(django_user_model, user_credential):
    user = django_user_model.objects.create_user(**user_credential)
    return user


def test_available_get_token(anonymous_client, login_user, user_credential):
    url = "/api/v1/api-token-auth/"
    resp = anonymous_client.post(url, data=user_credential)

    assert resp.status_code == status.HTTP_200_OK, (
        f"Убедитесь, что в проекте настроен эндпоинт {url} для получения токена."
    )


def test_add_rest_framework_authtoken_app(settings):
    installed_app = 'rest_framework.authtoken'
    assert installed_app in settings.INSTALLED_APPS, (
        f"Проверьте, что в файле `ya_tube/settings.py` с настройками проекта в `INSTALLED_APPS` "
        f"добавлено приложение `{installed_app}`"
    )


@pytest.mark.parametrize(
    "rest_framework_key, default_class",
    [
        ('DEFAULT_PERMISSION_CLASSES', 'rest_framework.permissions.IsAuthenticated'),
        ('DEFAULT_AUTHENTICATION_CLASSES', 'rest_framework.authentication.TokenAuthentication')
    ]
)
def test_rest_framework_settings(settings, rest_framework_key, default_class):
    setting_name = "REST_FRAMEWORK"
    rest_framework_setting = getattr(settings, setting_name, None)
    assert rest_framework_setting is not None, (
        f"Проверьте, что в файле `ya_tube/settings.py` с настройками проекта "
        f"добавлена настройка `{setting_name}`"
    )

    assert rest_framework_key in rest_framework_setting, (
        f"Проверьте, что в файле `ya_tube/settings.py` c настройками проекта в `{setting_name}` "
        f"добавлен ключ `{rest_framework_key}`"
    )

    assert default_class in rest_framework_setting[rest_framework_key], (
        f"Проверьте, что в файле `ya_tube/settings.py` c настройками проекта в `{setting_name}` "
        f"по ключу `{rest_framework_key}` добавлен класс `{default_class}`"
    )
