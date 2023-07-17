from rest_framework.routers import SimpleRouter

from .views import PostModelViewSet, GroupViewSet

router = SimpleRouter()

router.register('posts', PostModelViewSet)
router.register('groups', GroupViewSet)
