from rest_framework.serializers import ModelSerializer
from .models import Post, Group


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "text", "pub_date", "group")


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")
