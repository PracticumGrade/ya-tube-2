from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Post, Group, Comment


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "text", "pub_date", "group")


class GroupSerializer(ModelSerializer):

    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class CommentSerializer(ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
