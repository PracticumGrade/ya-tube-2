def test_init_api_application():
    try:
        import api
    except ImportError:
        raise AssertionError(
            'Убедитесь, что инициализирована приложение `api` '
            'и в нем объявлены маршруты (urls), представления (views) и сериализаторы (serializers).'
        )
