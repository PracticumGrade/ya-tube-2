from rest_framework.routers import SimpleRouter

from .views import PostModelViewSet, GroupViewSet, CommentViewSet

router = SimpleRouter()

router.register('api/v1/posts', PostModelViewSet)
router.register('api/v1/groups', GroupViewSet)
router.register(r'api/v1/posts/(?P<post_pk>\d+)/comments', CommentViewSet)
