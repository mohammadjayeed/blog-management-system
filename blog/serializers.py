from .models import Blog
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
class BlogCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Blog
        exclude = ('created_at','updated_at','author')


# Detail view showing author id along with author name
class BlogRetrieveSerializer(ModelSerializer):
    author_name = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'slug', 'created_at', 'updated_at', 'author', 'author_name']

    def get_author_name(self, obj):
        return obj.author.username