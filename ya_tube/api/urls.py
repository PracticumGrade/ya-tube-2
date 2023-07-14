from rest_framework.routers import SimpleRouter

from .views import PostModelViewSet

router = SimpleRouter()

router.register('posts', PostModelViewSet)
