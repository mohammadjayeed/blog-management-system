from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from .models import Comment
from blog.models import Blog
from rest_framework.permissions import IsAuthenticated
from .serializers import CommentPostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema


class CommentCreateViewSet(ViewSet):
    
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=CommentPostSerializer,tags=['comments'])
    def create(self, request, *args, **kwargs):
        
        blog_post_pk = self.kwargs.get('pk')

        
        queryset = get_object_or_404(Blog, pk = blog_post_pk)

        serializer = CommentPostSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status": "error","message": serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
        
        if Comment.objects.filter(author_id=request.user.id, blog_id=queryset.id).exists():
            raise ValidationError(detail={'comment_status': ['Already commented by author']})

        serializer.save(author=request.user,blog=queryset)
        return Response({"status": "success","message": "comment posted."}, status.HTTP_201_CREATED)


