from .models import Blog
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from comment.serializers import ShowCommentSerializer


class BlogCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Blog
        exclude = ('created_at','updated_at','author')


# Detail view showing author id along with author name
class BlogRetrieveSerializer(ModelSerializer):
    author_name = serializers.SerializerMethodField()
    comments = ShowCommentSerializer(many=True)
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'author_name','comments']

    def get_author_name(self, obj):
        return obj.author.username
    

class BlogSerializer(ModelSerializer):
    author_name = serializers.SerializerMethodField()
    comments = ShowCommentSerializer(many=True)
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author_name','comments']

    def get_author_name(self, obj):
        return obj.author.username