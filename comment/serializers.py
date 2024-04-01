from rest_framework import serializers
from .models import Comment
class CommentPostSerializer(serializers.ModelSerializer):
    # username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['comment']


class ShowCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['author','author_name','comment','created_at']

    def get_author_name(self, obj):
        return obj.author.username if obj.author else None